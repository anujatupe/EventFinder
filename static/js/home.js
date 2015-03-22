$(function(){
    var count = 0;

    function show_form_error() {
        $("#form_error").show();
        setTimeout(function() {
            $("#form_error").fadeOut();
        }, 2000);
    }

    $('#categories_form :checkbox').click( function() {
        if($(this).is(':checked')) {
            count++;
        } else {
            count--;
        }

        if (count > 3 ) {
            $("#submit_categories").prop("disabled", true);
            show_form_error();
        } else if (count <= 0) {
            $("#submit_categories").prop("disabled", true);
        } else {
            $("#submit_categories").prop("disabled", false);
        }
    });

    $("#submit_categories").click(function() {
        if (count > 3) {
            show_form_error();
        } else {
            $("#categories_form").submit();
        }
    })
});
