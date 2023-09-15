$(document).ready(function(){
    
    let dropdown_button = $('#dropdown_button');
    let dropdown_content = $('#dropdown_content');

    dropdown_button.click(function(event){
        dropdown_content.toggle("show");
    });
});