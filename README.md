# DAgora

La DAgora es un projecto con la finalidad de crear una forma para la DA de tener un sistema que permita llevar las reuniones / JDs de forma más ordenada
y más sencilla para todos los miembros, con su función principal siendo permitir a los miembros de la DA de poder marcar su asistencia / avisar si van a asistir
o no a la reunión por adelantado, para así permitir a los organizadores de la reunión tener más facilidad a la hora de organizarla, en vez de tener que mandar varios 
whatsapps y forms.

El projecto es una web API que utiliza Django, una backend de python, pero también utiliza JQuery de javascript para mejorar la comodidad y efectividad de la pagina.

El projecto consiste en varias partes:
- 
- Un sistema de Login:

    Los usuarios no podrán acceder a ninguna parte de la página sin verificarse. Algunos usuarios también tendrán más permisos que otros (como por ejemplo el permiso para crear 
    reuniones), lo cual se implementará utilizando el sistema de grupos de Django. 
  
 - La página principal:
  
    La página principal será donde los usuarios puedan ver la información de su perfil junto con una lista de todas las reuniones a las que han sido o están siendo 
    convocados. Al pulsar las reuniones te redirige a la pagina de información de la reunión.
  
 - Páginas de información sobre las reuniones:
  
    Cada reunion tendrá su propia pagina ("/<nombre de la reunión>") donde el usuario podrá ver la información básica de la reunión junto con la lista de miembros convocados.
    A parte, también es esa la página donde los usuarios podrán avisar de si van a asistir o no a la reunión.

    Los miembros con los permisos necesarios también podrán editar la información de la reunión, borrarla, o subir archivos.
  
 - Pagina de creación de reuniones:
 
    Esta es la pagina donde los usuarios con los permisos necesarios podrán crear reuniones. Consiste primero en una form simple que permita al creador de definir la
    información básica de la reunión (nombre, fecha, descripción) y en una lista seleccionable de usuarios, donde el creador puede filtrar usuarios por distintas 
    características y seleccionar a que usuarios convocar a la reunión.

    Al darle al botón de crear reunión el usuario será deredigido a la pagina de información de la nueva reunión.
    
    
Funcionalidad:
-
- Para los perfiles actualmente se está utilizando el sistema de perfiles de django, pero se ha ampliado para añadir a cada Usuario los atributos de clase/curso y
rol dentro de la delegación, con el fin de facilitar la selección de convocados a la hora de crear nuevas reuniones. 

  El codigo para esto consiste en una nueva clase 'UserProfile' con esos atributos la cual luego se añade como extensión a la clase 'User' que viene con Django.
  Todo esto se encuentra dentro de la carpeta 'custom_profiles'.

- Hay un sistema muy básico de login de django. 

  Django automaticamente busca un login.html de login dentro de la carpeta templates/registration para crear la pagina de login, así que en caso de edición solo 
  hay que tocar eso

- Para ver que usuarios han sido convocados a que reuniones se usa el objeto "Attendance". Se ha creado una nueva clase 'Attendance' con una oneToOne relationship 
con el usuario y la reunión. Basicamente, por cada usuario convocado por reunión se crea uno de estos objetos el cual vincula al usuario a la reunión. Además es este
objeto el que tiene el atributo de la asistencia y guarda la información sobre si el usuario va a asistir a la reunión o no.

  El codigo para todo esto está en la carpeta de 'reuniones'.
  
- Todas las views / El codigo sobre las principales páginas se encuentra en 'reuniones/view'


Cosas que faltan:
 -
 - Un sistema para subir archivos a la hora de crear la reunión
 - Toda la parte que permite a ciertos usuarios editar la información de la reunión en la pagina de información
    - Crear página de edición ("/&lt;nombre>/edit"?)
    - Añadir botón visible solo por ciertos usuarios que lleve a la pagina de edición 
 - Añadir el sistema de permisos que permita darle a ciertos usuarios ciertos poderes
 - Implementar sistema de notificaciónes
    - Objectivo: En la página principal que esté señalizado a los usuarios si no han entrado a la pagina de información de la reunión desde su creación o su ultima
    edición
    - → Implementar atributo de fecha de creación / edición a la clase "Reunion"
    - → Implementar atributo de fecha de visita a la clase "Attendances"
 -  Implementar usuarios UPM oficiales (todavía no se puede hacer)
 
 
  
  
