$(document).ready(function () {

    $("#file_submit_button").click( function (event) {



        var url = '';
        var data = {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'post_type':'file_submit',
        
        };


        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            success: function (data) {
                location.reload(true); //reloads page after view runs its program so document list gets updated
            }
        });
    });  
});