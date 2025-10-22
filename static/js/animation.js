document.addEventListener('wheel', (e) => {
  e.preventDefault();
  const direction = e.deltaY > 0 ? 1 : -1;
  const sections = document.querySelectorAll('.landing-section, .insight-container-1, .insight-container-2, .insight-container-3, .signup-form, .footer');
  const currentIndex = Array.from(sections).findIndex(sec => sec.getBoundingClientRect().top >= 0);

  let nextIndex = currentIndex + direction;
  if (nextIndex < 0) nextIndex = 0;
  if (nextIndex >= sections.length) nextIndex = sections.length - 1;

  sections[nextIndex].scrollIntoView({ behavior: 'smooth' });
}, { passive: false });

