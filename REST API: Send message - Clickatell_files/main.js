// globals
var didScroll, showCookie, user_is_scrolling;
var lastScrollTop = 0;
var delta 		  = $('#header.small').height();
var navbarHeight  = $('#header.small').outerHeight();


// Get time and date from server NOT client
var serverInfo = {
    'time' : $('.cookie-show').data().currentTime,
    'date' : $('.cookie-show').data().currentDate
};

// Get Cookie info stored in localStorage
if(typeof localStorage.cookiePolicy !== 'undefined') {
    var cookieInfo = {
        'time' : JSON.parse(localStorage.cookiePolicy).timestamp.timeSet,
        'date' : JSON.parse(localStorage.cookiePolicy).timestamp.dateSet
    };
}

// set up moment on date/time objects
var oneWeekLater   = moment(cookieInfo).add(7, 'days').format('LL');
var theCurrentTime = moment(serverInfo).format('LL');

// Events
$(window).load(function() {
    initResize();
    
    // Determine whether or not to show the cookie
    show_cookie = (theCurrentTime === oneWeekLater) ? true : false;
    if(show_cookie || (typeof localStorage.cookiePolicy === 'undefined')) {
        $('.cookie-show').delay( 3000 ).animate({ bottom: 0 });
        setTimeout(function() { $('.cookie-show .glyphicon-remove').click(); }, 7000);
    } else {
        $('.cookie-show').remove();
    }
    if(window.innerWidth < 768) {
        $('#clickatell-main-nav .navbar-toggle').fadeIn('slow');
    }
    
    //Twitter
    window.twttr = (function (d,s,id) {
      var t, js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return; js=d.createElement(s); js.id=id;
      js.src="https://platform.twitter.com/widgets.js"; fjs.parentNode.insertBefore(js, fjs);
      return window.twttr || (t = { _e: [], ready: function(f){ t._e.push(f) } });
    }(document, "script", "twitter-wjs"));
});

$(window).bind('mousewheel', function(event) {
    user_is_scrolling = (event.originalEvent.wheelDelta >= 0) ? 'up' : 'down';
});

$(window).resize(initResize);

function initResize() {
    //Equal height columns (for direct children of all instances of .equal-height-cols)
    if($('.equal-height-cols').length) {
        $('.equal-height-cols').each(function() {
            var tallestH = 0;
            $(this).find('> div').each(function() {
                var colH = $(this).height();
                if(colH > tallestH) tallestH = colH;
            });
            $(this).find('> div').css('height', tallestH+'px');
            
        });
    }
}

$(window).scroll(function(event) {

    didScroll = true;
    //fixed on scroll
    // if($('.pin-on-scroll').length > 0) pinElementToTopOfScreen($('.pin-on-scroll'));
    if($('[data-on-scroll="fixed"]').length > 0 && $(window).width() > 991) {
        pinOnScroll($('[data-on-scroll="fixed"]'));
    };
    
    if($('.single-promotions .promo-form-wrap').length > 0 && $(window).width() > 991) {
        var scrolled = $(window).scrollTop();
        if(scrolled > 253) {
            $('.single-promotions .promo-form-wrap').addClass('scrolled');
        } else{
            $('.single-promotions .promo-form-wrap').removeClass('scrolled');
        }
        
        if(scrolled > ($(document).height()-($('.get-involved').innerHeight()+$('#footer').innerHeight()+$('.slice.pulled-in').innerHeight()+$('.promo-form-wrap').innerHeight()))) {
            $('.single-promotions .promo-form-wrap').addClass('past');
        } else{
            $('.single-promotions .promo-form-wrap').removeClass('past');
        }
    }
});

setInterval(function() {
    if (didScroll) {
        // hasScrolled
        // first argument is the target
        // second is the pages templates to include the feature on
        hasScrolled($('#header.small'), $('#template-blog-landing, #template-blog-category'));
        didScroll = false;
    }
}, 250);

$(document).scroll(function() {
    stickyNav();
});

$(function() {
    if($('#spy').length) {
        $('body').scrollspy({
            target: '#spy',
            offset: $('#spy').height() + 57
        });
    }

	if($('.cookie-show').length > 0) {
        $('.cookie-show').css({
            bottom    : '-400px',
            visibility: 'visible'
        });
	}
    
    // Sharing
    $('.icon-share-fb').click(function(e) {
        e.preventDefault();
        fbShare();
    });
    $('.icon-share-li').click(function(e) {
        e.preventDefault();
        liShare();
    });
    $('.icon-share-tw').attr('href', 'https://twitter.com/intent/tweet?url='+encodeURIComponent($('meta[property="og:url"]').attr('content'))+'&text='+encodeURIComponent($('meta[name="twitter:title"]').attr('content')));
        
    // When the user close timestamp set necessary value accordingly
    $('.cookie-show .glyphicon-remove').click(function () {
        var parent    = $(this).parent();
        var timestamp = { 'timestamp' : {
                'timeSet' : parent.data().currentTime,
                'dateSet' : parent.data().currentDate
            }
        };
        parent.animate({ bottom: '-400px' }, function() { $('.cookie-show').remove(); });
        localStorage.setItem('cookiePolicy', JSON.stringify(timestamp));
    })

    // show more
	$('.toggle-list').click(function(e) {
		e.preventDefault();
		$(this).parent().next().toggleClass('opened');
		if($(this).hasClass('btn')) {
			$(this).parent().next().hasClass('opened') ? $(this).text('Read less') : $(this).text('Read more');
		} else {
			$(this).hasClass('opened') ? $(this).text('See less') : $(this).text('See benefits');
		}
	});

	$('.read-more').click(function(e) {
        e.preventDefault();
        $(this).parent().parent().find('.read-more-wrap').slideToggle(230, "linear").toggleClass('opened');
        if($(this).parent().parent().find('.read-more-wrap').hasClass('opened')) {
            $(this).text('See less')
        } else {
            $(this).text('See more')
        }
        
	});
    
    $('.open-benefits').click(function(e) {
        e.preventDefault();
        var id = $(this).attr('href');
        $('.benefits-intro').slideUp();
        $(id).slideDown();
    });
    
    $('.close-benefits').click(function(e) {
        e.preventDefault();
        $('.benefits #sa, .benefits #usa').slideUp();
        $('.benefits-intro').slideDown();
    });

    // scrollto link with fade
	$('body').on('click', 'a[href^="#"]:not( a[href="#"], a[href="#sa"], a[href="#usa"], a[href="#basicSlider"], a[data-toggle="collapse"], a[data-toggle="tab"] )', function(e) {
        e.preventDefault();
        var hash = $(this).attr('href');
        var custom_offset = $('#template-media-library.page-id-554').length || $('#template-product.page-id-39').length ? 80 : $('#spy').height();
        if($('.product-transact').length && hash == '#s7') custom_offset = 150;
        $('html, body').animate({
			scrollTop: $(hash).offset().top - custom_offset
		}, 1000);
    });

    // Just a quick custom scroll to for [href="[[*uri]]#Top"] this might change
    $('a[href="[[*uri]]#Top"]').click(function (e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: $('body').offset().top
        }, 1000);
    });
    
    //Dropkick
	$('select, .xs-select').not('.custom-dk').dropkick({
        mobile: true
	});
    
    //Developers
    if($('#template-developers').length || $('#template-developers-search').length) {
        //Dropkick
        dkDevs = $('#dropdown-devs').dropkick({
            mobile: true,
            change: function() {
                window.location.href = '/developers/'+this.value+'/';
            }
        });
    }
    
    if($('#template-developers').length) {
        //Load first article
        $('.load_article').click(function () {
            var el = $($(this).attr('href')).find('a').first();
            window.location.href = el.attr('href');
        });

        //Responsive tables {
        $('#template-developers .content table').addClass('table table-responsive');

        //Placeholder fix for IE
        if ($('input, textarea').length) {
            $('input, textarea').placeholder();
        }
    }
    
    //Page Navigation
    $('.slice').each(function(index) {
        if($(this).hasClass('slice-nav')) {
            if($(this).find('h1').length) {
                var title = $(this).find('h1').first().text();
            } else if($(this).find('h2').length) {
                var title = $(this).find('h2').first().text();
            } else if($(this).find('h3').length) {
                var title = $(this).find('h3').first().text();
            }
            title = title.replace('Touch pricing', 'PRICING');
            title = title.replace('Download the Touch app today', 'DOWNLOAD');
            $('.page-navigation').append('<li><a data-slice="#'+index+'" href="#s'+index+'">'+title+'</a></li>');
        }
		if($('.page-navigation a[data-slice="#'+index+'"]').text() === '') {
			$('.page-navigation a[data-slice="#'+index+'"]').parent().remove();
		}
    });

    // Remove slice from view (used for custom views)
    $('.remove-node.hide').parent().remove();

	$('#filter-search').click(function(e) {
		e.preventDefault();
		var landing      = $('select.landing').val().length > 0 ? $('select.landing').val() : 'articles';
		var category     = $('select.category').val().length > 0 ? $('select.category').val() :  '';
        
        var url_redirect = home_url + '/' + landing + '/' + category + '/';
		window.location  = url_redirect;
	});

	$('#watch-video, .watch-video, .play-tutorial').click(function(e){
		e.preventDefault();
		var get_src = $(this).attr( "href" );
        if($(this).hasClass('play-tutorial')) {
            $('#videoModal .iframe-container').html('<iframe width="800" height="450" src="'+get_src+'" frameborder="0" allowfullscreen></iframe>');
        } else {
            $('#videoModal .iframe-container').html('<iframe width="100%" height="315" src="'+get_src+'" frameborder="0" allowfullscreen></iframe>');
        }
		$('#videoModal').modal('show');
	});

	$('#videoModal .close').click(function() {
		$('#videoModal .iframe-container').empty();
	});
    
	// TODO: Find all slick sliders and see where we can refactor
	if($('.convert-to-slider').length) {

        $('.convert-to-slider').removeClass('hide');
	    getSlidesToShow = function (setWidth) {
            if (setWidth < 550) { return 1; }
            if (setWidth < 680) { return 2; }
            if (setWidth > 768) { return 3; }
        };
        if(window.innerWidth > 767) {

            $('.convert-to-slider').slick({
                infinite: true,
                dots: true,
                arrows: true,
                prevArrow: "<span class='slider-left bs-icon-arrow-left'></span>",
                nextArrow: "<span class='slider-right bs-icon-arrow-right'></span>",
                slidesToShow: getSlidesToShow(window.innerWidth), // show side depending on screen size
                slidesToScroll: 1
            });
            $('.media').each(function () {
                $(this).find($('.slick-dots, .slider-left, .slider-right'))
                       .wrapAll("<div class='slick-pagination-wrap'></div>");
            })
        }
	}

    if($('.slider').length > 0) {

        $('.slider').slick({
            dots: true,
            infinite: true,
            arrows: $('.slider').data().slideArrows ? true : false,
            prevArrow: '<a class="left slider-carousel-control hidden-xs"></a>',
            nextArrow: '<a class="right slider-carousel-control hidden-xs"></a>',
            slidesToShow: 1,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: $('.page-id-39 #s1 .slider').length ? 5000 : 2000
        });
    }

    $('.show-all').click(function(e){
        e.preventDefault();
        var main_wrap = $(this).parent().parent().parent();
        main_wrap.find('.show-all').hide();
        main_wrap.find('.hidden-xs').removeClass('hidden-xs');
        main_wrap.find('.hide-on-mobile').removeClass('hide-on-mobile');
    });

    if(window.innerWidth < 768) {
        //Mobile Nav
        $('.navbar-nav > li.dropdown > a').each(function() {
            $(this).addClass('dropdown-toggle').attr('data-toggle', 'dropdown').attr('role', 'button').attr('aria-haspopup', 'true').attr('aria-expanded', 'false');
        });

		$('#clickatell-main-nav .navbar-toggle, #clickatell-main-nav .close-nav').click(function() {
			$('#clickatell-main-nav').toggleClass('nav-is-open');
		});

		// Apply slick to all the names in array
		$('.mobile-slider, #our-success-stories, #our-values .row:last-child, .benefits.box .row').slick({
			dots:           true,
			infinite:       true,
			arrows:         false,
			slidesToShow:   1,
			slidesToScroll: 1,
			autoplay:       true,
			autoplaySpeed:  2000
		});
		
		$('.products-mobile-slider[data-arrows="true"][data-dots="false"]').slick({
			dots:           false,
			infinite:       true,
			arrows:         true,
			slidesToShow:   1,
			slidesToScroll: 1,
			autoplay:       false,
			autoplaySpeed:  2000,
			prevArrow: $('.slider-arrow-left'),
            nextArrow: $('.slider-arrow-right'),
		});


		$('h3').data('mobile', 'btn').click(function() {
			$(this).parent().toggleClass('open');
		});

    }
    
    $('.info-box .close').on('click',function (e) {
        e.preventDefault();
        $(this).parent().hide();
    });

    $('.info .icon').on('click', function (e) {
        e.preventDefault();
        $(this).next().show();
    });

    if(window.innerWidth > 768) {
        $('.info .icon').hover( function (e) {
            e.preventDefault();
            $(this).next().show();
        });
    }

    // Touch product
    $('#template-product [data-href^="#"]').click(function () {
        var id = $(this).data().href.replace('#', '');
        $('#template-product .nav-item').removeClass('active');
        $(this).addClass('active');
        $('#template-product .item-wrap').removeClass('active')
        $('#template-product .item-wrap#' + id).addClass('active');
    });
    
    // Short Code page
    $('.see-more-btn').click(function(e) {
        e.preventDefault();
        
        if($(this).text() == 'See more') {
            $('.see-more-text').removeClass('hidden-xs');
            $(this).text('See less');
        } else {
            $('.see-more-text').addClass('hidden-xs');
            $(this).text('See more');
        }
    });
    
    if(window.innerWidth < 768) {
        var benHtml = '';
        $('#shortcode-benefits .row > div').each(function() {
            benHtml += '<div>'+$(this).html()+'</div>';
        });
        $('#shortcode-benefits').html(benHtml);
        
        $('#shortcode-benefits').slick({
			dots:           true,
			infinite:       true,
			arrows:         false,
			slidesToShow:   1,
			slidesToScroll: 1,
			autoplay:       true,
			autoplaySpeed:  2000
		});
    }
    

    // JQuery sticky
    if($('.sticky-nav').length > 0 && $(window).width() > 991) {
        $('.sticky-nav').sticky({ bottomSpacing : $('.get-involved').height() + $('#footer').height() + 50 });
    }
});

// Functions

function stickyNav() {
    // sticky nav
	var header_height = $('#header').height();
    if($('nav[data-on-scroll="fixed"]').length > 0) {
        // Duplicated this bottom section we can clean it later
        var nav = $('nav[data-on-scroll="fixed"]');
        var scrolled = nav.hasClass('top-fixed') ? true : false;
        var nav_height = nav.height();
        if ($(this).scrollTop() >= header_height) {
            scrolled = true;
            nav.addClass('top-fixed').next().css('padding-top', nav_height);
        } else {
            nav.removeClass('top-fixed').next().css('padding-top', 0);
        }
    }
    // Reverse scroll
    if($('nav[data-on-scroll="reverse-fixed"]').length > 0) {
        var nav        = $('nav[data-on-scroll="reverse-fixed"]');
        var scrolled   = nav.hasClass('bottom-fixed') ? true : false;
        var thisElementInView = isScrolledIntoView($('.original'));
        if(thisElementInView) {
            scrolled = true;
            // fade out old nav
            nav.hide();
            $('.original').addClass('fade-in');
            // fade in new nav
        } else {
            nav.show();
            $('.original').removeClass('fade-in');
        }
    }

    if($('#slices').length > 0) {
        var nav  = $('#slices .page-navigation');
        var scrolled = nav.parent().parent().parent().hasClass('top-fixed') ? true : false;

        if($('#template-blog-category, #template-blog-landing, #template-secondary').length === 0 && $('#spy ul li').length !== 0) {
            if($(this).scrollTop() >= header_height) {
                scrolled = true;
                nav.parent().parent().parent().addClass('top-fixed');
                $('#slices').addClass('nav-is-scrolling');
            } else {
                nav.parent().parent().parent().removeClass('top-fixed');
                $('#slices').removeClass('nav-is-scrolling');
            }
        }
    }

	if($('.filter-wrap').length > 0) {
		if($(this).scrollTop() >= header_height + 59) {
			scrolled = true;
			$('.filter-wrap').addClass('top-fixed');
		} else {
			if($('.filter-wrap').hasClass('top-fixed')) {
				$('.filter-wrap').removeClass('top-fixed');
			}

		}
	}

}

//Themosis AJAX form
function ajaxCall(action, data, cb) {
    data['action'] = action;
    data['_themosisnonce'] = $('#_themosisnonce').val();
    
    $.ajax({
        url: themosis.ajaxurl,
        method: 'POST',
        dataType: 'json',
        data: data
    }).done(function(data) {
        cb(data);
    });
}

//Prepare AJAX data array
function ajaxData(el) {
    var data = {};
    $(el+' input, '+el+' textarea, '+el+' select').each(function() {
        data[$(this).attr('name')] = $(this).val();
    });
    if(data.hasOwnProperty('verify_email')) delete data.verify_email;
    return data;
}


//Send Form with Ajax
function ajaxForm(formElement, targElement, successMsg) {
	formElement = typeof formElement !== 'undefined' ? formElement : '.ajax';
	targElement = typeof targElement !== 'undefined' ? targElement : '.result';
	successMsg  = typeof successMsg  !== 'undefined' ? successMsg  : '<h3>Thank you</h3><p>Your message was sent successfully.</p>';

	$(formElement).submit(function (e) {
		e.preventDefault();
		if(is_valid) {
			$(targElement).addClass('bg-warning').show().html('<strong>Loading...</strong>');
			$.ajax({
				type: 'POST',
				dataType: 'json',
				url: $(this).attr('action'),
				data: $(this).serialize(),
				success: function (data, textStatus, jqXHR) {
					$(targElement).removeClass('bg-success bg-danger bg-warning').empty();
					if (data && data.success == true) {
						$(targElement).addClass('bg-success').html(successMsg);
						$('input, textarea').val('');
						$('option').removeAttr('selected');
						$('.checkbox input, .radio input').removeAttr('checked');
						return;
					}
					if (data && data.success == false) {
						$(targElement).addClass('bg-danger');
						$.each(data.errors, function (index, value) {
							$(targElement).append(value + '<br />');
						});
						return;
					}
				},
				error: function (jqXHR, textStatus, errorThrown) {
					$(targElement).addClass('bg-danger').text('Something went wrong, please try again later.');
				}
			});
		}
		return false;
	});
}

//FB Share
function fbShare() {
	var winWidth = 520;
	var winHeight = 350;
	var winTop = (screen.height / 2) - (winHeight / 2);
	var winLeft = (screen.width / 2) - (winWidth / 2);
	window.open('http://www.facebook.com/sharer.php?s=100&p[url]='+window.location.href, 'sharer', 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width='+winWidth+',height='+winHeight);
}

function liShare() {
    var winWidth = 520;
	var winHeight = 350;
	var winTop = (screen.height / 2) - (winHeight / 2);
	var winLeft = (screen.width / 2) - (winWidth / 2);
	window.open('https://www.linkedin.com/shareArticle?mini=true&url='+window.location.href+'&title='+encodeURIComponent($('meta[name="twitter:title"]').attr('content')), 'sharer', 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width='+winWidth+',height='+winHeight);
}

// Scrolling

function hasScrolled(target, on_template) {
    if(on_template.length) {
        var st = $(this).scrollTop();

        // Make sure they scroll more than delta
        if(Math.abs(lastScrollTop - st) <= delta)
            return;

        // If they scrolled down and are past the navbar, add class .nav-up.
        // This is necessary so you never see what is "behind" the navbar.
        if (st > lastScrollTop && st > navbarHeight){
            // Scroll Down
            target.removeClass('nav-down').addClass('nav-up');
        } else {
            // Scroll Up
            if(st + $(window).height() < $(document).height()) {
                target.removeClass('nav-up').addClass('nav-down');
            }
        }

        if(st === 0) {
            $('#header.small').removeClass('nav-down');
        }
        lastScrollTop = st;
    }
}

// See if an element is in scroll view
function isScrolledIntoView(target)
{
    var docViewTop    = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop    = $(target).offset().top;
    var elemBottom = elemTop + $(target).height();

    // return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
    return elemBottom <= docViewBottom;
}

function cLog(msg) {
    if(debug) console.log(msg);
}

// Check for nested object keys, usage: checkNested(test, 'level1', 'level2', 'level3');
function checkNested(obj) {
    var args = Array.prototype.slice.call(arguments, 1);
    for (var i = 0; i < args.length; i++) {
        if (!obj || !obj.hasOwnProperty(args[i])) {
            return false;
        }
        obj = obj[args[i]];
    }
    return true;
}

function pinElementToTopOfScreen(target) {
    var target_parent_distance  = target.parent().offset().top; // get the original value in the array
    var target_distance         = target.offset().top; // get the modified value in the array
    var window_top_position     = $(window).scrollTop();

    if(window_top_position >= target_distance) target.addClass('fixed');

    if(window_top_position < target_parent_distance) target.removeClass('fixed');
}

function pinOnScroll(target) {
    var obj           = target;
    var parent        = obj.parent();
    var window_scroll = $(window).scrollTop();
    var offset = {
        start : target.offset().top,
        stop  : $('.col-content').height() || $('.col-right').height(),
        container_offset : $('.col-content').offset() || $('.col-right').offset()
    }
    offset.stop = offset.stop - offset.container_offset.top
    cLog(offset.stop);
    if($('.main-content2').length) offset.start = 295;
    
    // set the height of the column to match the height
    // of the previous column.
    parent.height(offset.stop);

    // scrolling down
    if(user_is_scrolling === 'down') {
        if (window_scroll >= offset.start) {
            obj.addClass('fixed-top');
        }
        if (window_scroll >= offset.stop) {
            obj.removeClass('fixed-top').addClass('absolute');
        }
    }

    // scrolling up
    if(user_is_scrolling === 'up') {
        if(window_scroll <= offset.stop) {
            obj.removeClass('absolute').addClass('fixed-top');
        }
        if(window_scroll <= offset.start) {
            obj.removeClass('fixed-top').removeClass('absolute');
        }
    }
}

//CustomEvent polyfill for IE
(function () {
  if ( typeof window.CustomEvent === "function" ) return false; //If not IE

  function CustomEvent ( event, params ) {
    params = params || { bubbles: false, cancelable: false, detail: undefined };
    var evt = document.createEvent( 'CustomEvent' );
    evt.initCustomEvent( event, params.bubbles, params.cancelable, params.detail );
    return evt;
   }

  CustomEvent.prototype = window.Event.prototype;

  window.CustomEvent = CustomEvent;
})();