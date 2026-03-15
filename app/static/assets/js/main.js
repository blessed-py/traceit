(function ($) {
    "use strict";
    /*=================================
        JS Index Here
    ==================================*/
    /*
    01. On Load Function
    02. Preloader
    03. Mobile Menu
    04. Sticky fix
    05. Scroll To Top
    06. Set Background Image Color & Mask
    07. Global Slider
    08. Ajax Contact Form
    09. Search Box Popup
    10. Popup Sidemenu
    11. Magnific Popup
    12. Section Position
    13. Filter
    14. Counter Up
    15. Shape Mockup
    16. Progress Bar Animation
    17. Countdown
    18. Image to SVG Code
    00. Woocommerce Toggle
    00. Color Scheme
    00. Right Click Disable
    */
    /*=================================
        JS Index End
    ==================================*/
    /*

  /*---------- 01. On Load Function ----------*/
    $(window).on("load", function () {
        $(".preloader").fadeOut();
    });

    /*---------- 02. Preloader ----------*/
    if ($(".preloader").length > 0) {
        $(".preloaderCls").each(function () {
            $(this).on("click", function (e) {
                e.preventDefault();
                $(".preloader").css("display", "none");
            });
        });
    }

    /*---------- 03. Mobile Menu ----------*/
    $.fn.thmobilemenu = function (options) {
        var opt = $.extend(
            {
                menuToggleBtn: ".th-menu-toggle",
                bodyToggleClass: "th-body-visible",
                subMenuClass: "th-submenu",
                subMenuParent: "menu-item-has-children",
                thSubMenuParent: "th-item-has-children",
                subMenuParentToggle: "th-active",
                meanExpandClass: "th-mean-expand",
                appendElement: '<span class="th-mean-expand"></span>',
                subMenuToggleClass: "th-open",
                toggleSpeed: 400,
            },
            options
        );

        return this.each(function () {
            var menu = $(this); // Select menu

            // Menu Show & Hide
            function menuToggle() {
                menu.toggleClass(opt.bodyToggleClass);

                // collapse submenu on menu hide or show
                var subMenu = "." + opt.subMenuClass;
                $(subMenu).each(function () {
                    if ($(this).hasClass(opt.subMenuToggleClass)) {
                        $(this).removeClass(opt.subMenuToggleClass);
                        $(this).css("display", "none");
                        $(this).parent().removeClass(opt.subMenuParentToggle);
                    }
                });
            }

            // Class Set Up for every submenu
            menu.find("." + opt.subMenuParent).each(function () {
                var submenu = $(this).find("ul");
                submenu.addClass(opt.subMenuClass);
                submenu.css("display", "none");
                $(this).addClass(opt.subMenuParent);
                $(this).addClass(opt.thSubMenuParent); // Add th-item-has-children class
                $(this).children("a").append(opt.appendElement);
            });

            // Toggle Submenu
            function toggleDropDown($element) {
                var submenu = $element.children("ul");
                if (submenu.length > 0) {
                    $element.toggleClass(opt.subMenuParentToggle);
                    submenu.slideToggle(opt.toggleSpeed);
                    submenu.toggleClass(opt.subMenuToggleClass);
                }
            }

            // Submenu toggle Button
            var itemHasChildren = "." + opt.thSubMenuParent + " > a";
            $(itemHasChildren).each(function () {
                $(this).on("click", function (e) {
                    e.preventDefault();
                    toggleDropDown($(this).parent());
                });
            });

            // Menu Show & Hide On Toggle Btn click
            $(opt.menuToggleBtn).each(function () {
                $(this).on("click", function () {
                    menuToggle();
                });
            });

            // Hide Menu On outside click
            menu.on("click", function (e) {
                e.stopPropagation();
                menuToggle();
            });

            // Stop Hide full menu on menu click
            menu.find("div").on("click", function (e) {
                e.stopPropagation();
            });
        });
    };

      $(".th-menu-wrapper").thmobilemenu();

    //--------------------- Style-2
    $.fn.thmobilemenu2 = function (options) {
        var opt = $.extend(
            {
                menuToggleBtn: ".th-menu-toggle2",
                bodyToggleClass: "th-body-visible2",
                subMenuClass: "th-submenu2",
                subMenuParent: "menu-item-has-children2",
                thSubMenuParent: "th-item-has-children2",
                subMenuParentToggle: "th-active2",
                meanExpandClass: "th-mean-expand2",
                appendElement: '<span class="th-mean-expand-2"></span>',
                subMenuToggleClass: "th-open2",
                toggleSpeed: 400,
            },
            options
        );

        return this.each(function () {
            var menu = $(this); // Select menu

            // Menu Show & Hide
            function menuToggle() {
                menu.toggleClass(opt.bodyToggleClass);

                // collapse submenu on menu hide or show
                var subMenu = "." + opt.subMenuClass;
                $(subMenu).each(function () {
                    if ($(this).hasClass(opt.subMenuToggleClass)) {
                        $(this).removeClass(opt.subMenuToggleClass);
                        $(this).css("display", "none");
                        $(this).parent().removeClass(opt.subMenuParentToggle);
                    }
                });
            }

            // Class Set Up for every submenu
            menu.find("." + opt.subMenuParent).each(function () {
                var submenu = $(this).find("ul");
                submenu.addClass(opt.subMenuClass);
                submenu.css("display", "none");
                $(this).addClass(opt.subMenuParent);
                $(this).addClass(opt.thSubMenuParent); // Add th-item-has-children class
                $(this).children("a").append(opt.appendElement);
            });

            // Toggle Submenu
            function toggleDropDown($element) {
                var submenu = $element.children("ul");
                if (submenu.length > 0) {
                    $element.toggleClass(opt.subMenuParentToggle);
                    submenu.slideToggle(opt.toggleSpeed);
                    submenu.toggleClass(opt.subMenuToggleClass);
                }
            }

            // Submenu toggle Button
            var itemHasChildren = "." + opt.thSubMenuParent + " > a";
            $(itemHasChildren).each(function () {
                $(this).on("click", function (e) {
                    e.preventDefault();
                    toggleDropDown($(this).parent());
                });
            });

            // Menu Show & Hide On Toggle Btn click
            $(opt.menuToggleBtn).each(function () {
                $(this).on("click", function () {
                    menuToggle();
                });
            });

            // Hide Menu On outside click
            menu.on("click", function (e) {
                e.stopPropagation();
                menuToggle();
            });

            // Stop Hide full menu on menu click
            menu.find("div").on("click", function (e) {
                e.stopPropagation();
            });
        });
    };

    $(".th-menu-wrapper2").thmobilemenu2();


    /*---------- 04. Sticky fix ----------*/
    $(window).scroll(function () {
        var topPos = $(this).scrollTop();
        if (topPos > 1000) {
            $(".sticky-wrapper").addClass("sticky");
            $(".category-menu").addClass("close-category");
        } else {
            $(".sticky-wrapper").removeClass("sticky");
            $(".category-menu").removeClass("close-category");
        }
    });

    $(".menu-expand").each(function () {
        $(this).on("click", function (e) {
            e.preventDefault();
            $(".category-menu").toggleClass("open-category");
        });
    });

    /*----------- One Page Nav ----------*/
    function onePageNav(element) {
        if ($(element).length > 0) {
            $(element).each(function () {
                var link = $(this).find("a");
                $(this)
                    .find(link)
                    .each(function () {
                        $(this).on("click", function () {
                            var target = $(this.getAttribute("href"));
                            if (target.length) {
                                event.preventDefault();
                                $("html, body")
                                    .stop()
                                    .animate(
                                        {
                                            scrollTop: target.offset().top - 10,
                                        },
                                        1000
                                    );
                            }
                        });
                    });
            });
        }
    }
    onePageNav(".onepage-nav");
    onePageNav(".scroll-down");

    /*---------- 05. Scroll To Top ----------*/
    if ($(".scroll-top").length > 0) {
        var scrollTopbtn = document.querySelector(".scroll-top");
        var progressPath = document.querySelector(".scroll-top path");
        var pathLength = progressPath.getTotalLength();
        progressPath.style.transition = progressPath.style.WebkitTransition =
            "none";
        progressPath.style.strokeDasharray = pathLength + " " + pathLength;
        progressPath.style.strokeDashoffset = pathLength;
        progressPath.getBoundingClientRect();
        progressPath.style.transition = progressPath.style.WebkitTransition =
            "stroke-dashoffset 10ms linear";
        var updateProgress = function () {
            var scroll = $(window).scrollTop();
            var height = $(document).height() - $(window).height();
            var progress = pathLength - (scroll * pathLength) / height;
            progressPath.style.strokeDashoffset = progress;
        };
        updateProgress();
        $(window).scroll(updateProgress);
        var offset = 50;
        var duration = 750;
        jQuery(window).on("scroll", function () {
            if (jQuery(this).scrollTop() > offset) {
                jQuery(scrollTopbtn).addClass("show");
            } else {
                jQuery(scrollTopbtn).removeClass("show");
            }
        });
        jQuery(scrollTopbtn).on("click", function (event) {
            event.preventDefault();
            jQuery("html, body").animate({ scrollTop: 0 }, duration);
            return false;
        });
    }

    /*---------- 06. Set Background Image Color & Mask ----------*/
    if ($("[data-bg-src]").length > 0) {
        $("[data-bg-src]").each(function () {
            var src = $(this).attr("data-bg-src");
            $(this).css("background-image", "url(" + src + ")");
            $(this).removeAttr("data-bg-src").addClass("background-image");
        });
    }

    if ($("[data-bg-color]").length > 0) {
        $("[data-bg-color]").each(function () {
            var color = $(this).attr("data-bg-color");
            $(this).css("background-color", color);
            $(this).removeAttr("data-bg-color");
        });
    }

    if ($("[data-theme-color]").length > 0) {
        $("[data-theme-color]").each(function () {
            var $color = $(this).attr("data-theme-color");
            $(this).get(0).style.setProperty("--theme-color", $color);
            $(this).removeAttr("data-theme-color");
        });
    }

    $("[data-border]").each(function () {
        var borderColor = $(this).data("border");
        $(this).css("--th-border-color", borderColor);
    });

    if ($("[data-mask-src]").length > 0) {
        $("[data-mask-src]").each(function () {
            var mask = $(this).attr("data-mask-src");
            $(this).css({
                "mask-image": "url(" + mask + ")",
                "-webkit-mask-image": "url(" + mask + ")",
            });
            $(this).addClass("bg-mask");
            $(this).removeAttr("data-mask-src");
        });
    }

    /*----------- 07. Global Slider ----------*/
    $(".th-slider").each(function () {
        var thSlider = $(this);
        var settings = $(this).data("slider-options") || {};

        // Store references to the navigation buttons
        var prevArrow = thSlider.find(".slider-prev");
        var nextArrow = thSlider.find(".slider-next");
        var paginationEl1 = thSlider.find(".slider-pagination").get(0);
        var paginationEl2 = thSlider.find(".slider-pagination2");
        var progressBarEl = thSlider.find(
            ".slider-pagination-progressbar2 .slider-progressbar-fill"
        );

        var sliderDefault = {
            slidesPerView: 1,
            spaceBetween: settings.spaceBetween || 24,
            loop: settings.loop !== false,
            speed: settings.speed || 1000,
            autoplay: settings.autoplay || {
                delay: 6000,
                disableOnInteraction: false,
            },
            navigation: {
                prevEl: prevArrow.get(0),
                nextEl: nextArrow.get(0),
            },
            pagination: {
                el: paginationEl1,
                type: settings.paginationType || "bullets",
                clickable: true,
                renderBullet: function (index, className) {
                    var number = index + 1;
                    var formattedNumber = number < 10 ? "0" + number : number;
                    return (
                        '<span class="' +
                        className +
                        '" aria-label="Go to Slide ' +
                        formattedNumber +
                        '"></span>'
                    );
                },
            },
            on: {
                init: function () {
                    updatePagination(this);
                    updateProgressBar(this);
                },
                slideChange: function () {
                    updatePagination(this);
                    updateProgressBar(this);
                },
            },
        };

        var options = $.extend({}, sliderDefault, settings);
        var swiperInstance = new Swiper(thSlider.get(0), options);

        // Update Pagination and other UI elements
        function updatePagination(swiper) {
            var activeIndex = swiper.realIndex + 1;
            var totalSlides = swiper.slides.length;
            paginationEl2.html(
                '<span class="current-slide">' +
                    (activeIndex < 10 ? "0" + activeIndex : activeIndex) +
                    '</span> <span class="divider">/</span> <span class="total-slides">' +
                    (totalSlides < 10 ? "0" + totalSlides : totalSlides) +
                    "</span>"
            );
        }

        function updateProgressBar(swiper) {
            var progress =
                ((swiper.realIndex + 1) / swiper.slides.length) * 100;
            progressBarEl.css("height", progress + "%");
        }

        if ($(".slider-area").length > 0) {
            $(".slider-area")
                .closest(".container")
                .parent()
                .addClass("arrow-wrap");
        }

        // Tab Button Slider Integration
        $(".tab-btn").on("click", function () {
            var index = $(this).index();
            $(".tab-btn").removeClass("active");
            $(this).addClass("active");
            swiper.slideTo(index);
        });
    });

    // Function to add animation classes
    function animationProperties() {
        $("[data-ani]").each(function () {
            var animationName = $(this).data("ani");
            $(this).addClass(animationName);
        });

        $("[data-ani-delay]").each(function () {
            var delayTime = $(this).data("ani-delay");
            $(this).css("animation-delay", delayTime);
        });
    }
    animationProperties();

    // Add click event handlers for external slider arrows based on data attributes
    $("[data-slider-prev], [data-slider-next]").on("click", function () {
        var sliderSelector =
            $(this).data("slider-prev") || $(this).data("slider-next");
        var targetSlider = $(sliderSelector);

        if (targetSlider.length) {
            var swiper = targetSlider[0].swiper;

            if (swiper) {
                if ($(this).data("slider-prev")) {
                    swiper.slidePrev();
                } else {
                    navigator, swiper.slideNext();
                }
            }
        }
    });

    /*----------- 08. Ajax Contact Form ----------*/
    var form = ".ajax-contact";
    var invalidCls = "is-invalid";
    var $email = '[name="email"]';
    var $validation =
        '[name="name"],[name="email"],[name="subject"],[name="number"],[name="message"]'; // Must be use (,) without any space
    var formMessages = $(".form-messages");

    function sendContact() {
        var formData = $(form).serialize();
        var valid;
        valid = validateContact();
        if (valid) {
            jQuery
                .ajax({
                    url: $(form).attr("action"),
                    data: formData,
                    type: "POST",
                })
                .done(function (response) {
                    // Make sure that the formMessages div has the 'success' class.
                    formMessages.removeClass("error");
                    formMessages.addClass("success");
                    // Set the message text.
                    formMessages.text(response);
                    // Clear the form.
                    $(
                        form +
                            ' input:not([type="submit"]),' +
                            form +
                            " textarea"
                    ).val("");
                })
                .fail(function (data) {
                    // Make sure that the formMessages div has the 'error' class.
                    formMessages.removeClass("success");
                    formMessages.addClass("error");
                    // Set the message text.
                    if (data.responseText !== "") {
                        formMessages.html(data.responseText);
                    } else {
                        formMessages.html(
                            "Oops! An error occured and your message could not be sent."
                        );
                    }
                });
        }
    }

    function validateContact() {
        var valid = true;
        var formInput;

        function unvalid($validation) {
            $validation = $validation.split(",");
            for (var i = 0; i < $validation.length; i++) {
                formInput = form + " " + $validation[i];
                if (!$(formInput).val()) {
                    $(formInput).addClass(invalidCls);
                    valid = false;
                } else {
                    $(formInput).removeClass(invalidCls);
                    valid = true;
                }
            }
        }
        unvalid($validation);

        if (
            !$($email).val() ||
            !$($email)
                .val()
                .match(/^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/)
        ) {
            $($email).addClass(invalidCls);
            valid = false;
        } else {
            $($email).removeClass(invalidCls);
            valid = true;
        }
        return valid;
    }

    $(form).on("submit", function (element) {
        element.preventDefault();
        sendContact();
    });

    /*---------- 09. Search Box Popup ----------*/
    function popupSarchBox($searchBox, $searchOpen, $searchCls, $toggleCls) {
        $($searchOpen).on("click", function (e) {
            e.preventDefault();
            $($searchBox).addClass($toggleCls);
        });
        $($searchBox).on("click", function (e) {
            e.stopPropagation();
            $($searchBox).removeClass($toggleCls);
        });
        $($searchBox)
            .find("form")
            .on("click", function (e) {
                e.stopPropagation();
                $($searchBox).addClass($toggleCls);
            });
        $($searchCls).on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            $($searchBox).removeClass($toggleCls);
        });
    }
    popupSarchBox(
        ".popup-search-box",
        ".searchBoxToggler",
        ".searchClose",
        "show"
    );

    /*---------- 10. Popup Sidemenu ----------*/
    function popupSideMenu($sideMenu, $sideMunuOpen, $sideMenuCls, $toggleCls) {
        // Sidebar Popup
        $($sideMunuOpen).on("click", function (e) {
            e.preventDefault();
            $($sideMenu).addClass($toggleCls);
        });
        $($sideMenu).on("click", function (e) {
            e.stopPropagation();
            $($sideMenu).removeClass($toggleCls);
        });
        var sideMenuChild = $sideMenu + " > div";
        $(sideMenuChild).on("click", function (e) {
            e.stopPropagation();
            $($sideMenu).addClass($toggleCls);
        });
        $($sideMenuCls).on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            $($sideMenu).removeClass($toggleCls);
        });
    }
    popupSideMenu(".sidemenu-cart", ".sideMenuToggler", ".sideMenuCls", "show");
    popupSideMenu(".sidemenu-info", ".sideMenuInfo", ".sideMenuCls", "show");

    /*----------- 11. Magnific Popup ----------*/
    /* magnificPopup img view */
    $(".th-popup-image").magnificPopup({
        type: "image",
        mainClass: "mfp-zoom-in",
        removalDelay: 260,
        gallery: {
            enabled: true,
        },
        image: {
            tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
            titleSrc: function (item) {
                return item.el.attr("title");
            },
        },
    });

    /* magnificPopup video view */
    $(".th-popup-video").magnificPopup({
        type: "iframe",
        mainClass: "mfp-zoom-in",
    });

    /* magnificPopup video view */
    $(".th-popup-content").magnificPopup({
        type: "inline",
        midClick: true,
    });

    /*---------- 12. Section Position ----------*/
    // Interger Converter
    function convertInteger(str) {
        return parseInt(str, 10);
    }

    $.fn.sectionPosition = function (mainAttr, posAttr) {
        $(this).each(function () {
            var section = $(this);

            function setPosition() {
                var sectionHeight = Math.floor(section.height() / 2), // Main Height of section
                    posData = section.attr(mainAttr), // where to position
                    posFor = section.attr(posAttr), // On Which section is for positioning
                    topMark = "top-half", // Pos top
                    bottomMark = "bottom-half", // Pos Bottom
                    parentPT = convertInteger($(posFor).css("padding-top")), // Default Padding of  parent
                    parentPB = convertInteger($(posFor).css("padding-bottom")); // Default Padding of  parent

                if (posData === topMark) {
                    $(posFor).css(
                        "padding-bottom",
                        parentPB + sectionHeight + "px"
                    );
                    section.css("margin-top", "-" + sectionHeight + "px");
                } else if (posData === bottomMark) {
                    $(posFor).css(
                        "padding-top",
                        parentPT + sectionHeight + "px"
                    );
                    section.css("margin-bottom", "-" + sectionHeight + "px");
                }
            }
            setPosition(); // Set Padding On Load
        });
    };

    var postionHandler = "[data-sec-pos]";
    if ($(postionHandler).length) {
        $(postionHandler).imagesLoaded(function () {
            $(postionHandler).sectionPosition("data-sec-pos", "data-pos-for");
        });
    }

    /*----------- 14. Filter ----------*/
    $(".filter-active").imagesLoaded(function () {
        var $filter = ".filter-active",
            $filterItem = ".filter-item",
            $filterMenu = ".filter-menu-active";

        if ($($filter).length > 0) {
            var $grid = $($filter).isotope({
                itemSelector: $filterItem,
                filter: "*",
                masonry: {
                    // use outer width of grid-sizer for columnWidth
                    // columnWidth: 1,
                },
            });

            // filter items on button click
            $($filterMenu).on("click", "button", function () {
                var filterValue = $(this).attr("data-filter");
                $grid.isotope({
                    filter: filterValue,
                });
            });

            // Menu Active Class
            $($filterMenu).on("click", "button", function (event) {
                event.preventDefault();
                $(this).addClass("active");
                $(this).siblings(".active").removeClass("active");
            });
        }
    });

    $(".masonary-active, .woocommerce-Reviews .comment-list").imagesLoaded(
        function () {
            var $filter =
                    ".masonary-active, .woocommerce-Reviews .comment-list",
                $filterItem =
                    ".filter-item, .woocommerce-Reviews .comment-list li";

            if ($($filter).length > 0) {
                $($filter).isotope({
                    itemSelector: $filterItem,
                    filter: "*",
                    masonry: {
                        // use outer width of grid-sizer for columnWidth
                        columnWidth: 1,
                    },
                });
            }
            $('[data-bs-toggle="tab"]').on("shown.bs.tab", function (e) {
                $($filter).isotope({
                    filter: "*",
                });
            });
        }
    );

    /*----------- 14. Counter Up ----------*/
    $(".counter-number").counterUp({
        delay: 10,
        time: 1000,
    });

    /*----------- 15. Shape Mockup ----------*/
    $.fn.shapeMockup = function () {
        var $shape = $(this);
        $shape.each(function () {
            var $currentShape = $(this),
                shapeTop = $currentShape.data("top"),
                shapeRight = $currentShape.data("right"),
                shapeBottom = $currentShape.data("bottom"),
                shapeLeft = $currentShape.data("left");
            $currentShape
                .css({
                    top: shapeTop,
                    right: shapeRight,
                    bottom: shapeBottom,
                    left: shapeLeft,
                })
                .removeAttr("data-top")
                .removeAttr("data-right")
                .removeAttr("data-bottom")
                .removeAttr("data-left")
                .parent()
                .addClass("shape-mockup-wrap");
        });
    };

    if ($(".shape-mockup")) {
        $(".shape-mockup").shapeMockup();
    }

    /*----------- 16. Progress Bar Animation ----------*/
    $(".progress-bar").waypoint(
        function () {
            $(".progress-bar").css({
                animation: "animate-positive 1.8s",
                opacity: "1",
            });
        },
        { offset: "100%" }
    );

    /*---------- 18. Image to SVG Code ----------*/
    const cache = {};

    $.fn.inlineSvg = function fnInlineSvg() {
        this.each(imgToSvg);

        return this;
    };

    function imgToSvg() {
        const $img = $(this);
        const src = $img.attr("src");

        // fill cache by src with promise
        if (!cache[src]) {
            const d = $.Deferred();
            $.get(src, (data) => {
                d.resolve($(data).find("svg"));
            });
            cache[src] = d.promise();
        }

        // replace img with svg when cached promise resolves
        cache[src].then((svg) => {
            const $svg = $(svg).clone();

            if ($img.attr("id")) $svg.attr("id", $img.attr("id"));
            if ($img.attr("class")) $svg.attr("class", $img.attr("class"));
            if ($img.attr("style")) $svg.attr("style", $img.attr("style"));

            if ($img.attr("width")) {
                $svg.attr("width", $img.attr("width"));
                if (!$img.attr("height")) $svg.removeAttr("height");
            }
            if ($img.attr("height")) {
                $svg.attr("height", $img.attr("height"));
                if (!$img.attr("width")) $svg.removeAttr("width");
            }

            $svg.insertAfter($img);
            $img.trigger("svgInlined", $svg[0]);
            $img.remove();
        });
    }

    $(".svg-img").inlineSvg();

    /*---------- 19. Circle Progress ----------*/
    document.addEventListener("DOMContentLoaded", function () {
        const progressBars = document.querySelectorAll(".circular-progress");

        progressBars.forEach((progressBar) => {
            const circle = progressBar.querySelector(".circle");
            const percentageDisplay = progressBar.querySelector(".percentage");
            const target = parseInt(
                progressBar.getAttribute("data-target"),
                10
            );
            let progressValue = 0;

            const animateProgress = () => {
                if (progressValue <= target) {
                    const offset = 100 - (progressValue * 100) / 100;
                    circle.style.strokeDashoffset = offset;
                    percentageDisplay.textContent = progressValue + "%";
                    progressValue++;
                    requestAnimationFrame(animateProgress);
                }
            };

            animateProgress();
        });
    });

    /*----------- 00. Woocommerce Toggle ----------*/
    // Ship To Different Address
    $(document).on(
        "change",
        "#ship-to-different-address-checkbox",
        function () {
            const $shippingAddress = $("#ship-to-different-address").next(
                ".shipping_address"
            );
            $(this).is(":checked")
                ? $shippingAddress.slideDown()
                : $shippingAddress.slideUp();
        }
    );

    // Login Toggle
    $(document).on("click", ".woocommerce-form-login-toggle a", function (e) {
        e.preventDefault();
        $(".woocommerce-form-login").slideToggle();
    });

    // Coupon Toggle
    $(document).on("click", ".woocommerce-form-coupon-toggle a", function (e) {
        e.preventDefault();
        $(".woocommerce-form-coupon").slideToggle();
    });

    // Shipping Calculator Toggle
    $(document).on("click", ".shipping-calculator-button", function (e) {
        e.preventDefault();
        $(this).next(".shipping-calculator-form").slideToggle();
    });

    // Payment Method Toggle
    $(".wc_payment_methods input[type='radio']:checked")
        .siblings(".payment_box")
        .show();

    $(document).on(
        "change",
        ".wc_payment_methods input[type='radio']",
        function () {
            $(".payment_box").slideUp();
            $(this).siblings(".payment_box").slideDown();
        }
    );

    // Rating Stars Toggle
    $(document).on("click", ".rating-select .stars a", function (e) {
        e.preventDefault();
        $(this).siblings().removeClass("active");
        $(this).parent().parent().addClass("selected");
        $(this).addClass("active");
    });

    // Quantity Plus Minus ---------------------------
    $(document).on("click", ".quantity-plus", function (e) {
        e.preventDefault();
        const $qty = $(this).siblings(".qty-input");
        const currentVal = parseInt($qty.val(), 10); // radix specified
        if (!isNaN(currentVal)) {
            $qty.val(currentVal + 1);
        }
    });

    $(document).on("click", ".quantity-minus", function (e) {
        e.preventDefault();
        const $qty = $(this).siblings(".qty-input");
        const currentVal = parseInt($qty.val(), 10); // radix specified
        if (!isNaN(currentVal) && currentVal > 1) {
            $qty.val(currentVal - 1);
        }
    });

    // /*----------- 00.Color Scheme ----------*/
    $(".color-switch-btns button").each(function () {
        // Get color for button
        const button = $(this);
        const color = button.data("color");
        button.css("--theme-color", color);

        // Change theme color on click
        button.on("click", function () {
            const clickedColor = $(this).data("color");
            $(":root").css("--theme-color", clickedColor);
        });
    });

    $(document).on("click", ".switchIcon", function () {
        $(".color-scheme-wrap").toggleClass("active");
    });

    // /*----------- lettering js ----------*/
    function injector(t, splitter, klass, after) {
        var a = t.text().split(splitter),
            inject = "";
        if (a.length) {
            $(a).each(function (i, item) {
                inject +=
                    '<span class="' +
                    klass +
                    (i + 1) +
                    '">' +
                    item +
                    "</span>" +
                    after;
            });
            t.empty().append(inject);
        }
    }

    var methods = {
        init: function () {
            return this.each(function () {
                injector($(this), "", "char", "");
            });
        },

        words: function () {
            return this.each(function () {
                injector($(this), " ", "word", " ");
            });
        },

        lines: function () {
            return this.each(function () {
                var r = "eefec303079ad17405c889e092e105b0";
                // Because it's hard to split a <br/> tag consistently across browsers,
                // (*ahem* IE *ahem*), we replaces all <br/> instances with an md5 hash
                // (of the word "split").  If you're trying to use this plugin on that
                // md5 hash string, it will fail because you're being ridiculous.
                injector(
                    $(this).children("br").replaceWith(r).end(),
                    r,
                    "line",
                    ""
                );
            });
        },
    };

    $.fn.lettering = function (method) {
        // Method calling logic
        if (method && methods[method]) {
            return methods[method].apply(this, [].slice.call(arguments, 1));
        } else if (method === "letters" || !method) {
            return methods.init.apply(this, [].slice.call(arguments, 0)); // always pass an array
        }
        $.error("Method " + method + " does not exist on jQuery.lettering");
        return this;
    };
    $(".circle-title-anime").lettering();

    /*----------- image Slider ----------*/
    $("#slider").on("input change", (e) => {
        const sliderPos = e.target.value;
        // Update the width of the foreground image
        $(".foreground-img").css("width", `${sliderPos}%`);
        // Update the position of the slider button
        $(".slider-button").css("left", `calc(${sliderPos}% - 43px)`);
    });

    // ---------- Smooth Scroll ----------
    gsap.registerPlugin(ScrollTrigger);

    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (!prefersReducedMotion) {
        const lenis = new Lenis({
            lerp: 0.07,
        });

        lenis.on("scroll", ScrollTrigger.update);

        gsap.ticker.add((time) => {
            lenis.raf(time * 1000);
        });

        document.querySelectorAll(".allow-natural-scroll").forEach((el) => {
            el.addEventListener("wheel", (e) => e.stopPropagation(), {
                passive: true,
            });
            el.addEventListener("touchmove", (e) => e.stopPropagation(), {
                passive: true,
            });
        });
    }

    // ---------- GSAP Text Animation ----------
    function animateText(selector, config) {
        const elements = document.querySelectorAll(selector);
        if (!elements.length) return;

        elements.forEach((el) => {
            const split = new SplitText(el, { type: "chars, words" });
            gsap.from(split.chars, {
                duration: config.duration,
                delay: config.delay,
                x: config.x,
                autoAlpha: 0,
                stagger: config.stagger,
                ease: config.ease,
                scrollTrigger: {
                    trigger: el,
                    start: "top 85%",
                },
            });
        });
    }

    animateText(".text-anim", {
        duration: 1,
        delay: 0.5,
        x: 20,
        stagger: 0.05,
        ease: "power2.out",
    });

    animateText(".text-anim2", {
        duration: 1,
        delay: 0.1,
        x: 20,
        stagger: 0.03,
        ease: "power2.out",
    });

    /*---------- Hover Item Active Class ----------*/
    $(document).on("mouseover", ".hover-item", function () {
        $(this)
            .addClass("item-active")
            .siblings(".hover-item")
            .removeClass("item-active");
    });

    /*----------- Price Slider ----------*/
    $(".price_slider").slider({
        range: true,
        min: 0,
        max: 350,
        values: [0, 350],
        slide: function (event, ui) {
            $(".from").text("$" + ui.values[0]);
            $(".to").text("$" + ui.values[1]);
        },
    });
    $(".from").text("$" + $(".price_slider").slider("values", 0));
    $(".to").text("$" + $(".price_slider").slider("values", 1));

    $(document).ready(function () {
        // process-2-list-wrap add & remove active class
        $(document).on("click", ".process-card2", function () {
            $(this).addClass("active").siblings().removeClass("active");
        });
    });

    /*----------- 18. Countdown ----------*/

    $.fn.countdown = function () {
        $(this).each(function () {
            var $counter = $(this),
                countDownDate = new Date($counter.data("offer-date")).getTime(), // Set the date we're counting down toz
                exprireCls = "expired";

            // Finding Function
            function s$(element) {
                return $counter.find(element);
            }

            // Update the count down every 1 second
            var counter = setInterval(function () {
                // Get today's date and time
                var now = new Date().getTime();

                // Find the distance between now and the count down date
                var distance = countDownDate - now;

                // Time calculations for days, hours, minutes and seconds
                var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                var hours = Math.floor(
                    (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
                );
                var minutes = Math.floor(
                    (distance % (1000 * 60 * 60)) / (1000 * 60)
                );
                var seconds = Math.floor((distance % (1000 * 60)) / 1000);

                // Check If value is lower than ten, so add zero before number
                days < 10 ? (days = "0" + days) : null;
                hours < 10 ? (hours = "0" + hours) : null;
                minutes < 10 ? (minutes = "0" + minutes) : null;
                seconds < 10 ? (seconds = "0" + seconds) : null;

                // If the count down is over, write some text
                if (distance < 0) {
                    clearInterval(counter);
                    $counter.addClass(exprireCls);
                    $counter.find(".message").css("display", "block");
                } else {
                    // Output the result in elements
                    s$(".day").html(days);
                    s$(".hour").html(hours);
                    s$(".minute").html(minutes);
                    s$(".seconds").html(seconds);
                }
            }, 1000);
        });
    };

    if ($(".counter-list").length) {
        $(".counter-list").countdown();
    }
    /*----------- 21. Pricing-switch & Tab----------*/
    var e = document.getElementById("filt-monthly"),
        d = document.getElementById("filt-yearly"),
        t = document.getElementById("switcher"),
        m = document.getElementById("monthly"),
        y = document.getElementById("yearly");

    if ($(".pricing-tabs").length) {
        $(document).on("click", "#filt-monthly", function () {
            $("#switcher").prop("checked", false);
            $("#filt-monthly").addClass("toggler--is-active");
            $("#filt-yearly").removeClass("toggler--is-active");
            $("#monthly").removeClass("hide");
            $("#yearly").addClass("hide");
        });

        $(document).on("click", "#filt-yearly", function () {
            $("#switcher").prop("checked", true);
            $("#filt-yearly").addClass("toggler--is-active");
            $("#filt-monthly").removeClass("toggler--is-active");
            $("#monthly").addClass("hide");
            $("#yearly").removeClass("hide");
        });

        $(document).on("click", "#switcher", function () {
            $("#filt-yearly, #filt-monthly").toggleClass("toggler--is-active");
            $("#monthly, #yearly").toggleClass("hide");
        });
    }

    // /*----------- 00. Right Click Disable ----------*/
    //   window.addEventListener('contextmenu', function (e) {
    //     // do something here...
    //     e.preventDefault();
    //   }, false);

    // /*----------- 00. Inspect Element Disable ----------*/
    //   document.onkeydown = function (e) {
    //     if (event.keyCode == 123) {
    //       return false;
    //     }
    //     if (e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)) {
    //       return false;
    //     }
    //     if (e.ctrlKey && e.shiftKey && e.keyCode == 'C'.charCodeAt(0)) {
    //       return false;
    //     }
    //     if (e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)) {
    //       return false;
    //     }
    //     if (e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) {
    //       return false;
    //     }
    //   }
})(jQuery);

// scrollCue
scrollCue.init({
    percentage: 0.99,
    duration: 900,
});



//Mobile menu dropdown

        document.addEventListener('DOMContentLoaded', function() {
            const menuToggle = document.querySelector('.th-menu-toggle');
            const dropdown = document.querySelector('.mobile-menu-dropdown');

            if (menuToggle && dropdown) {
                menuToggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    dropdown.classList.toggle('show');
                    console.log('Menu clicked, dropdown toggled');
                });

                // Close dropdown when clicking outside
                document.addEventListener('click', function(e) {
                    if (!menuToggle.contains(e.target) && !dropdown.contains(e.target)) {
                        dropdown.classList.remove('show');
                    }
                });

                // Close dropdown when clicking on a link
                dropdown.querySelectorAll('a').forEach(link => {
                    link.addEventListener('click', function() {
                        dropdown.classList.remove('show');
                    });
                });
            } else {
                console.log('Menu toggle or dropdown not found');
            }
        });