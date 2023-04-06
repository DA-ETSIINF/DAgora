
$(document).ready(function () {

    // When starting the page, order the form by Name
    // Should be like that automatically, but there are errors if the first name starts with a lowercase letter sometimes
    var divs = $('#id_users').find('div').toArray();
    divs.sort(function(a, b) {
        return $(a).text().toUpperCase().localeCompare($(b).text().toUpperCase());
        });
    $('#id_users').empty();
    $.each(divs, function(index, item) {
        $('#id_users').append(divs); 
    });



    // Functions to order the userSelectionForm when pressing the buttons
    $('#RoleButton').click(function(event){
        var divs = $('#id_users').find('div').toArray();
        divs.sort(function(a, b) {
            return $(a).text().toUpperCase().split('-')[2].localeCompare($(b).text().toUpperCase().split('-')[2]);
         });
        $('#id_users').empty();
        $.each(divs, function(index, item) {
            $('#id_users').append(divs); 
        });
    });
    $('#NameButton').click(function(event){
        var divs = $('#id_users').find('div').toArray();
        divs.sort(function(a, b) {
            return $(a).text().toUpperCase().localeCompare($(b).text().toUpperCase());
         });
        $('#id_users').empty();
        $.each(divs, function(index, item) {
            $('#id_users').append(divs); 
        });
    });
    $('#ClassButton').click(function(event){
        var divs = $('#id_users').find('div').toArray();
        divs.sort(function(a, b) {
            return $(a).text().toUpperCase().split('-')[1].localeCompare($(b).text().toUpperCase().split('-')[1]);
         });
        $('#id_users').empty();
        $.each(divs, function(index, item) {
            $('#id_users').append(divs); 
        });

    });

    /*$('#reunionname').click(function(event){
        var formArray = $('#id_users').find('div').toArray();
        var divs = $('#id_users').find('div').toArray();
        var objects = [];
        });*/



    
  });


