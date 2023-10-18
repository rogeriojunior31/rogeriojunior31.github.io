$(document).ready(function() {
  "use strict"; // Enable strict mode

  // Variables
  var $codeSnippets = $('.code-example-body'),
      $nav = $('.navbar'),
      $body = $('body'),
      $window = $(window),
      $popoverLink = $('[data-popover]'),
      $popovers = $('.popover'),
      navOffsetTop = $nav.offset().top,
      entityMap = {
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': '&quot;',
          "'": '&#39;',
          "/": '&#x2F;'
      };

  function init() {
      $window.on('scroll', onScroll)
             .on('resize', resize);

      $popoverLink.on('click', openPopover);
      $document.on('click', closePopover);
      $('a[href^="#"]').on('click', smoothScroll);
      
      buildSnippets();
  }

  function smoothScroll(e) {
      e.preventDefault();

      var target = this.hash;
      var $target = $(target);

      $('html, body').stop().animate({
          'scrollTop': $target.offset().top - 40
      }, 500, 'swing', function() {
          window.location.hash = target;
      });
  }

  function openPopover(e) {
      e.preventDefault();
      closePopover();

      var popover = $($(this).data('popover'));
      popover.toggleClass('open');

      e.stopImmediatePropagation();
  }

  function closePopover() {
      $popovers.removeClass('open');
  }

  $("#button").click(function() {
      $('html, body').animate({
          scrollTop: $("#elementtoScrollToID").offset().top
      }, 2000);
  });

  function resize() {
      navOffsetTop = $nav.offset().top;
      onScroll();
  }

  function onScroll() {
      if (navOffsetTop < $window.scrollTop() && !$body.hasClass('has-docked-nav')) {
          $body.addClass('has-docked-nav');
      } else if (navOffsetTop > $window.scrollTop() && $body.hasClass('has-docked-nav')) {
          $body.removeClass('has-docked-nav');
      }
  }

  function escapeHtml(string) {
      return String(string).replace(/[&<>"'\/]/g, function(s) {
          return entityMap[s];
      });
  }

  function buildSnippets() {
      $codeSnippets.each(function() {
          var newContent = escapeHtml($(this).html());
          $(this).html(newContent);
      });
  }

  init();
});