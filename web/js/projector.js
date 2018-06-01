function switchitem(){
    data = {
        'status' : '-'
    }

    $.ajax({
      url: '/projector/',
      data: data
    });
}

function getProjectorStatus() {
  $.getJSON('/projector_status/', function( data ) {
    ischecked='';
    if (typeof data != 'undefined') {
          if (data == '1') {
            ischecked=' checked ';
          }
    }
    
    text='<ul><li><label for="status">Cinema Mode</label><input type="checkbox" id="chk_status" name="status" data-on="ON" data-off="OFF" onchange="switchitem()" '+ischecked+'/></li></ul>';
    
    $("#items").html( text );
    $('input[type=checkbox]').tzCheckbox({labels:['Enable','Disable']});
    
    $('.tzCheckBox').click(function() {
       switchitem();
    });
 
    
  });
}


$( window ).load(function() {
    getProjectorStatus();
    $('input[type=checkbox]').tzCheckbox({labels:['Enable','Disable']});
});