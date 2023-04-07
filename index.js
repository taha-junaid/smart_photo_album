$(document).ready(function () {
    var submitButton = document.querySelector('.submit-button');

    // Add an event listener to the submit button
    submitButton.addEventListener('click', function () {
        var file = document.getElementById('uploaded_file').files[0];
        var customLabels = document.getElementById("custom_labels");
        // console.log(custom_labels.value);
        var reader = new FileReader();

        reader.onload = function (event) {//
            // var body = btoa(event.target.result.replace(/^data:(.*;base64,)?/, ''));
            var body = event.target.result;
            // console.log(body);
            // console.log(file.type);
            var filename = Date.now() + file.name
            // console.log(filename)
            var params = {
                'bucket': 'pictures-assignment2',
                'filename': filename,
                'Content-Type': file.type,
                'x-amz-meta-customLabels': customLabels.value,
            };
            sdk.bucketFilenamePut(params, body, {})
                .then(function (res) {
                    if (res.status == 200) {
                        alert(filename, "IMAGE UPLOADED!!")
                    }
                });
        }
        reader.readAsDataURL(file);
    }, false);

    // ---------------------------------------------- audio search ------------------------------------------------------
    window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition
    if ('SpeechRecognition' in window) {
        console.log("SpeechRecognition is Working");
    } else {
        console.log("SpeechRecognition is Not Working");
    }

    var inputSearchQuery = document.getElementById("search_query");
    const recognition = new window.SpeechRecognition();
    //recognition.continuous = true;

    micButton = document.getElementById("mic_search");

    micButton.addEventListener('click', function () {
        if (micButton.innerHTML == "mic") {
            recognition.start();
        } else if (micButton.innerHTML == "mic_off") {
            recognition.stop();
        }

        recognition.addEventListener("start", function () {
            micButton.innerHTML = "mic_off";
            console.log("Recording.....");
        });

        recognition.addEventListener("end", function () {
            console.log("Stopping recording.");
            micButton.innerHTML = "mic";
        });

        recognition.addEventListener("result", resultOfSpeechRecognition);
        function resultOfSpeechRecognition(event) {
            const current = event.resultIndex;
            transcript = event.results[current][0].transcript;
            inputSearchQuery.value = transcript;
            console.log("transcript : ", transcript)
        }
    });

    // ---------------------------------------------- get search results ------------------------------------------------------

    var searchPhotosButton = document.getElementById('searchPhotos');
    var searchResultsDiv = document.getElementById('searchResults');

    searchPhotosButton.addEventListener('click', function () {
        
        async function fetchImages() {
            console.log(inputSearchQuery.value)
            var params = {
                'q': inputSearchQuery.value
            };
            try {
                const response = await sdk.searchGet(params, {}, {});
                // console.log(response);
                // testArr = ["https://pictures-assignment2.s3.amazonaws.com/1679631501092cat4.jpeg", "https://pictures-assignment2.s3.amazonaws.com/1679631501092cat4.jpeg", "https://pictures-assignment2.s3.amazonaws.com/1679631501092cat4.jpeg"]
                for (const imageUrl of response['data']['data']) {
                // for (const imageUrl of testArr) {
                    const imageResponse = await fetch(imageUrl);
                    if (!imageResponse.ok) {
                        throw new Error('Network response was not ok.');
                    }
                    const img = document.createElement('img');
                    img.src = await imageResponse.text();
                    searchResultsDiv.innerHTML = '';
                    searchResultsDiv.appendChild(img);
                }
            } catch (error) {
                console.log(error);
            }
        }

        fetchImages();
    });

});
