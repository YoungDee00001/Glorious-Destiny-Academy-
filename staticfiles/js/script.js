document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert.fade-out");
  alerts.forEach(function(alert) {
    setTimeout(() => {
      alert.classList.add("hide");
      setTimeout(() => {
        alert.style.display = "none";
      }, 1000); // wait for transition to end
    }, 3000); // display for 3 seconds
  });
});


//  Preloader and Back to Top JS
window.addEventListener('load', () => {
    document.getElementById('preloader').style.display = 'none';
});

const backToTop = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
    if (
    document.body.scrollTop > 100 ||
    document.documentElement.scrollTop > 100
    ) {
    backToTop.style.display = 'block';
    } else {
    backToTop.style.display = 'none';
    }
});

backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});