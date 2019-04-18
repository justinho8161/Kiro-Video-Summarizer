(function($) {
  "use strict"; // Start of use strict

  // Closes the sidebar menu
  $(".menu-toggle").click(function(e) {
    e.preventDefault();
    $("#sidebar-wrapper").toggleClass("active");
    $(".menu-toggle > .fa-bars, .menu-toggle > .fa-times").toggleClass("fa-bars fa-times");
    $(this).toggleClass("active");
  });

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });



//Interactive Video
window.onload = function() {
    // get video element
    var video = document.getElementsByTagName("video")[0];
    var transcript = document.getElementById("transcriptContainer");
    var trans_text = document.getElementById("transcriptText");
    var speaking = document.getElementById("speaking");
    var current = -1;

// register events for the clicks on the text
    var cues = document.getElementsByClassName("cue");
    for (i=0; i<cues.length; i++) {
      cues[i].addEventListener("click", function(evt) {
        var start = parseFloat(this.getAttribute("data-time"));
        video.currentTime = start;
        video.play();
      }, false);
    }

    // pause video as you mouse over transcript
    transcript.addEventListener("mouseover", function(evt) {
      video.pause();
    }, false);


    video.addEventListener("timeupdate", function(evt) {
      if (video.paused || video.ended) {
        return;
      }
      // scroll to currently playing time offset
      for (i=0; i<cues.length; i++) {
        var cueTime = cues[i].getAttribute("data-time");
        if (cues[i].className.indexOf("current") == -1 &&
            video.currentTime >= parseFloat(cueTime) &&
            video.currentTime < parseFloat(cueTime)) {
          trans_text.scrollTop =
            cues[i].offsetTop - trans_text.offsetTop;
          if (current >= 0) {
              cues[current].classList.remove("current");
          }
          cues[i].className += " current";
          current = i;
          if (cues[i].getAttribute("aria-live") == "rude") {
            speaking.innerHTML = cues[i].innerHTML;
          }
        }
      }
    }, false);
};

  //From Materialize input

  $(".mat-input").focus(function(){
    $(this).parent().addClass("is-active is-completed");
  });

  $(".mat-input").focusout(function(){
    if($(this).val() === "")
      $(this).parent().removeClass("is-completed");
    $(this).parent().removeClass("is-active");
  })


  //From Tobias
  // Wrap every letter in a span
  $('.ml12').each(function(){
    $(this).html($(this).text().replace(/([^\x00-\x80]|\w)/g, "<span class='letter'>$&</span>"));
  });

  anime.timeline({loop: true})
    .add({
      targets: '.ml12 .letter',
      translateX: [40,0],
      translateZ: 0,
      opacity: [0,1],
      easing: "easeOutExpo",
      duration: 1200,
      delay: function(el, i) {
        return 500 + 30 * i;
      }
    }).add({
      targets: '.ml12 .letter',
      translateX: [0,-30],
      opacity: [1,0],
      easing: "easeInExpo",
      duration: 1100,
      delay: function(el, i) {
        return 100 + 30 * i;
      }
    });


  // Closes responsive menu when a scroll trigger link is clicked
  $('#sidebar-wrapper .js-scroll-trigger').click(function() {
    $("#sidebar-wrapper").removeClass("active");
    $(".menu-toggle").removeClass("active");
    $(".menu-toggle > .fa-bars, .menu-toggle > .fa-times").toggleClass("fa-bars fa-times");
  });

  // Scroll to top button appear
  $(document).scroll(function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

})(jQuery); // End of use strict

// Disable Google Maps scrolling
// See http://stackoverflow.com/a/25904582/1607849
// Disable scroll zooming and bind back the click event
var onMapMouseleaveHandler = function(event) {
  var that = $(this);
  that.on('click', onMapClickHandler);
  that.off('mouseleave', onMapMouseleaveHandler);
  that.find('iframe').css("pointer-events", "none");
}
var onMapClickHandler = function(event) {
  var that = $(this);
  // Disable the click handler until the user leaves the map area
  that.off('click', onMapClickHandler);
  // Enable scrolling zoom
  that.find('iframe').css("pointer-events", "auto");
  // Handle the mouse leave event
  that.on('mouseleave', onMapMouseleaveHandler);
}
// Enable map zooming with mouse scroll when the user clicks the map
$('.map').on('click', onMapClickHandler);
