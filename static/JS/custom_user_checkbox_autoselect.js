$(document).ready( function(){

    // Select/deselect every instance of user checkbox for the same user when selecting/deselecting
    $('#userSelectionFormRole').children('li').children('div').children('div').children('label').click(function(event){

        // When clicking on the label the code runs twice -> Once for the "label" element and once for the "input" element for the checkbox
        // inside of the label
        // When clicking on the checkbox only the "input" element eventlistener triggers
        // When doing this we filter out the "label" event trigger so it only runs once every time
        // Plus we dont have to change code for "input" and "label" element event trigger
        if($(event.target).prop('nodeName') != 'INPUT'){
            return;
        }

        let target = $(event.target).parent().parent(); //The label element

        // gets all checkbox lines with the same user info (included the one clicked)
        let usersWithSameText = $('#userSelectionFormRole').children('li').children('div').children('div').children('label').filter(function(){
            return $(this).text().trim() == target.text().trim();
        });

        // checks/unchecks all the users with the same info the same way the clicked one was supposed to be checked/unchecked
        // this works because the checking / unchecking happens before the event is triggered
        usersWithSameText.children('div').children(':checkbox').prop('checked',target.children('div').children(':checkbox').prop('checked'));



        // if unchecked -> uncheck the role checkbox
        // do this with every rolebox that contains an element which was changed (usersWithSameText)
        if(!target.children('div').children(':checkbox').prop('checked')){
            usersWithSameText.parent().parent().parent().children('label').children('div').children(':checkbox').prop('checked',false);
        }

        // if checked -> see if every other user of every role is checked and check the role checkbox
        else if(target.children('div').children(':checkbox').prop('checked')){
            // one loop for every role there is
            for (let index = 0; index < ($('#userSelectionFormRole').children('li')).length; index++){

                let liArray = $('#userSelectionFormRole').children('li'); // just for cleaner code

                let roleLabel = $(liArray[index]).children('label');
                let roleUserlistLabels = $(liArray[index]).children('div').children('div').children('label');

                // if roleLabel is already checked -> all users are already selected -> no need to check
                // only do something if it isnt checked
                if(!roleLabel.children('div').children(':checkbox').prop('checked')){
                    // check if all users are checked
                    let allAreChecked = true;
                    let a = 0;
                    while (allAreChecked && a<roleUserlistLabels.length){
                        allAreChecked = $(roleUserlistLabels[a]).children('div').children(':checkbox').prop('checked');
                        a++
                    }

                    // change role checkbox to the result of allAreChecked
                    roleLabel.children('div').children(':checkbox').prop('checked',allAreChecked);
                }
            }
        }



    });

    // Select/Deselect all when checkmarking the role
    $('#userSelectionFormRole').children('li').children('label').click(function(event){

        // When clicking on the label the code runs twice -> Once for the "label" element and once for the "input" element for the checkbox
        // inside of the label
        // When clicking on the checkbox only the "input" element eventlistener triggers
        // When doing this we filter out the "label" event trigger so it only runs once every time
        // Plus we dont have to change code for "input" and "label" element event trigger
        if($(event.target).prop('nodeName') != 'INPUT'){
            return;
        }


        let target = $(event.target).parent().parent(); // the label element, not checkbox input element

        // label elements for every user under that role
        let roleUsers = target.parent().children('div').children('div').children('label');  

        let usersWithSameTextAsRoleUsers = $('#userSelectionFormRole').children('li').children('div').children('div').children('label').filter(function(){
            
            let hasSameText = false;            
            let a=0

            while(!hasSameText && a<roleUsers.length){                
                hasSameText = $(this).text().trim() ==  $(roleUsers[a]).text().trim();
                a++;
            }
            return hasSameText;
        });

        roleUsers.children('div').children(':checkbox').prop('checked', target.children('div').children(':checkbox').prop('checked'));

        usersWithSameTextAsRoleUsers.children('div').children(':checkbox').prop('checked',target.children('div').children(':checkbox').prop('checked'));
        
    });
});