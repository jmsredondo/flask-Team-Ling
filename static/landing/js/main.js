jQuery(document).ready(function ($) {	

/* ==================================================
			Preloader Calling
================================================== */  
	jQuery(window).load(function() {
        $('.doc-loader').fadeOut('slow');
    });
/* ==================================================
				Parallax
================================================== */
	$(document).ready(function() {  
		$('#features').parallax("50%", 0.6);
		$('#features-2').parallax("50%", 0.6);
		$('#features-3').parallax("50%", 0.6);
		$('#features-4').parallax("50%", 0.6);
		$('#features-5').parallax("50%", 0.6);
		$('#features-6').parallax("50%", 0.6);
		$('#features-7').parallax("50%", 0.6);
		$('#features-8').parallax("50%", 0.6);
		$('#slogan').parallax("50%", 0.6);
		$('#p-contact').parallax("50%", 0.6);
		$('#bg-testimonial').parallax("50%", 0.6);
		$('#home').parallax("50%", 0.6);
	});
/* ==================================================
				Caraousel
================================================== */	
	$('.carousel').carousel();	
/* ==============================================
			Flexslider Slideshow
=============================================== */
	$(window).load(function() {
	  $('.flexslider').flexslider({
		animation: "slide",
		animationLoop: false,
		slideshow: false
	  });
	});
	
	$(window).load(function() {
	  $('.testimonial').flexslider({
		animation: "slide"
	  });
	});
	
	$(window).load(function() {
	  $('.flex-about').flexslider({
		animation: "fade"
	  });
	});
	
	$(window).load(function() {
	  $('.about').flexslider({
		animation: "slide",
		animationLoop: false,
		slideshow: false
	  });
	});
/* ==============================================
			Camera Slideshow
=============================================== */
	jQuery(function(){
		jQuery('#camera_wrap_4').camera({
			height: '50%',
			loader: 'bar',
			loaderColor: '#fff',
			loaderBgColor: 'transparent', 
			pagination: false,
			thumbnails: false,
			hover: false,
			opacityOnGrid: true,
			pauseOnClick: false,
			imagePath: 'images/',
			transPeriod: 2500,
			fx: 'simpleFade' // 'mosaicReverse' mosaicRandom bottomLeftTopRight stampede mosaicSpiralReverse
		});
	});
	
	$(function() {
		$( "#f-accordion" ).accordion({
		  collapsible: true,
		  heightStyle: "content"
		});
	  });
/* ==============================================
				Navbar Dropdown
=============================================== */
	jQuery(document).ready(function ($) {
	$('.navbar .dropdown').hover(function() {
		$(this).addClass('didropdown').find('.dropdown-menu').first().stop(true, true).delay(100).slideDown();
	}, function() {
		var na = $(this)
		na.find('.dropdown-menu').first().stop(true, true).delay(100).slideUp('fast', function(){ na.removeClass('extra-nav-class') })
	});

	$('.dropdown-submenu').hover(function() {
		$(this).addClass('extra-nav-class').find('.dropdown-menu').first().stop(true, true).delay(100).slideDown();
	}, function() {
		var na = $(this)
		na.find('.dropdown-menu').first().stop(true, true).delay(100).slideUp('fast', function(){ na.removeClass('extra-nav-class') })
	});

	});	
/* ==================================================
						Animation	
================================================== */ 
	$('.from-top').each(function () {
		$(this).appear(function() {
		  $(this).delay(150).animate({opacity:1,top:"0px"},1000);
		});	
	});
	
	$('.from-bottom').each(function () {
		$(this).appear(function() {
		  $(this).delay(150).animate({opacity:1,bottom:"0px"},1000);
		});	
	});
	
	
	$('.from-left').each(function () {
		$(this).appear(function() {
		  $(this).delay(150).animate({opacity:1,left:"0px"},1000);
		});	
	});
	
	
	$('.from-right').each(function () {
		$(this).appear(function() {
		  $(this).delay(150).animate({opacity:1,right:"0px"},1000);
		});	
	});
	
	$('.fade-in').each(function () {
		$(this).appear(function() {
		  $(this).delay(150).animate({opacity:1,right:"0px"},1000);
		});	
	});	
/* ==============================================
				skillbar
=============================================== */	
	jQuery(document).ready(function(){
		jQuery('.skillbar').each(function(){
			jQuery(this).find('.skillbar-bar').animate({
				width:jQuery(this).attr('data-percent')
			},6000);
		});
	});
/* ==============================================
				prettyPhoto
=============================================== */
	$(document).ready(function(){
        $("a[rel^='prettyPhoto']").prettyPhoto({
		//theme:'dark_square',
		deeplinking: false
		});
    });
/* ==============================================
		Quicksand FIlterable 
=============================================== */
	var $filterType = $('#filterOptions li.active a').attr('class');
	var $holder = $('ul.holder');
	var $data = $holder.clone();

	$('#filterOptions li a').click(function(e) {
		
		$('#filterOptions li').removeClass('active');
		
		var $filterType = $(this).attr('class');
		$(this).parent().addClass('active');
		
		if ($filterType == 'all') {
			var $filteredData = $data.find('li');
		} 
		else {
			var $filteredData = $data.find('li[data-type~=' + $filterType + ']');
		}
		
		// call quicksand
		$holder.quicksand($filteredData, {
			duration: 800,
			filter: 'selector',
			easing: 'linear'
			});
		return false;
	});


		
//Portfolio Filter Start

function show(filterVal){
if(filterVal == 'all') {
	$('ul#portfolio-items li').fadeIn('slow');
} else {
	$('ul#portfolio-items li').each(function() {
		if($(this).hasClass(filterVal)) {
			$(this).fadeIn('slow');
			}
		})
}
}

$('ul#filter a').click(function() {
	$(this).css('outline','none');
	var filterVal = $(this).text().toLowerCase().replace(' ','-');
	var itemsLength = $('ul#portfolio-items  li:visible').length;
	$('ul#filter .active').removeClass('active');
	$(this).parent().addClass('active');
	$('ul#portfolio-items  li:visible').each(function(i) {
		$(this).fadeOut('slow', function(){
			if(itemsLength == ++i){show(filterVal);		
			}
		});
	});
	return false;
});


});	