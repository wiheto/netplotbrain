function ready() {
  function button(className) {
    return '<button class="button ' + className + '"></button>';
  };

  function container(className) {
    return '<div class="pheasant-button-container">' + button(className) + '</div>';
  };

  $(".pheasant-fenced-code .cell.input .code").append(container('toggle input'));
  $(".pheasant-fenced-code .cell.error .code").append(container('toggle error hide'));
  $(".pheasant-fenced-code .cell.embed .code").append(container('embed'));

  $('.toggle.input').attr('title', 'Toggle Status Line').click(function(e) {
    $('.pheasant-fenced-code .input').toggleClass('hide')
  });

  $(".pheasant-fenced-code").each(function() {
    $(this).find('.cell.input').each(function() {
      var stdout = $(this).parent().find('.cell.stdout');
      if (stdout.length) {
        $(button('toggle output')).prependTo($(this).find('.pheasant-button-container'))
          .attr('title', 'Toggle Stdout').click(function(e) {
            stdout.toggleClass('hide');
            $(this).toggleClass('hide');
          });
      };
      var stderr = $(this).parent().find('.cell.stderr').toggleClass('hide');
      if (stderr.length) {
        $(button('toggle error hide')).prependTo($(this).find('.pheasant-button-container'))
          .attr('title', 'Toggle Stderr').click(function(e) {
            stderr.toggleClass('hide');
            $(this).toggleClass('hide');
          });
      };
    });

    $(this).find('.cell.error').toggleClass('hide').each(function(index, error) {
      $(this).find('.toggle.error').each(function() {
        $(this).attr('title', 'Toggle Traceback').click(function(e) {
          $(error).toggleClass('hide');
          $(this).toggleClass('hide');
        });

      })
    });
  });

  $('.pheasant-fenced-code .report .count').attr('title', 'Cell Number');
  $('.pheasant-fenced-code .report .start').attr('title', 'Evaluated at');
  $('.pheasant-fenced-code .report .time').attr('title', 'Cell Execution Time');
  $('.pheasant-fenced-code .report .total').attr('title', 'Total Execution Time');
  $('.pheasant-fenced-code .report .kernel').attr('title', 'Kernel Name');

  $('.source .pheasant-button-container .embed').attr('title', 'Source Code');
  $('.file .pheasant-button-container .embed').attr('title', 'Source File');
  $('.terminal .pheasant-button-container .embed').attr('title', 'Terminal Command');
}

$(ready);
