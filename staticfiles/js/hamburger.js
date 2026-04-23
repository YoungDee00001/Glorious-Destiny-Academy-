
function toggleMenu() {
  const hamburger = document.querySelector(".hamburger");
  const menu = document.getElementById("sideMenu");

  hamburger.classList.toggle("active");

  menu.style.display = (menu.style.display === "flex") ? "none" : "flex";
}