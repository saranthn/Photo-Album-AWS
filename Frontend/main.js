function search()
{
	var searchBox = document.getElementsByClassName('searchbar')[0];
	console.log(searchBox.value);

	if (!searchBox.value)
	{
		alert('Please enter a valid text');
	}
	else
	{
		getPhotos(searchBox.value.trim().toLowerCase());
	}
}

function getPhotos(text)
{
	document.getElementsByClassName('searchbar')[0].value = '';

 	var sdk = apigClientFactory.newClient({ apiKey: "yIrpNJShAv4XL3TBzPzt8y9FphCht9v1DDOuVl5d" });

    sdk.searchGet({ q: text, "x-api-key": "yIrpNJShAv4XL3TBzPzt8y9FphCht9v1DDOuVl5d"})
    	.then(function(result) {
    		console.log(result['data']['results']);

    		var photo_results = result['data']['results'];

            if (photo_results.length == 0)
            {
                alert("No images found for your search");
            }

    		var photosDiv = document.getElementById('photos_results');
    		photosDiv.innerHTML = "";

    		for (var i=0; i<photo_results.length; i++)
    		{
    			console.log(photo_results[i]['url']);
    			photosDiv.innerHTML += "<figure><img src=" + photo_results[i]['url'] + " style='width:25%'></figure>"
    		}
    	}).catch(function(result){
    		console.log(result);
    	});
}

function upload()
{
	var filePath = (document.getElementById('uploaded_file').value).split("\\");
    var fileName = filePath[filePath.length - 1];
    var fileExt = fileName.split(".").pop();
    
    if (!document.getElementById('custom_labels').innerText == "") {
        var customLabels = document.getElementById('custom_labels');
    }
    console.log(fileName);
    console.log(custom_labels.value);

    var file = document.getElementById("uploaded_file").files[0];
    file.constructor = () => file;

    console.log(file.type);

    var sdk = apigClientFactory.newClient({ apiKey: "yIrpNJShAv4XL3TBzPzt8y9FphCht9v1DDOuVl5d" });

    var params = {
        'x-amz-meta-customLabels': custom_labels.value,
        "filename": fileName,
        "bucket": "photos-st3523",
        //'x-amz-meta-customLabels': {"labels": custom_labels.value},
        //'x-amz-meta-customabels': custom_labels.value,
        "x-api-key": "yIrpNJShAv4XL3TBzPzt8y9FphCht9v1DDOuVl5d"
    };

    var additionalParams = {
        headers: {
            //'x-amz-meta-customLabels': custom_labels.value,
            'Content-Type': file.type,
            //'policy': ["starts-with", "$x-amz-meta-customLabels", ""]
        }
    };

    var reader = new FileReader();
    reader.onload = function (event) {
        body = btoa(event.target.result);
        //console.log('Reader body : ', body);
        return sdk.uploadBucketFilenamePut(params, file, additionalParams)
        .then(function(result) {
            console.log(result);
            alert('Image uploaded successfully')
        })
        .catch(function(error) {
            console.log(error);
        })
    }
    reader.readAsBinaryString(file);

    document.getElementById('uploaded_file').value = "";
    document.getElementById('custom_labels').value = "";

    // var url = "https://wajuqrne5c.execute-api.us-east-1.amazonaws.com/v1/upload/photos-st3523/duck.jpeg"
    // axios.put(url, file, params).then(response => {
    //     alert("Image uploaded: " + file.name);
    // })
    // .catch(function(error) {
    //     console.log(error);
    // });   
}

window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition

function interpretVoice()
{
    if ('SpeechRecognition' in window) {
        console.log("SpeechRecognition is Working");
    } else {
        console.log("SpeechRecognition is Not Working");
    }

    var searchBox = document.getElementsByClassName('searchbar')[0];
    const recognition = new window.SpeechRecognition();

    mic = document.getElementById("switch");  
    
    if (mic.innerHTML == "micOn") {
        recognition.start();
    } else if (mic.innerHTML == "micOff"){
        recognition.stop();
    }

    console.log("reached")

    recognition.addEventListener("start", function() {
        console.log("reached")

        mic.innerHTML = "micOff";
        console.log("Recording.....");
    });

    recognition.addEventListener("end", function() {
        console.log("Stopping recording.");
        mic.innerHTML = "micOn";
    });

    recognition.addEventListener("result", resultOfSpeechRecognition);
    function resultOfSpeechRecognition(event) {
        const current = event.resultIndex;
        transcript = event.results[current][0].transcript;
        searchBox.value = transcript;
        console.log("transcript : ", transcript)
    }
}














