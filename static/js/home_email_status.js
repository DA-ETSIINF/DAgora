// javascript for changing status of the users "show_email" attribute when pressing on the checkbox on the homepage
$(document).ready(function(){
    $('#profile_window').find("#email_checkbox").click(function(event){
        var url = '';
        var data = {
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
          'show_email': $(this).prop('checked'),
        };

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            success: function (data) {

            }
          });
    });
});