$(document).ready(function(){
    // auxilary function
    function get_text(value){ // function to convert the value to a string but if its blank it stays blank instead of 'undefined'
        if(value == undefined){
            return '';
        }
        else{
            return String(value);
        }
    }

    $('#submit_button').click(function(event){

        

        
        // Get basic info of the meeting from the different input boxes

        let meeting_name = get_text($('#name_input_box').val());
        let meeting_date = get_text($('#date_input_box').val());
        let meeting_description = get_text($('#description_input_box').val());


        // raise alert if theres no name or date written
        if (meeting_name == '' || meeting_date == ''){
            $('#alert').css("display","block").css("color","red").css('font-weight','bold');            
            $('#alert').text('*please fill out all fields');
            $("html, body").animate({ scrollTop: 0 }, "slow");
            $('#name_input_box').change( function(event){
                $('#alert').css('display','none');
                return;
            });
        }


        // User list:
        // Get every user with its checkbox checked
        // The value of the checkbox input is the id of the user

        let labels_of_checked_users = $('#user_selection').children('li').children('div').children('div').children('label').filter(function(){
            return $(this).children('div').children(':checkbox').prop('checked');
        }); // Labels of users who have their checkbox checked -> Only selects labels of users, not roles

        let user_ids = [];
        for (let i = 0; i<labels_of_checked_users.length; i++){
            let checkbox = $(labels_of_checked_users[i]).children('div').children(':checkbox');
            let id = Number(checkbox.val());
            if (jQuery.inArray(id, user_ids) == -1){ //checks if user id is already in array before adding
                user_ids.push(id);
            }            
        }
        //Transform array to string because django expects data in String form:
        let user_ids_string = ' ';
        for (let i = 0; i<user_ids.length; i++){
            user_ids_string = user_ids_string + String(user_ids[i]) + " ";
        }
        user_ids_string = user_ids_string.trim();




        var url = '';
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
        data.append('post_type', 'meeting_submit');
        data.append('submited_users_Ids', user_ids_string);
        data.append('meeting_name', meeting_name);
        data.append('meeting_date', meeting_date);
        data.append('meeting_description', meeting_description);

        var files = myDropzone.getAcceptedFiles();
        for (var i = 0; i < files.length; i++) {
            data.append('files', files[i]);
        }

        if(meeting_date != '' && meeting_name != ''){ // Only submits ajax request if there is a date and a name
            $.ajax({
                url: url,
                method: 'POST',
                data: data,
                processData: false,
                contentType: false,
                success: function (response) {

                    if (response.redirect){
                        window.location.href = '/../meeting/' + response.meeting_id;
                    }
                    else{
                        // if redirect response == false -> view said the name is already in use -> display alert
                        $('#alert').css("display","block").css("color","red").css('font-weight','bold');
                        $('#alert').text('*a reunion with that name already exists, please change the name');
                        $("html, body").animate({ scrollTop: 0 }, "slow");
                        $('#name_input_box').change( function(event){
                            $('#alert').css('display','none');
                            return;
                        });
                        return;
                    }
                    
                }
            });
        }

    })
    
});