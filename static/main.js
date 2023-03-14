Dropzone.autoDiscover=false;
const myDropzone= new Dropzone('#my-dropzone',{
    url:'upload/',
    maxFiles:5,
    maxFilesize:5,
    //acceptedFiles:'.jpg',
})