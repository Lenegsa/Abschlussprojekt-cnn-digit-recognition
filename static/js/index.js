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

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    context.beginPath();
    context.moveTo(x, y);
    event.preventDefault();
}

function draw(event) {
    if(is_drawing) {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        context.lineTo(x, y);
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

//HTML elements
const predictedNumber = document.getElementById('predicted-number');
const confidence = document.getElementById('confidence');
const visImg = document.getElementById('visualization-img');
const greyscaleImage = document.getElementById('greyscale-img');
const visualizationFeaturemap = document.getElementById('visualization-featuremap');
const emojiElement = document.getElementById('confidence-emoji');
const confidenceMessage = document.getElementById('confidence-message')


function clear_canvas(){
    context.fillStyle = start_background_color;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillRect(0, 0, canvas.width, canvas.height);
    predictedNumber.innerText = "-";
    confidence.innerText = "-";
    visImg.innerHTML = "";
    greyscaleImage.innerHTML = ""; 
    visualizationFeaturemap.innerHTML = "";
    emojiElement.innerText = '😊';
    confidenceMessage.innerText = "I'm waiting for your number....";

}

//communicate with server AJAX = Asynchronous JavaScript And XML.

const layers_images = [];

//waiting 
function waiting (boolean){
    //set the corsor wait
    if(boolean){
     document.body.style.cursor = 'wait';

    //show waiting image and text
     greyscaleImage.innerHTML = `<h6>I am working. Please wait.</h6>
     <img src="/static/images/wait.jpg" class="img-fluid rounded mx-auto d-block" alt="Waiting"></img>`;
    
    //disable buttons, so that we cannot send a new request
     document.getElementById('predict').disabled = true;
     document.getElementById('clear').disabled = true;
    }
    else{

    //set back the cursor
    document.body.style.cursor = 'default';

    // enable buttons
    document.getElementById('predict').disabled = false;
    document.getElementById('clear').disabled = false;
    }  
}

//show confidence emoji
function showConfidenceEmoji(confidence, prediction){
    
    // chose a emoji
    if (confidence >= 95) {
        emojiElement.innerText = '😎'; 
        confidenceMessage.innerText = "I'm sure it's this: " + prediction;  
    } else if (confidence >= 80) {
        emojiElement.innerText = '😊'; 
        confidenceMessage.innerText = "I'm not sure, but maybe : " + prediction;
    } else if (confidence >= 60) {
        emojiElement.innerText = '🙂'; 
        confidenceMessage.innerText = "I guess it's a: " + prediction;
    } else if (confidence >= 40) {
        emojiElement.innerText = '🤔';
        confidenceMessage.innerText = "It's hard, but maybe : " + prediction;  
    } else {
        emojiElement.innerText = '😕'; 
        confidenceMessage.innerText = "Are you sure that's a number?"; 
    } ;
}

function sendImage(){

    waiting(true);

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
    predictedNumber.innerText = data.prediction;
    showConfidenceEmoji(data.confidence, data.prediction);
    confidence.innerText = `${data.confidence.toFixed(2)}`;

    //visulaisation
    //prediction image
    visImg.innerHTML =
    `<img src= ${data.visualisation} class="img-fluid" alt="greyscaleImage" />`;

    //predicted greyscale image
    greyscaleImage.innerHTML =
    `<img src= ${data.greyscaleImage} class="img-fluid" alt="greyscaleImage" />`;

     //greyscale images
    visualizationFeaturemap.innerHTML =
    `<h6>First layer (convolutional, yellow)</h6>
     <img src= ${data.firstLayerConv2d} class="img-fluid" alt="firstLayerConv2d" />
     <hr>
     <br>
     <h6>Second layer (max pooling, red)</h6>
     <img src= ${data.secondLayerMaxPool2d} class="img-fluid" alt="secondLayerMaxPool2d" />
     <hr>
     <br>
     <h6>Third layer (convolutional, yellow)</h6>
     <img src= ${data.thirdLayerConv2d} class="img-fluid" alt="thirdLayerConv2d" />
     <hr>
     <br>
     <h6>Fourth layer (convolutional, yellow)</h6>
     <img src= ${data.fourthLayerConv2d} class="img-fluid" alt="fourthLayerConv2d" />
     <hr>
     <br>
     <h6>Fifth layer (max pooling, red)</h6>
     <img src= ${data.fifthLayerMaxPool2d} class="img-fluid" fifthLayerMaxPool2d" />
     <hr>
     <br>
     <h6>Sixth layer (convolutional, yellow)</h6>
     <img src= ${data.sixthLayerConv2d} class="img-fluid" alt="sixthLayerConv2d" />
     <hr>
     <br>
     <h6>Seventh layer (convolutional, yellow)</h6>
     <img src= ${data.seventhLayerConv2d} class="img-fluid" alt="eventhLayerConv2d" />
     <hr>
     <br>
     <h6>Eighth layer (max pooling, red)</h6>
     <img src= ${data.eighthLayerMaxPool2d} class="img-fluid" alt="eighthLayerMaxPool2d" />`
    ;

    waiting(false);

})
.catch(error => {
    console.error('Error:', error);
});
    
}

