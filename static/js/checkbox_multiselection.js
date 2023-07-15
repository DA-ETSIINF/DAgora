// This file tries to solve a problem there is with the checkboxes when selecting users in the meeting creation / edition page:
// A user can have multiple roles, and therefore can appear multiple times
// When we selec an user we want him to be selected in all roles, and not just the one where we selected him
// Because we dont want an user to appear both selected and not selected at the same time
// Extra: We can add a checkbox to the roles, that when pressed selects all user of its role

// To do this we can change the 'checked' proprety of a 'checkbox' item of the html to true or false based on the name on its label

//Auxiliary functions:

function has_same_user(label1,label2){ //Only for user checkboxes, not roles
    // The imputs(checkboxes) inside of the user labels have the user id as their value
    return label1.find('input').val() == label2.find('input').val();
}

function user_id(label){
    return label.find('input').val();
}

function check(label, checked_val){ //expects a boolean, true if you want to check, false if you want to uncheck
    label.find('input').prop('checked',checked_val);
}

function check_all_users_with_same_id(target){
    // find all labels with the same users
    let labels_of_same_user = $('#user_selection').children('li').children('div').children('div').children('label').filter(function(){ // includes the target
        return has_same_user($(this), target);
    });

    // Check/Uncheck all labels of same users
    for(let i=0;i<labels_of_same_user.length;i++){
        check($(labels_of_same_user[i]), target.find('input').prop('checked'));
    };
}

function role_users_checked(role_label){ // return true if all users have been checked, false if not
    let user_labels = role_label.parent().children('div').children('div').children('label');
    let result = true;
    for(let i=0;i<user_labels.length;i++){
        if(!$(user_labels[i]).find('input').prop('checked')){
            return false;
        }
    }
    return true;
}

$(document).ready(function(){
    $('#user_selection').children('li').children('div').children('div').children('label').click(function(event){
        // The target if the click event are the labels of users, NOT ROLES

        //When clicking the label the event runs twice -> Once for the 'label' element and once for the 'input' element inside of the label
        //When clicking on the checkbox, which is inside of the label, only the 'input' element event triggers
        //To prevent the event from running twice we filter out the 'label' event trigger
        if($(event.target).prop('nodeName') != 'INPUT'){
            return;
        }

        let target = $(event.target).parent().parent(); // target = label element

        check_all_users_with_same_id(target);


        // Check if all users within a role have been checked!
        let role_labels = $('#user_selection').children('li').children('label');
        for(let i=0;i<role_labels.length;i++){
            $(role_labels[i]).find('input').prop('checked',role_users_checked($(role_labels[i])));
        }

    });
    $('#user_selection').children('li').children('label').click(function(event){
        // The target of the event are the labels of roles, NOT USERS

        if($(event.target).prop('nodeName') != 'INPUT'){
            return;
        }

        let target = $(event.target).parent().parent(); // target = label element of the role
        let users_with_role = target.parent().children('div').children('div').children('label');

        for(let i=0;i < users_with_role.length;i++){
            // First, check all users within the role
            $(users_with_role[i]).find('input').prop('checked', target.find('input').prop('checked'));

            // Then check all users with the same name as them
            check_all_users_with_same_id($(users_with_role[i]));
        }
                
        // Check if all users within a role have been checked!
        let role_labels = $('#user_selection').children('li').children('label');
        for(let i=0;i<role_labels.length;i++){
            $(role_labels[i]).find('input').prop('checked',role_users_checked($(role_labels[i])));
        }
    });
});