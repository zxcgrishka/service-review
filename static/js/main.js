document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".rating .stars .star");
    const inputs = document.querySelectorAll(".rating .stars .star-input");

    stars.forEach((star, index) => {
        star.addEventListener("mouseover", () => {
            // Сбрасываем все подсветки перед новым наведением
            resetHoverEffect();
            // Подсвечиваем только те звезды, которые идут до текущей
            for (let i = 0; i <= index; i++) {
                stars[i].classList.add("hovered");
            }
        });

        star.addEventListener("mouseout", () => {
            // Убираем подсветку при выходе курсора
            resetHoverEffect();
        });

        star.addEventListener("click", () => {
            // Сбрасываем все фиксированные звезды перед новым кликом
            resetFillEffect();
            // Фиксируем звезды до текущей, включая её
            for (let i = 0; i <= index; i++) {
                inputs[i].checked = true; // Устанавливаем радиокнопку как выбранную
                stars[i].classList.add("filled"); // Добавляем класс для подсветки
            }
        });
    });

    // Функция сброса подсветки для всех звезд
    function resetHoverEffect() {
        stars.forEach(star => star.classList.remove("hovered"));
    }

    // Функция сброса фиксированных звезд
    function resetFillEffect() {
        stars.forEach(star => star.classList.remove("filled"));
        inputs.forEach(input => input.checked = false); // Снимаем все отметки с радиокнопок
    }
});
