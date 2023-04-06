$(document).ready(function(){


    // Ajax request for user submission
    $("#reunionname").click( function (event) {   

        // get reunion Info from the form ->
        // the info is stored in three input elements with the ids id_my_name, id_my_date and id_my_description

        function hasText(value){ // function to convert the value to a string but if its blank it stays blank
            if(value == undefined){
                return '';
            }
            else{
                return String(value);
            }
        }

        let my_name = hasText($('#id_my_name').val());
        let my_date = hasText($('#id_my_date').val());
        let my_description = hasText($('#id_my_description').val());

        // raise alert if theres no name written
        if (my_name == '' || my_date == ''){
            $('#alert').css("display","block").css("color","red").css('font-weight','bold');
            $("html, body").animate({ scrollTop: 0 }, "slow");
            $('#id_my_name').change( function(event){
                $('#alert').css('display','none');
                return;
            });
        }




        // get user list ->

        // data = every user id with checked checkbox
        // val proprety of every user label element == {{user.id}}
        // but only do this for labels with checked checkboxes

        // Get label elements for checked users
        let checkedUserLabels = $('#userSelectionFormRole').children('li').children('div').children('div').children('label').filter(function(){
            return $(this).children('div').children(':checkbox').prop('checked');
        });

        let userIds = [];
        for (let i = 0; i<checkedUserLabels.length; i++){
            let checkbox = $(checkedUserLabels[i]).children('div').children(':checkbox');
            let id = Number(checkbox.val());
            // check if the id is already contained 
            //so even if the same user is selected multiple times (which will happen) there are no repeated ids pased over
            if (jQuery.inArray(id, userIds) == -1){ // if it == -1 it means it is not contained
                userIds.push(id);
            }            
        }

        

        // transform it to string becasue the server expects all the 'data' to be of String type
        let userIdsString = ' ';
        for (let i = 0; i<userIds.length; i++){
            userIdsString = userIdsString + String(userIds[i]) + " ";
        }
        userIdsString = userIdsString.trim(); // delete the extra space added at the end


        var url = '';
        var data = {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'post_type':'reunion_users_submit_ajax',
        'submited_users_Ids': userIdsString,
        'reunion_name':my_name,
        'reunion_date':my_date,
        'reunion_description':my_description,
        };


        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            success: function (data) {
                console.log(userIdsString);
                const xhr = new XMLHttpRequest();
                xhr.open("GET", '../reunion/' + my_name + "/");
                xhr.send();
                window.location = '../reunion/' + my_name + "/";
            }
        });
    });  


});