function switchitem(param){
    data = {
        'filename' : param
    }    

    
    $.ajax({
      url: '/roomba_switch/',
      data: data
    });
}





function RetItem(name, active) {
     checked = '';
     
     if  ( active ) {
      checked = ' checked ';
     } 

    return 	 '<li><label for="ch_'+name+'">'+name+': </label><input type="checkbox" id="ch_'+name+'" name="ch_'+name+'" data-on="ON" data-off="OFF" onchange="switchitem(\''+name+'\')" '+checked+ '/></li>';
}




function getLastRoombaStatus() {
  $.getJSON('/roomba_status/', function( data ) {
    if (typeof data != 'undefined') {
            text="<ul>"
            for (i = 0; i < data.length; ++i) {
                item = data[i];
                text+=RetItem(item[0], item[1]);
            }        
            text+="</ul>"


        $("#items").html( text  );
    }
    $('input[type=checkbox]').tzCheckbox({labels:['Enable','Disable']});
    
    
    $('.tzCheckBox').click(function() {
       name=this.parentElement.children[1].id.replace("ch_", "");
       switchitem(name);
    });
 
    
  });
}



$( window ).load(function() {
    getLastRoombaStatus();
  

});