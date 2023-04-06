$(document).ready(function () {
    // add eventlistener to lables
    // every label is inside of a automatically created div with the id "id_users"

    var selectedUsers = [];
    
    $('#userByRolesForm').children("#userForm").mouseup(function(event){
        setTimeout(function(){
                
            var targetedUserDiv = $(event.target).parent();
            if ( targetedUserDiv.children('label').text() == ""){
                return;
            }
            var userInfo = targetedUserDiv.children('label').text();

            console.log(userInfo);

            if((jQuery.inArray(userInfo, selectedUsers)) == -1){
                selectedUsers.push(userInfo);
            }

            if(targetedUserDiv.children('label').children(':checkbox').prop('checked')){
                console.log('A');
                //selectedUsers = jQuery.grep(selectedUsers, function(value){
                //    return value != userInfo;
                //});
            }
            
            // cleans the whole window
            $('#userByRolesForm').children("li").children('div').children('div').children('label').filter( function(){
                return jQuery.inArray($(this).text(), selectedUsers) == -1;
            }).children(':checkbox').prop('checked',false);


            $('#userByRolesForm').children("li").children('div').children('div').children('label').filter(function(){
                return jQuery.inArray($(this).text(), selectedUsers) != -1;
            }).children(':checkbox').prop('checked', true);


        }, 1);
    });
});