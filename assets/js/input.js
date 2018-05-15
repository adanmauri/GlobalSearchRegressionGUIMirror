function select4pyhtml() {
    $('[data-toggle="select"]').select2();
    $('select.select').each(function(){
        var input = $(this).parent().find('input[data-toggle="select4"]');
        $(input).val($(this).val());
        $(this).change(function(){
            $(input).val($(this).val());
        });
    });
    
    $('select.multiselect').each(function(){
        var input = $(this).parent().find('input[data-toggle="select4"]');
        var value = ($(this).val())?$(this).val().join(';'):'';
        $(input).val(value);
        $(this).change(function(){
            var value = ($(this).val())?$(this).val().join(';'):'';
            $(input).val(value);
        });
    });
}

function number4pyhtml() {
    
    $('input[type="number"]').each(function() {
        var parent = $(this).parent();
        var input = $(this);        
        var min = ($(input).attr('min'))?$(input).attr('min'):-999999999999999999;
        var max = ($(input).attr('max'))?$(input).attr('max'):999999999999999999;
        var step = ($(input).attr('step'))?parseInt($(input).attr('step')):1;

        $(this).data('val', $(this).val());
        
        $(input).on('focusin', function(){
            $(this).data('val', parseInt($(this).val()));
        });

        $(input).on('change', function(){
            var prev = $(this).data('val');
            var current = $(this).val();

            if (!parseInt(current)) {
                $(this).val(prev);
            } else if (parseInt(current) > max) {
                $(this).val(max);
                if ($(this).data('max-body')) {
                    var modal = $('#alertModal');
                    $(modal).find('.modal-title').html($(this).data('max-title'));
                    $(modal).find('.modal-body').html($(this).data('max-body'));
                    $(modal).modal();
                }
            } else if (parseInt(current) < min) {
                $(this).val(min);
                if ($(this).data('min-body')) {
                    var modal = $('#alertModal');
                    $(modal).find('.modal-title').html($(this).data('min-title'));
                    $(modal).find('.modal-body').html($(this).data('min-body'));
                    $(modal).modal();
                }
            } else {
                $(this).val(parseInt(current));
            }
        });

        $(parent).append(
            '<div class="input-number-nav">'+
            '   <div class="input-number-button input-button-up">+</div>'+
            '   <div class="input-number-button input-button-down">-</div>'+
            '</div>'
        );

        var btns = $(parent).find('.input-number-button');
        var btnUp = $(parent).find('.input-button-up');
        var btnDown = $(parent).find('.input-button-down');

        $(btns).mouseover(function(){
            $(input).addClass("active");
        });
        $(btns).mouseover(function(){
            $(input).addClass("active");
        });
        
        $(btns).click(function() {
            var oldValue = parseInt($(input).val());
            if ($(this).hasClass("input-button-up")) {
                if (oldValue >= max) {
                    var newVal = oldValue;
                } else {
                    var newVal = oldValue + step;
                }    
            } else {
                if (oldValue <= min) {
                    var newVal = oldValue;
                } else {
                    var newVal = oldValue - step;
                }
            }
            $(input).val(newVal);
            $(input).trigger("change");
        });        
    });
}

/*jQuery(
    '<div class="quantity-nav">'+
    '   <div class="quantity-button quantity-up">+</div>'+
    '   <div class="quantity-button quantity-down">-</div>'+
    '</div>').insertAfter('.quantity input'
    );
    jQuery('.quantity').each(function() {
        var spinner = jQuery(this),
        input = spinner.find('input[type="number"]'),
        btnUp = spinner.find('.quantity-up'),
        btnDown = spinner.find('.quantity-down'),
        min = input.attr('min'),
        max = input.attr('max');

  btnUp.click(function() {
    var oldValue = parseFloat(input.val());
    if (oldValue >= max) {
      var newVal = oldValue;
    } else {
      var newVal = oldValue + 1;
    }
    spinner.find("input").val(newVal);
    spinner.find("input").trigger("change");
  });

  btnDown.click(function() {
    var oldValue = parseFloat(input.val());
    if (oldValue <= min) {
      var newVal = oldValue;
    } else {
      var newVal = oldValue - 1;
    }
    spinner.find("input").val(newVal);
    spinner.find("input").trigger("change");
  });

});*/
