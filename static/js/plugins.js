// Avoid `console` errors in browsers that lack a console.
(function () {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }




    var vid = document.getElementById("cvideo"),
        pauseButton = document.getElementById("vbutton");
    vid.playbackRate = 0.8;

    function vidFade() {
        vid.classList.add("stopfade");
    }
    vid.addEventListener('ended', function () {
        vid.pause();
        vidFade();
    });
    pauseButton.addEventListener("click", function () {
        vid.classList.toggle("stopfade");
        if (vid.paused) {
            vid.play();
            pauseButton.innerHTML = '<span class="ti-control-pause" ></span>';
            $('.section-video .section-bg,.section-video-text').addClass("fadeOut animated");
            $('.section-video .section-bg').animate({
                'top': '100%'
            });
            $('.section-video-text').animate({
                'top': '100%'
            });
        } else {
            vid.pause();
            pauseButton.innerHTML = '<span class="ti-control-play" ></span>';
            $('.section-video .section-bg,.section-video-text').removeClass("fadeOut animated");
            $('.section-video .section-bg').animate({
                'top': '0%'
            });
            $('.section-video-text').animate({
                'top': '50%'
            });
        }
    });
    vid.addEventListener("click", function () {
        vid.classList.toggle("stopfade");
        if (vid.paused) {
            vid.play();
            pauseButton.innerHTML = '<span class="ti-control-pause" ></span>';
            $('.section-video .section-bg,.section-video-text').addClass("fadeOut animated");
            $('.section-video .section-bg').animate({
                'top': '100%'
            });
            $('.section-video-text').animate({
                'top': '100%'
            });
        } else {
            vid.pause();
            pauseButton.innerHTML = '<span class="ti-control-play" ></span>';
            $('.section-video .section-bg,.section-video-text').removeClass("fadeOut animated");

            $('.section-video .section-bg').animate({
                'top': '0%'
            });
            $('.section-video-text').animate({
                'top': '50%'
            });
        }
    });
}());

$(window).scroll(function(){
	// Add parallax scrolling to all images in .paralax-image container
	$('.parallax-image').each(function(){
		// only put top value if the window scroll has gone beyond the top of the image
		if ($(this).offset().top < $(window).scrollTop()) {
			// Get ammount of pixels the image is above the top of the window
			var difference = $(window).scrollTop() - $(this).offset().top;
			// Top value of image is set to half the amount scrolled
			// (this gives the illusion of the image scrolling slower than the rest of the page)
			var half = (difference / 2) + 'px';

			$(this).find('img').css('top', half);
		} else {
			// if image is below the top of the window set top to 0
			$(this).find('img').css('top', '0');
		}
	});
});

$(function () {
    $('#mainmenu a[href*="#"]:not([href="#"])').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });
});
// Place any jQuery/helper plugins in here.