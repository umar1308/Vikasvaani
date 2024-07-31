

function verify2(){
    alert('You will recieve a confirmation mail. Check out to confirm.');
}

document.addEventListener('DOMContentLoaded', () => {
    const slidingElement = document.querySelector('.sliding-element');
    setTimeout(() => {
        slidingElement.classList.add('visible');
    }, 100); // Add a slight delay to ensure the transition occurs
});

document.getElementById('scroll-button').addEventListener('click', function() {
    document.getElementById('target-section').scrollIntoView({
        behavior: 'smooth'
    });
});



document.addEventListener('DOMContentLoaded', () => {
    const card2Container = document.querySelector('');

    const showCardOnScroll = () => {
        const cardPosition = card2Container.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;

        if (cardPosition < screenPosition) {
            card2Container.classList.add('visible');
        }
    };

    window.addEventListener('scroll', showCardOnScroll);
});

document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggleButton');
    const sidebar = document.getElementById('sidebar');

    toggleButton.addEventListener('click', () => {
        if (sidebar.style.left === '-250px') {
            sidebar.style.left = '0';
        } else {
            sidebar.style.left = '-250px';
        }
    });
});

// CARASOUSEL ON INDEX
document.addEventListener('DOMContentLoaded', () => {
    const carouselItems = document.querySelectorAll('.carousel-item');
    const dots = document.querySelectorAll('.dot');
    const leftArrow = document.querySelector('.left-arrow');
    const rightArrow = document.querySelector('.right-arrow');
    
    let currentIndex = 0;
    
    function updateCarousel(index) {
        carouselItems.forEach((item, i) => {
            item.style.transform = `translateX(-${index * 100}%)`;
        });
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }
    
    function showNext() {
        currentIndex = (currentIndex + 1) % carouselItems.length;
        updateCarousel(currentIndex);
    }
    
    function showPrevious() {
        currentIndex = (currentIndex - 1 + carouselItems.length) % carouselItems.length;
        updateCarousel(currentIndex);
    }
    
    rightArrow.addEventListener('click', showNext);
    leftArrow.addEventListener('click', showPrevious);
    
    dots.forEach(dot => {
        dot.addEventListener('click', (e) => {
            currentIndex = parseInt(e.target.getAttribute('data-slide'));
            updateCarousel(currentIndex);
        });
    });
});

