function switchitem(obj, patch){

    if (  document.getElementById(obj).checked ) {
       val=1;
    } else {
       val=0;
    }

   
    $.ajax({
      url: '/setmodules/fan/fan_turnon/'+val,
    });
}





$( window ).load(function() {
    $('input[type=checkbox]').tzCheckbox({labels:['Enable','Disable']});
    
    $('.tzCheckBox').click(function() {
       name=this.parentElement.children[1].id.replace("ch_", "");
       switchitem(name);
    });

  

});