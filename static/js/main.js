document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.querySelector('.c-hamburger');
  const headNav = document.querySelector('.p-header__nav');


  if (!hamburger) {
    return false;
  }

  hamburger.addEventListener('click', () => {
    if (hamburger.classList.contains("is-active")) {
      hamburger.classList.remove('is-active');
      headNav.classList.remove('is-active')
    } else {
      hamburger.classList.add('is-active');
      headNav.classList.add('is-active')
    }

  });

  headNav.addEventListener('click', () => {
    hamburger.classList.remove('is-active');
    headNav.classList.remove('is-active')
  });
});
