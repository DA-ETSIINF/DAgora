$(document).ready(function () {
    $('#attendanceForm').submit(function (event) {
      event.preventDefault();
  
      var trueAsist = $('#trueAsist').val();
      var falseAsist = $('#falseAsist').val();
      var asistValue;

      // Mira que botón se ha pulsado y mete su valor en la var asistValue
      if ($(this).find('#trueAsist').is(':focus')) {
        asistValue = trueAsist;
      } else if ($(this).find('#falseAsist').is(':focus')) {
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

          var currentText = $(".myUser").children(".userli").text();
          var updatedText = currentText.replace('will attend', '').replace('wont attend', '');
          
          if (asistValue == 'True'){
            updatedText += 'will attend';
          }
          else if (asistValue == 'False'){
            updatedText += 'wont attend';
          }
          
          $(".myUser").children(".userli").text(updatedText);

        }
      });
    });
  });