// get the Canvas element
const canvas = document.getElementById('canvas');

// canvas width and height
canvas.width = 280;
canvas.height = 280;

let context = canvas.getContext('2d'); // 2D
let start_background_color = "white";
context.fillStyle = start_background_color; // set background color white
context.fillRect(0, 0, canvas.width, canvas.height); // fill the background


let draw_color = "black";
let draw_width = "25";
let is_drawing = false;

//touch
canvas.addEventListener("touchstart", start, false);
canvas.addEventListener("touchmove", draw, false);
canvas.addEventListener("touchend", stop, false);

//mouse
canvas.addEventListener("mousedown", start, false);
canvas.addEventListener("mousemove", draw, false);
canvas.addEventListener("mouseup", stop, false);
canvas.addEventListener("mouseout", stop, false);


function start(event) {
    is_drawing = true;
    context.beginPath();
    context.moveTo(event.clientX - canvas.offsetLeft,
        event.clientY - canvas.offsetTop);
    event.preventDefault();
}

function draw(event) {
    if(is_drawing) {
        context.lineTo(event.clientX - canvas.offsetLeft,
            event.clientY - canvas.offsetTop);
        context.strokeStyle = draw_color;
        context.lineWidth = draw_width;
        context.lineCap = "round";
        context.lineJoin = "round";
        context.stroke();
    }
    event.preventDefault();
}

function stop(event) {
    if(is_drawing) {
        context.stroke();
        context.closePath();
        is_drawing = false;
    }
    event.preventDefault();
}

const result = document.getElementById('result');
const confidence = document.getElementById('confidence');
const visImg = document.getElementById('visualization-img');
const greyscaleImage = document.getElementById('greyscale-img');
const visualizationFeaturemap = document.getElementById('visualization-featuremap');

function clear_canvas(){
    context.fillStyle = start_background_color;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillRect(0, 0, canvas.width, canvas.height);
    result.innerText = "-";
    confidence.innerText = "-";

}

//communicate with server AJAX = Asynchronous JavaScript And XML.

const layers_images = [];

function sendImage(){
   const imageDataURL = canvas.toDataURL('image/png'); //base64 String

   fetch('/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        image: imageDataURL
    })
})
.then(response => response.json())
.then(data => {
    // Server response
    console.log('Prediction:', data.prediction);
    console.log('Confidence values:', data.confidence);
    console.log('ImageSrc:', data.visualisation );
    console.log('GreySaleSrc:', data.greyscaleImage);
    console.log(data.firstLayerConv2d);


    //Show the result
    result.innerText = data.prediction;
    confidence.innerText = `${data.confidence.toFixed(2)}%`;

    //visulaisation
    //prediction image
    visImg.innerHTML =
    `<img src= ${data.visualisation} />`;

    //predicted greyscale image
    greyscaleImage.innerHTML =
    `<img src= ${data.greyscaleImage} />`;

     //greyscale images
    visualizationFeaturemap.innerHTML =
    `<img src= ${data.firstLayerConv2d} />
     <img src= ${data.secondLayerMaxPool2d} />
     <img src= ${data.thirdLayerConv2d} />
     <img src= ${data.fourthLayerConv2d} />
     <img src= ${data.fifthLayerMaxPool2d} />
     <img src= ${data.sixthLayerConv2d} />
     <img src= ${data.seventhLayerConv2d} />
     <img src= ${data.eighthLayerMaxPool2d} />`
   
    ;
})
.catch(error => {
    console.error('Error:', error);
});
    
}

