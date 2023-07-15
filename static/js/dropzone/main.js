Dropzone.autoDiscover=false;
const myDropzone= new Dropzone('#myDropzone',{
    url:'upload/',
    maxFiles:5,
    maxFilesize:5,
    //acceptedFiles:'.jpg',
})