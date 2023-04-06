$(document).ready(function () {

    $(".documentDelButton").click( function (event) {

        var documentName =  $(event.target).parent().children('a').text();

        var url = '';
        var data = {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'documentName':documentName,
        'post_type':'file_deletion',
        
        };


        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            success: function (data) {
                var div = $(event.target).parent().parent();
                $(event.target).parent().remove();
                if ($.trim(div.html())==''){ // checks if the div is empty
                    div.append('<li>There are no documents linked to this Reunion</li>');
                }
                
            }
        });
    });  
});
