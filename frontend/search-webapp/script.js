const dropArea = document.getElementById('dropArea');
const uploadButton = document.querySelector('label[for="fileToUpload"]');
const fileUploadButton = document.getElementById('fileToUpload');
const fileNameSpan = document.getElementById('fileName');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropArea.classList.add('highlight');
}

function unhighlight(e) {
    dropArea.classList.remove('highlight');
}

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    document.getElementById('fileToUpload').files = files;
    // console.log("------------")
    // console.log(files)
    // console.log("------------")

    handleFiles(files);
}

fileUploadButton.onchange = function() {
    const files = document.getElementById('fileToUpload').files;
    handleFiles(files);
}

// function handleFiles(files) {
//     console.log(files.length)
//     for (let i = 0; i < files.length; i++) {
//         const file = files[i];
//         console.log('File:', file);
//         // You can perform further actions with the dropped files here
//     }
// }

function handleFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        console.log('File:', file);
        fileNameSpan.textContent = file.name;
        fileInfo.style.display = 'block';
        dropArea.style.display = 'none';
    }
}

function uploadFiles(e) {
    const files = document.getElementById('fileToUpload').files;
    console.log(files);
    fileInfo.style.display = 'none';
    dropArea.style.display = 'block';
    console.log(files);
}