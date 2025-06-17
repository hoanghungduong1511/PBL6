document.addEventListener('DOMContentLoaded', function () {
    const dropdownToggle = document.getElementById('dropdownMenu');
    const dropdownMenu = document.getElementById('dropdownMenuContent');
  
    dropdownToggle.addEventListener('click', function (event) {
      event.preventDefault(); // Ngăn chặn hành động mặc định của thẻ <a>
      const isVisible = dropdownMenu.style.display === 'block';
      dropdownMenu.style.display = isVisible ? 'none' : 'block';
    });
  
    // Ẩn menu khi nhấp ra ngoài
    document.addEventListener('click', function (event) {
      if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.style.display = 'none';
      }
    });
  });

  function scrollToAppointment() {
    const element = document.getElementById("book-appointment");
    element.scrollIntoView({ behavior: "smooth", block: "center" });
}

document.querySelector('.dropdown-toggle').addEventListener('focus', function() {
    this.blur();
  });

document.getElementById("check-now").addEventListener("click", () => {
  const flexContainer = document.getElementById("flex-container");
  const formContainer = document.getElementById("form-container");

  // Thêm class để dịch bảng sang trái và hiển thị form
  flexContainer.classList.add("shift-left");

  // Hiển thị form bằng cách thay đổi display và opacity
  formContainer.style.display = "block";
  setTimeout(() => {
      formContainer.style.opacity = "1";
  }, 10);
});



  