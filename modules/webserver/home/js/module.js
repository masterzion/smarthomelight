function switchitem(s){
    obj=document.getElementById(s);

    if (  obj.checked ) {
       val=1;
    } else {
       val=0;
    }
    
    
    uri=obj.attributes['uri_val'].value
    s_url='/setmodules/'+uri+'/'+val;

    $.ajax({
      url: s_url,
    });
}





$( window ).load(function() {
    $('input[type=checkbox]').tzCheckbox({labels:['Enable','Disable']});
    
    $('.tzCheckBox').click(function() {
       name=this.parentElement.children[1].id.replace("ch_", "");
       switchitem(name);
    });

  

});