// File for the confirm_attendance buttons on the meeting info page
// Using ajax they send a signal to the view where the attendance is changed on the database
// Plus it changes the will attend / won't attend text displayed on the site so the user doesnt have to reload the whole site




$(document).ready(function(){
    $('#attendance_buttons').children('input').click(function(event){
        event.preventDefault();

        let attendance; 

        // Check which button was pressed
        if($('#attendance_true').is(':focus')){
            attendance = true;
        }
        else if($('#attendance_false').is(':focus')){
            attendance = false;
        }

        var url = '';
        var data = {
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
          'attendance': attendance
        };

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            success: function (data) {
                // change will assist / won't assist text on page uppon success of sending data via ajax

                // Every user info display has the class .user_info and the value of its id in the database -> check for all the user info labels with the same id/value
                let targets = $('.user_info').filter(function(){
                    return $(this).val() == $('#my_user').children('label').children('.user_info').val();
                });
                
                if(attendance == true){
                    var AttendanceText = " - will attend";
                }
                else{
                    var AttendanceText = " - won't attend";
                }

                // change the text content for every target
                for (let i=0; i<targets.length; i++){
                    let target = $(targets[i]);
                    let text = target.text().split('-');
                    text.pop();
                    text = text.join('-').trim() + AttendanceText;
                    target.text(text);            
                  }
            }
          });
    })
});