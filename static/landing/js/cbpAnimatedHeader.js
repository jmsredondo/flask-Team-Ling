/**
 * cbpAnimatedHeader.js v1.0.0
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * Copyright 2013, Codrops
 * http://www.codrops.com
 */
var cbpAnimatedHeader = (function() {

	var docElem = document.documentElement,
		opacity = document.querySelector( '.top-soc' ),
		navbar = document.querySelector( '.navbar' ),
		header = document.querySelector( '.top-soc' ),
		didScroll = false,
		changeHeaderOn = 90;

	function init() {
		window.addEventListener( 'scroll', function( event ) {
			if( !didScroll ) {
				didScroll = true;
				setTimeout( scrollPage, 90 );
			}
		}, false );
	}

	function scrollPage() {
		var sy = scrollY();
		if ( sy >= changeHeaderOn ) {
			classie.add( opacity, 'opacity' ),
			classie.add( navbar, 'border' ),
			classie.add( header, 'hidden' );
		}
		else {
			classie.remove( opacity, 'opacity' ),
			classie.remove( header, 'hidden' ),
			classie.remove( navbar, 'border' );
		}
		didScroll = false;
	}

	function scrollY() {
		return window.pageYOffset || docElem.scrollTop;
	}

	init();

})();