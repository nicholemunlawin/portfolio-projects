// Cache navigation links and their matching sections for active-state updates.
const navLinks = Array.from(document.querySelectorAll('.nav a'));
const sections = navLinks
    .map(link => document.querySelector(link.getAttribute('href')))
    .filter(Boolean);
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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

// Reveal elements once as they enter the viewport, and skip motion-heavy effects when reduced motion is preferred.
const revealElements = Array.from(document.querySelectorAll('.reveal'));
let revealObserver = null;

if (prefersReducedMotion) {
    revealElements.forEach(el => el.classList.add('visible'));
} else {
    revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
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
}

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
    if (prefersReducedMotion) {
    revealElements.forEach(el => el.classList.add('visible'));
    }
});
setActiveNav();
