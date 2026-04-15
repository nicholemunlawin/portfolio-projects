// Cache navigation links and their matching sections for active-state updates.
const navLinks = Array.from(document.querySelectorAll('.nav a'));
const sections = navLinks
    .map(link => document.querySelector(link.getAttribute('href')))
    .filter(Boolean);

// Keep the navigation underline aligned with the section currently in view.
function setActiveNav() {
    const scrollY = window.scrollY;
    const viewportBottom = scrollY + window.innerHeight;
    const pageBottom = document.documentElement.scrollHeight - 4;

    let currentId = '';

    if (viewportBottom >= pageBottom) {
    currentId = sections[sections.length - 1]?.id || currentId;
    } else {
    for (const section of sections) {
        const top = section.offsetTop - 120;
        if (scrollY >= top) currentId = section.id;
    }
    }

    navLinks.forEach(link => {
    const active = link.getAttribute('href') === '#' + currentId;
    link.classList.toggle('active', active);
    });
}

// Re-trigger reveal animations whenever elements leave and re-enter the viewport.
const revealElements = Array.from(document.querySelectorAll('.reveal'));

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
    if (entry.isIntersecting) {
        entry.target.classList.remove('visible');
        requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            entry.target.classList.add('visible');
        });
        });
    } else {
        entry.target.classList.remove('visible');
    }
    });
}, {
    threshold: 0.18,
    rootMargin: '0px 0px -8% 0px'
});

revealElements.forEach(el => {
    el.classList.remove('visible');
    revealObserver.observe(el);
});

// Throttle scroll-driven UI updates with requestAnimationFrame.
let ticking = false;
function onScroll() {
    if (!ticking) {
    window.requestAnimationFrame(() => {
        setActiveNav();
        ticking = false;
    });
    ticking = true;
    }
}

window.addEventListener('scroll', onScroll, { passive: true });
window.addEventListener('resize', setActiveNav);
// Animate any elements already visible when the page initially loads.
window.addEventListener('load', () => {
    setActiveNav();
    setTimeout(() => {
    revealElements.forEach((el) => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.92 && rect.bottom > 0) {
        el.classList.remove('visible');
        requestAnimationFrame(() => {
            requestAnimationFrame(() => el.classList.add('visible'));
        });
        }
    });
    }, 80);
});
setActiveNav();
