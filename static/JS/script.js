






// NOT BEING USED CURRENTLY!


























































// name_field code so the content of the field doesnt get refreshed with every POST/GET Method or reload

//We want to call the load button before the reset button so when we do arrow back from a different url the content is clear 
// (and so it's less probable we accidentaly register the same code twice)

window.addEventListener("load", function(){
  let name_field_value = sessionStorage.getItem("name_field_value");
  console.log(name_field_value);
  if (name_field_value) {
    document.getElementById("name_field").value = name_field_value;
  }
});

document.getElementById("name_field").addEventListener("input", function(){
    sessionStorage.setItem("name_field_value", this.value);
});



// date_field code so the content of the field doesnt get refreshed with every POST/GET Method

window.addEventListener("load", function(){
  let date_field_value = sessionStorage.getItem("date_field_value");
  console.log(date_field_value);
  if (date_field_value) {
    document.getElementById("date_field").value = date_field_value;
  }
});

document.getElementById("date_field").addEventListener("input", function(){
    sessionStorage.setItem("date_field_value", this.value);
});


// description_field code so the content of the field doesnt get refreshed with every POST/GET Method

window.addEventListener("load", function(){
  let description_field_value = sessionStorage.getItem("description_field_value");
  console.log(description_field_value);
  if (description_field_value) {
    document.getElementById("description_field").value = description_field_value;
  }
});

document.getElementById("description_field").addEventListener("input", function(){
    sessionStorage.setItem("description_field_value", this.value);
});




// Code so the content of the different fields does get reset when pressing the button
  // code for name_field
document.getElementById("reunionname").addEventListener("click", function() {
  sessionStorage.setItem("name_field_value", '');
});
  // code for date_field
document.getElementById("reunionname").addEventListener("click", function() {
  sessionStorage.setItem("date_field_value", '');
});
  // code for description_field
document.getElementById("reunionname").addEventListener("click", function() {
  sessionStorage.setItem("description_field_value", '');
});

