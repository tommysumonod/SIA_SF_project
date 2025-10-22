document.addEventListener('DOMContentLoaded', () => {
  const signupModal = document.getElementById('signupModal');
  const signinModal = document.getElementById('signinModal');

  const openSignup = document.getElementById('openSignupModal');
  const openLogin = document.getElementById('openLoginModal');
  const openLoginFromSignup = document.getElementById('openLoginFromSignup');
  const openSignupFromLogin = document.getElementById('openSignupFromLogin');

  // helper
  function openModal(modal) {
    if (!modal) return;
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
  }
  function closeModal(modal) {
    if (!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-open');
  }
  function closeAll() {
    closeModal(signupModal);
    closeModal(signinModal);
  }

  // attach openers (guard with ? in case element missing)
  openSignup?.addEventListener('click', (e) => { e.preventDefault(); openModal(signupModal); });
  openLogin?.addEventListener('click', (e) => { e.preventDefault(); openModal(signinModal); });

  openLoginFromSignup?.addEventListener('click', (e) => { e.preventDefault(); closeModal(signupModal); openModal(signinModal); });
  openSignupFromLogin?.addEventListener('click', (e) => { e.preventDefault(); closeModal(signinModal); openModal(signupModal); });

  // close buttons (select by data attribute)
  document.querySelectorAll('[data-close]').forEach(btn => {
    btn.addEventListener('click', (e) => { e.preventDefault(); closeAll(); });
  });

  // click outside to close
  window.addEventListener('click', (e) => {
    if (e.target === signupModal) closeModal(signupModal);
    if (e.target === signinModal) closeModal(signinModal);
  });

  // optional: re-open modal if server-side messages indicate validation error
  // This works only if your template injects a small flag when messages exist,
  // e.g. in base.html you can set <script>window.SERVER_MESSAGES = {{ has_messages|yesno:"1,0" }};</script>
  // For simplicity, this example checks for a visible .form-message inside modals and opens the modal.
  if (signupModal && signupModal.querySelector('.form-message')) {
    openModal(signupModal);
  }
  if (signinModal && signinModal.querySelector('.form-message')) {
    openModal(signinModal);
  }

  // Accessibility: close modal on ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeAll();
  });
});
