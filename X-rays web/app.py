import sys
import os
import stat
from myproject import app, db
from flask import send_file
from flask import render_template, redirect, request, url_for, flash,session,jsonify
from flask_login import login_user, login_required, logout_user,current_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm,ChangePasswordForm
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from predict import model_prediction,load_model
from flask import send_from_directory
from werkzeug.serving import WSGIRequestHandler
from myproject.forms import SaveDiagnosisForm

WSGIRequestHandler.timeout = 300



@app.route('/')
def index():
    if current_user.is_authenticated:  # Kiểm tra xem người dùng đã đăng nhập hay chưa
        if current_user.role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif current_user.role == 'patient':
            return redirect(url_for('patient_dashboard'))
    return render_template('index.html', logged_in=False)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out", "info")
    return redirect(url_for('index'))

@app.route('/logined')
@login_required
def logged_in():
    logged_in = 'user_id' in session  # Kiểm tra nếu người dùng đã đăng nhập
    return render_template('index.html', logged_in=logged_in)

@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    return render_template('doctor_dashboard.html')

@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
    if current_user.role != 'patient':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    return render_template('patient_dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Tìm người dùng trong database
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)  # Thêm tùy chọn remember để giữ người dùng đăng nhập
            session['user_id'] = user.id
            session['name'] = user.name
            
            # Kiểm tra vai trò người dùng để chuyển hướng
            if user.role == 'doctor':
                flash('Đăng nhập thành công với vai trò bác sĩ!', category='success')
                return redirect(url_for('doctor_dashboard'))  # Chuyển hướng đến trang bác sĩ
            elif user.role == 'patient':
                flash('Đăng nhập thành công với vai trò bệnh nhân!', category='success')
                return redirect(url_for('patient_dashboard'))  # Chuyển hướng đến trang bệnh nhân
            else:
                flash('Đăng nhập thành công!', category='success')
                return redirect(url_for('index'))  # Chuyển hướng đến trang chính
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại.', category='danger')

    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Kiểm tra sự tồn tại của username và email
        existing_username = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()

        # Kiểm tra và hiển thị lỗi nếu có
        errors = []
        if existing_username:
            errors.append("Username is already taken.")
        if existing_email:
            errors.append("Email is already taken.")
        
        if errors:
            # Hiển thị các lỗi nếu có
            for error in errors:
                flash(error, "danger")
        else:
            # Tạo người dùng mới
            user = User(
                name=form.name.data,
                phone_number=form.phone_number.data,
                birth_day=form.birth_day.data,
                gender=form.gender.data,
                email=form.email.data,
                username=form.username.data,
                password=form.password.data
            )

            try:
                db.session.add(user)
                db.session.commit()
                flash("User registered successfully!", "success")
                return redirect(url_for('login'))
            except Exception as e:
                print(f"Error adding user to database: {e}")
                db.session.rollback()
                flash("An error occurred. Please try again.", "danger")

    return render_template('register.html', form=form)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data

        if not current_user.check_password(current_password):
            flash('Mật khẩu hiện tại không đúng', 'danger')
            return render_template('change_password.html')

        current_user.set_password(new_password)
        db.session.commit()

        flash('Change Password Successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('change_password.html', form=form)

@app.route('/user_info', methods=['GET'])
@login_required
def user_info():
    # Lấy thông tin của người dùng hiện tại
    user = current_user  # `current_user` được Flask-Login cung cấp

    # Dữ liệu cần hiển thị
    user_data = {
        'index': 1, 
        'name': user.name,
        'email': user.email,
        'phone_number': user.phone_number,
        'birth_day': user.birth_day,
        'gender': user.gender,
        'diagnose_name': user.diagnose_name,
        'diagnose_image': user.diagnose_image
    }
    return render_template('user_info.html', user_data=user_data)

# Định nghĩa thư mục lưu ảnh upload
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')

# Cấp quyền cho thư mục static/uploads
folder_path = app.config['UPLOAD_FOLDER']

@app.route('/upload_image/<int:patient_id>', methods=['POST'])
@login_required
def upload_image(patient_id):
    patient = User.query.get_or_404(patient_id)

    # Kiểm tra nếu file được upload
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('patient_detail', id=patient_id))

    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        model, device = load_model()
        output_image, diagnosis = model_prediction(file_path, model, device)

        # Trả về dữ liệu sau khi predict
        return render_template(
            'patient_detail.html',
            patient=patient,
            uploaded_image=filename,
            output_image=output_image,
            diagnosis=diagnosis,
            form=SaveDiagnosisForm()
        )
    except Exception as e:
        flash(f"Error during prediction: {e}", 'danger')
        return redirect(url_for('patient_detail', id=patient_id))





@app.route('/show_image/<path:filename>')
@login_required
def show_image(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path)
    
@app.route('/patient_list')
@login_required
def patient_list():
    # Truy vấn tất cả người dùng có vai trò là 'patient'
    patients = User.query.filter_by(role='patient').all()
    return render_template('patient_list.html', patients=patients)


@app.route('/patient_detail/<int:patient_id>', methods=['GET'])
@login_required
def patient_detail(patient_id):
    # Truy vấn bệnh nhân từ database
    patient = User.query.get_or_404(patient_id)

    # Render template với đối tượng `patient`
    return render_template('patient_detail.html', patient=patient)

@app.route('/predict')
@login_required
def predict():
    return render_template('patient_detail.html')


@app.route('/save_diagnosis/<int:patient_id>', methods=['POST'])
@login_required
def save_diagnosis(patient_id):
    print("Route save_diagnosis triggered")

    # Truy vấn bệnh nhân
    patient = User.query.get_or_404(patient_id)

    # Lấy dữ liệu từ form
    diagnosis_name = request.form.get('diagnosis_name').replace("[", "").replace("]", "").replace("'", "")
    diagnosis_image = request.form.get('diagnosis_image')

    # Kiểm tra dữ liệu
    if not diagnosis_name or not diagnosis_image:
        flash('Invalid data. Diagnosis could not be saved.', 'danger')
        return redirect(url_for('patient_detail', patient_id=patient_id))

    # Gán dữ liệu vào đối tượng patient
    patient.diagnose_name = diagnosis_name
    patient.diagnose_image = diagnosis_image

    try:
        # Lưu thay đổi vào database
        db.session.commit()
        flash('Diagnosis saved successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error saving diagnosis: {e}")
        flash(f'Error saving diagnosis: {e}', 'danger')

    # Chuyển hướng về trang chi tiết bệnh nhân
    return redirect(url_for('patient_detail', patient_id=patient_id))







if __name__ == '__main__':
    app.run(debug=True)
