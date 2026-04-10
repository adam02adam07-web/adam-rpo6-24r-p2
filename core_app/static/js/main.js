// Navbar scroll shadow
const nav = document.getElementById('mainNav');
if (nav) {
    window.addEventListener('scroll', () => {
        nav.classList.toggle('scrolled', scrollY > 10);
    });
}