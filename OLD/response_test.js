const fetch = require('node-fetch');	//npm install node-fetch


// GET Request.
fetch('https://blooming-savannah-44967.herokuapp.com/https://api-29-seconds.herokuapp.com/api', {method: "POST", headers: {"difficulty": "1", "category": "anime"}})
    // Handle success
    .then(response => response.json())  // convert to json
    .then(json => console.log(json))    //print data to console
    .catch(err => console.log('Request Failed', err)); // Catch errors