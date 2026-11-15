const toggleButtons = document.querySelectorAll("[data-toggle]");

toggleButtons.forEach(button => {
    button.addEventListener("click", () => {
        const targetId = button.dataset.toggle;
        const target = document.getElementById(targetId);

        if (!target) {
            return;
        }

        target.hidden = !target.hidden;

        button.textContent = target.hidden
            ? "Xem các dấu hiệu nhận diện"
            : "Ẩn các dấu hiệu nhận diện";
    });
});