
    // Sự kiện bấm Check now
    document.getElementById("check-now").addEventListener("click", () => {
        const flexContainer = document.getElementById("flex-container");
        const formContainer = document.getElementById("form-container");
        // Hiển thị form upload
        flexContainer.classList.add("shift-left");
        formContainer.style.display = "block";
        setTimeout(() => {
            formContainer.style.opacity = "1";
        }, 10);
    });

    // Sự kiện chọn file
    document.getElementById("inputImage").addEventListener("change", (event) => {
        const file = event.target.files[0];
        const fileNameElement = document.getElementById("file-name");
        const previewContainer = document.getElementById("image-preview-container");
        const previewImage = document.getElementById("image-preview");
        const predictButton = document.getElementById("predict-button");

        if (file) {
            // Hiển thị tên file
            fileNameElement.textContent = `File Selected: ${file.name}`;
            fileNameElement.style.display = "block";

            // Hiển thị ảnh preview
            const reader = new FileReader();
            reader.onload = function (e) {
                previewImage.src = e.target.result;
                previewContainer.style.display = "block";
            };
            reader.readAsDataURL(file);

            // Hiển thị nút Predict
            predictButton.style.display = "block";
            predictButton.classList.add('active');
        } else {
            // Ẩn nếu không có file
            fileNameElement.style.display = "none";
            previewContainer.style.display = "none";
            predictButton.style.display = "none";
        }
    });
    
    
    
