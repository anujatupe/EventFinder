$(function(){
  /*
   * Count variable to keep a track of the number of checkboxes that are checked
   */
  var count = 0;

  /*
   * Show the error message
   */
  function show_form_error() {
    $("#form_error").show();
    setTimeout(function() {
      $("#form_error").fadeOut();
    }, 2000);
  }

  /*
   * Function to keep track of checked checkboxes.
   * Shows the error message when more than 3 checkboxes are checked.
   * If no checkboxes are checked or more than 3 are checked, disable the submit button.
   */
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

  /*
   * Function to submit the categories form. Checks how many checkboxes are checked before submitting.
   * If more than 3 are checked, show the error message.
   * If less than three and more than zero, submit the form.
   */
  $("#submit_categories").click(function() {
    if (count > 3) {
      show_form_error();
    } else {
      $("#categories_form").submit();
    }
  })
});
