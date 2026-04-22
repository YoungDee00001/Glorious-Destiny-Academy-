
  // const infoTrack = document.getElementById("infoTrack");
  // const totalPanels = infoTrack.children.length;
  // let currentPanel = 0;

  // function updatePanel() {
  //   infoTrack.style.transform = `translateX(-${currentPanel * 100}%)`;
  // }


  // function nextSlide() {
  //   currentPanel = (currentPanel + 1) % totalPanels;
  //   updatePanel();
  // }

  // function prevSlide() {
  //   currentPanel = (currentPanel - 1 + totalPanels) % totalPanels;
  //   updatePanel();
  // }

  // setInterval(nextSlide, 4000); // Auto-slide every 1 seconds


  // let counter = 1;

  // setInterval(() => {
  //   document.getElementById('slide' + counter).checked = true;
  //   counter++;
  //   if (counter > 3) {
  //     counter = 1;
  //   }
  // }, 4000); // Change slide every 1 seconds


    function toggleSidebar() {
      const sidebar = document.getElementById("sidebar");
      const mainContent = document.getElementById("main-content");
      sidebar.classList.toggle("active");
      mainContent.classList.toggle("shift");
    }

    function toggleDropdown(element) {
      element.classList.toggle("open");
    }




    // const sliderTrack = document.getElementById('sliderTrack');
    // let cards = sliderTrack.children;
    // let cardWidth = cards[0].offsetWidth + 20; // 20px includes margin

    // function slideCards() {
    //   // Slide left
    //   sliderTrack.style.transition = 'transform 0.5s ease-in-out';
    //   sliderTrack.style.transform = `translateX(-${cardWidth}px)`;

    //   // After animation
    //   setTimeout(() => {
    //     // Move first card to the end
    //     sliderTrack.appendChild(cards[0]);

    //     // Remove transition and reset position
    //     sliderTrack.style.transition = 'none';
    //     sliderTrack.style.transform = 'translateX(0)';
    //   }, 500);
    // }

    // setInterval(slideCards, 4000); // Slide every 3 seconds

  





