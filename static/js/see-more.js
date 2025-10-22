const seeMoreBtn = document.getElementById('seeMoreBtn');
const hiddenCategories = document.querySelectorAll('.category-box.hidden');

seeMoreBtn.addEventListener('click', () => {
  hiddenCategories.forEach(box => {
    box.classList.toggle('show');  // toggle "show"
  });

  seeMoreBtn.textContent = 
    seeMoreBtn.textContent === 'See More' ? 'See Less' : 'See More';
});

// Set background images from data-bg
document.querySelectorAll('.category-box').forEach(box => {
  const bg = box.getAttribute('data-bg');
  if(bg) box.style.backgroundImage = `url(${bg})`;
});

