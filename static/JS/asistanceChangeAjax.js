$(document).ready(function () {
    $('.AsistButton').click(function (event) {

      event.preventDefault();
  
      var trueAsist = $('#trueAsist').val();
      var falseAsist = $('#falseAsist').val();
      var asistValue;

      // Mira que botón se ha pulsado y mete su valor en la var asistValue
      if ($('#trueAsist').is(':focus')) {
        asistValue = trueAsist;
      } else if ($('#falseAsist').is(':focus')) {
        asistValue = falseAsist;
      }
  
      var url = '';
      var data = {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'asistValue': asistValue
      };
  
      $.ajax({
        url: url,
        method: 'POST',
        data: data,
        success: function (data) {
          // codigo jquery para cuando se manda la request correctamente
          // aquí es donde se cambia el texto / contenido de la pagina al pulsar los botones
          // no se actualiza el contenido de la database

          //definir que botones tienen el mismo text -> el mismo id en el value
          var textTargets = $('.user_info').filter( function(){
            return $(this).val() == $('#myUser').children('label').children('li').val();
          });

          // Definir que texto tienenn que tener => Nombre - clase - will attend / will not attend
          var text = $('#myUser').children('label').children('li').prop('innerText');
          text = text.trim();
          text = text.split('-');          
          var newText = '';
          newText = text[0].trim() + ' - ' + text[1].trim();

          if(asistValue == 'True'){
            newText += ' - will attend'
          }
          else if(asistValue == 'False'){
            newText += ' - will not attend'
          }

          // coge cada li del usuario que ha pulsado el boton y le cambia el texto al nuevo
          for (let i=0; i<textTargets.length; i++){
            var textTarget = $(textTargets[i]);
            textTarget.text(newText);            
          }
        }
      });
    });
  });