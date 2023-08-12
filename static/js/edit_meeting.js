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


        // Get selected documents (to delet them)
        let selected_files_checkbox = $('#document_list').children('li').find('input').filter(function(){
            return $(this).prop('checked');
        });
        // the value of the checkbox is the id of its corresponding file
        let file_ids = []
        for(let i = 0; i < selected_files_checkbox.length; i++){
            file_ids.push($(selected_files_checkbox[i]).val());
        }






        if(meeting_date != '' && meeting_name != ''){ // Only submits ajax request if there is a date and a name

            var url = '';
            var data = new FormData();
            data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
            data.append('post_type', 'meeting_submit');
            data.append('meeting_name', meeting_name);
            data.append('meeting_date', meeting_date);
            data.append('meeting_description', meeting_description);

            for (let i = 0; i < file_ids.length; i++) {
                data.append('file_id', file_ids[i]);
            }
    
            var files = myDropzone.getAcceptedFiles();
            for (let i = 0; i < files.length; i++) {
                data.append('files', files[i]);
            }

            $.ajax({
                url: url,
                method: 'POST',
                data: data,
                processData: false,
                contentType: false,
                success: function (response) {

                    if (response.redirect){
                        window.location = './'
                    }
                    
                }
            });
        }

    })
    
});