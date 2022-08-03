const body = document.querySelector('body'),
    navBar = document.querySelector('nav'),
    navItem = document.querySelector('.navlinks'),
    navLinks = document.querySelectorAll('.navlinks li'),
    burger = document.querySelector('.burger');

burger.addEventListener('click', () => {
    burger.classList.toggle('active');
    navBar.classList.toggle('show');
})
