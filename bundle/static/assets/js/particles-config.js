$(".hero-particle").each(function() {
  particlesJS($(this).attr('id'), {
    "particles": {
      "number": {
        "value": 3,
        "density": {
          "enable": true,
          "value_area": 1000
        }
      },
      "shape": {
        "type": ["image2", "image3", "image4", "image5", "image6"],
        "stroke": {
          "width": 0,
          "color": "#000000"
        },
        "image": {
          "src": "assets/img/theme-img/particle_1.png",
        },
      },
      "opacity": {
        "value": 0.5,
        "random": false,
        "anim": {
          "enable": true,
          "speed": 2,
          "opacity_min": 0.1,
          "sync": false
        }
      },
      "size": {
        "value": 8,
        "random": false,
        "anim": {
          "enable": false,
          "speed": 5,
          "size_min": 8,
          "sync": true
        }
      },
      "line_linked": {
        "enable": false,
      },
      "move": {
        "enable": true,
        "speed": 15,
        "direction": "none",
        "random": false,
        "straight": false,
        "out_mode": "bounce",
        "bounce": true,
        "attract": {
          "enable": false,
          "rotateX": 1200,
          "rotateY": 10000
        }
      }
    },
    "interactivity": {
      "detect_on": "canvas",
      "events": {
        "onhover": {
          "enable": true,
          "mode": "bubble"
        },
        "onclick": {
          "enable": true,
          "mode": "push"
        },
        "resize": true
      },
      "modes": {
        "bubble": {
          "distance": 300,
          "size": 8.2,
          "duration": 0.1,
          "opacity": 8,
          "speed": 80
        },
        "repulse": {
          "distance": 100,
          "duration": 1,
        },
        "push": {
          "particles_nb": 2
        },
        "remove": {
          "particles_nb": 4
        }
      }
    },
  })
});