function addForm(ev) {
    ev.preventDefault();
    var count = $('#items-form-container').children().length;

    // You can only submit a maximum of `max_attach` items
    if (window.max_attach == undefined) {
        window.max_attach = 42;
    }

    if (count < window.max_attach) {
        var tmplMarkup = $('#item-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('div#items-form-container').append(compiledTmpl);

        // update form count
        $('#id_media-TOTAL_FORMS').attr('value', count+1);

        // some animate to scroll to view our new form
        //$('html, body').animate({
        //        scrollTop: $("#add-item-button").position().top-200
        //    }, 800);
        return true;
        } // End if
    else {
        return false;
    } // End else
} // End addForm

function deleteForm(btn, ev) {
    ev.preventDefault();
    var prefix = "media"
    var count = $('#items-form-container').children().length;
    if (count > 1) {
        // Delete the item/form
        var parents = $(btn).parents();
        var parent2rm = $(btn).parents(".item");
        parent2rm.remove();
        //$(btn).parents('.item').remove();

        var forms = $('.item'); // Get all the forms

        // Update the total number of forms (1 less than before)
        $('#id_' + prefix + '-TOTAL_FORMS').attr('value', forms.length);
        //$('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

        // Go through the forms and set their indices, names and IDs
        var i = 0;
        for (count = forms.length; i < count; i++) {
            $(forms.get(i)).children().children().each(function () {
                if ($(this).attr('type') == 'text') updateElementIndex(this, prefix, i);
            });
        }
    } // End if
    return false;
} // End deleteForm


$(document).ready(function () {
    // Добавить поле при нажатии кнопки
    $('.add-item').click(function(ev) {
      return addForm(ev);
    });

    $('body').on('click', ".delete-item", function(ev) {
        return deleteForm(this, ev);
    });

    // Добавлять поле при вводе URL, если последнее поле заполнено
    $('body').on("input", "[name*='-url']", function (ev) {
            var last_url_field = $("[name*='-url']").get(-1);
            var last_value = last_url_field.value;
            if( last_value ) {
              addForm(ev);
            }
            return false;
        });
});