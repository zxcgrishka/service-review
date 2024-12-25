document.addEventListener('DOMContentLoaded', function() {
    // Обработка кликов по звездам в форме отзыва
    const ratingStars = document.querySelectorAll('.star-rating-input .star');
    const ratingInput = document.getElementById('rating');

    ratingStars.forEach(star => {
        star.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            ratingInput.value = value;
            updateStars(ratingStars, value);
        });

        star.addEventListener('mouseover', function() {
            const value = this.getAttribute('data-value');
            updateStars(ratingStars, value);
        });

        star.addEventListener('mouseout', function() {
            const currentValue = ratingInput.value;
            updateStars(ratingStars, currentValue);
        });
    });

    // Отображение звезд для общего рейтинга и отзывов
    const ratingElements = document.querySelectorAll('.star-rating');
    ratingElements.forEach(element => {
        const rating = element.getAttribute('data-rating');
        updateRatingDisplay(element, rating);
    });

    function updateStars(stars, value) {
        stars.forEach(star => {
            const starValue = star.getAttribute('data-value');
            if (starValue <= value) {
                star.style.color = 'gold';
            } else {
                star.style.color = 'black';
            }
        });
    }

    function updateRatingDisplay(element, rating) {
        element.innerHTML = '';
        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('span');
            star.classList.add('star');
            star.innerHTML = '&#9733;';
            if (i <= rating) {
                star.style.color = 'gold';
            } else {
                star.style.color = 'black';
            }
            element.appendChild(star);
        }
    }
});
