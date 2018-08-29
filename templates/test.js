
$(document).ready(function(){
    $('#form').submit(function(e){
        console.log('asdsad');
        $.post('', $(this).serialize(), function(data){
               // of course you can do something more fancy with your respone
               console.log('asdsad');
            });
            e.preventDefault();
        });

});
