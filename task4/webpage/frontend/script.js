// Get html elements for operating with them.
const imageContainer1 = document.getElementById("imageCont1");
const imageContainer2 = document.getElementById("imageCont2");
const imageContainer3 = document.getElementById("imageCont3");
const CNN_result = document.getElementById("cnn_result");
const result_element = document.getElementById("result")

// Base api URL for API requests.
const baseApiUrl = "http://127.0.0.1:5000";

/**
 * Event initializing listeners for the different images. When clicked a method
 * gets called which evaluates the image which got clicked with the CNN
 */
imageContainer1.addEventListener("click", () => {
    selectPicture(1);
})

imageContainer2.addEventListener("click", () => {
    selectPicture(2);
})

imageContainer3.addEventListener("click", () => {
    selectPicture(3);
})

/**
 * Gets called when a image is clicked. Sends the id of the picture to the backend where it gets evaluated
 * and the result gets displayed on the webpage.
 *
 * @param i The id (1-3) of the image clicked.
 */
function selectPicture(i) {
    fetch(`${baseApiUrl}/api/picture?id=${i}`).
    then(response => response.json())
        .then(data => {
            // Results gets assigned to the html element.
            result_element.innerText = data.result;
        })
        .catch(error => {
            console.error("Error:", error);
        });

}

/**
 * This method gets called when the reload images button is pressed and reloads the 3 images.
 */
function getPictures() {
    fetch(`${baseApiUrl}/api/pictures`)
        .then(response => response.json())
        .then(data => {
        console.log(data)
            const [picture1, picture2, picture3] = data.selected_images;
            // Create <img> elements for each picture
            const image1 = document.createElement("img");
            image1.src = picture1;

            const image2 = document.createElement("img");
            image2.src = picture2;

            const image3 = document.createElement("img");
            image3.src = picture3;

            // Remove and append these images to separate <div> elements in your HTML
            imageContainer1.removeChild(imageContainer1.firstChild);
            imageContainer2.removeChild(imageContainer2.firstChild);
            imageContainer3.removeChild(imageContainer3.firstChild);
            imageContainer1.appendChild(image1);
            imageContainer2.appendChild(image2);
            imageContainer3.appendChild(image3);
        })
        .catch(error => {
            console.error("Error:", error);
        });
}