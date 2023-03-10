$(document).ready(function () {

    $(".documentDelButton").click( function (event) {

        var documentName =  $(event.target).parent().children('a').text();
        console.log(documentName);

        var url = '';
        var data = {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'documentName':documentName,
        
        };


        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            success: function (data) {
                $(event.target).parent().remove();
            }
        });
    });  
});
