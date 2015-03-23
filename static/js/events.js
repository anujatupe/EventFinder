$(function(){
  $('a').click(function()
    {
      return ($(this).attr('disabled')) ? false : true;
    });
});