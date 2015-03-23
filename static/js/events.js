$(function(){
  /*
   * Function to disable a href if the attribute disabled is encountered in the a href element
   */
  $('a').click(function()
    {
      return ($(this).attr('disabled')) ? false : true;
    });
});