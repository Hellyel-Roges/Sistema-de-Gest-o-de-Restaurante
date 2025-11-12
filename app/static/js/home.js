$(function () {

  function isInViewport($el) {
    const top = $el.offset().top;
    const bottom = top + $el.outerHeight();
    const scrollTop = $(window).scrollTop();
    const windowBottom = scrollTop + $(window).height();
    return (top < windowBottom - 40) && (bottom > scrollTop + 40);
  }

  function checkFadeIns() {
    $('.fade-in').each(function () {
      const $this = $(this);
      if (!$this.hasClass('visible') && isInViewport($this)) {
        $this.addClass('visible');
      }
    });
  }

  // Checa após o carregamento e a cada rolagem
  $(window).on('load scroll resize', function () {
    checkFadeIns();
  });

  // Garante que o hero e o conteúdo apareçam mesmo sem rolar
  setTimeout(checkFadeIns, 200);
});