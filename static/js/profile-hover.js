// profile-hover.js
// When user hovers over a .profile-pic, after a short delay navigate to /profile/
(function(){
  function initHoverRedirect(){
    const pics = document.querySelectorAll('.profile-pic');
    pics.forEach(img => {
      let timer = null;
      img.addEventListener('mouseenter', function(){
        // small delay to avoid accidental redirects
        timer = setTimeout(() => {
          // if image is inside a link already, follow that link instead
          const parentLink = img.closest('a');
          if (parentLink && parentLink.href) {
            window.location.href = parentLink.href;
            return;
          }
          // otherwise go to /profile/
          window.location.href = '/profile/';
        }, 600);
      });
      img.addEventListener('mouseleave', function(){
        if (timer) {
          clearTimeout(timer);
          timer = null;
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHoverRedirect);
  } else {
    initHoverRedirect();
  }
})();
