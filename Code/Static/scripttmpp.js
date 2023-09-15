window.onload = function() {

  var seconds = 20;
  var rest = true;
  var interval;

  var intervalTime = 20;
  var breakTime = 10;

  var settingsButton = document.getElementById("settings");
  var intervalInput = document.getElementById("intervalTime");
  var breakInput = document.getElementById("breakTime");

  var startButton = document.getElementById("start");
  var pauseButton = document.getElementById("pause");
  var resetButton = document.getElementById("reset");

  var statusHeader = document.getElementById("status");
  var secondsSpan = document.getElementById("sec");

  	// To help you in connecting to the raspberry, the input form value is populated
	// automatically using the current URL
	window_url = window.location.href.split(':')[1].substring(2)
	document.getElementById("raspIP").value = window_url

	// Create a simple line chart
	var data = {
		// A labels array that can contain any sort of values. It will be your x_labels
		labels: [],
		// Our series array that contains series objects or in this case series data arrays
		series: [
			[],[],[]
		]
	};

	// Inside you can pass a number of different options. Commented is one if you want
	// to set a static size.
	var options = {
	//	width: '300px',
	//	height: '200px'
	};

	// In the global name space Chartist we call the Line function to initialize a line chart. 
	// As a first parameter we pass in a selector where we would like to get our chart created (in this case the chart div).
	// To select a div by its ID you use # + div id
	// Second parameter is the actual data object and as a third parameter we pass in our options
	var chart = new Chartist.Line('#chart', data, options);

	// After we create our chart placeholder we need to link the click of the button
	// to some action. 
	var initial_time = -1

  settingsButton.onclick = function() {
    intervalTime = Math.floor(intervalInput.value * 1);
    breakTime = Math.floor(breakInput.value * 1);
    reset();
  }

  startButton.onclick = function() {
    rest = false;
    changeToGo();
    interval = setInterval(countdownSeconds, 1000);
    
    	// The first step is to try and connect to the web socket end point
	// of our server. To know more about web sockets and their purpose
	// consult the readme.md file inside the lab 9 folder.
	ws = new WebSocket('ws://' + document.getElementById("raspIP").value + ':9999/ws');
	var interval = null	
	// When the websocket opens, we will start sending messages requesting
	// data every second
	ws.onopen = function (event) {
		interval = setInterval(function(){
			n = document.getElementById("n_sets").value
			ws.send(JSON.stringify({type:'sendData', n_sets: n}))
			}, 100);
	}


	// This will handle the incoming messages. In this simple example, we just
	// append the message to the data variable until we have the last 60 seconds
	// of data. Afterwards we start to removing the first value.
	ws.onmessage = function (event) {
		msg = JSON.parse(event.data)
		// If condition to set the intial time
		if(initial_time==-1){
			initial_time = msg.timestamp
		}
		
		// The next piece of logic is to keep the size of both array
		// less or equal to 60 points, being a sliding window plot
		if(data.labels.length == 60){
			// If the lenght if already 60, then we remove the first
			// value from each array
			data.labels.shift()
			data.series[0].shift()
                        data.series[1].shift()
                        data.series[2].shift()
		}
		
		// We then append it to the array the received values

		data.labels.push(Math.round(msg.timestamp - initial_time)) 
		data.series[0].push(msg.data[0])
                data.series[1].push(msg.data[1])
                data.series[2].push(msg.data[2])
		
		// We then update the chart with the new data variable..
		chart.update(data)



		//Shows result of classifier
		if(msg.class != 0){
			if(msg.class == 'Others'){
			    document.getElementById("exercise").innerHTML = "<img  src='static/others.png' style = 'width: 10vw'>"
console.log('Others')
			}
			if(msg.class == 'Squats'){
			    document.getElementById("exercise").innerHTML = "<img  src='static/squats.png' style = 'width: 10vw'>"
			}
			if(msg.class == 'Lunges'){
			    document.getElementById("exercise").innerHTML = "<img  src='static/lunges.png' style = 'width: 10vw'>"
			}
			if(msg.class == 'Push Ups'){
			    document.getElementById("exercise").innerHTML = "<img  src='static/pushups.png' style = 'width: 10vw'>"
			}

		}
		
	}
	//

	// This handles any error, like connection drops.
	ws.onclose = function(evt) {
		clearInterval(interval)
		if (evt.code==1006){
			alert('Can not connect to the server.\nIs the raspberry IP correct?\nIs the server running?\nAre you connect to the "PI" network?')
		}
	}
			
  }

  resetButton.onclick = function() {
    reset();
  }

  function reset() {
    clearInterval(interval);
    seconds = intervalTime;
    secondsSpan.innerText = seconds;
    rest = true;
    changeToRest();
  }

  pauseButton.onclick = function() {
    clearInterval(interval);
  }

  function countdownSeconds() {
    seconds -= 1;
    secondsSpan.innerText = seconds;
    checkForStateChange();
  }

  function checkForStateChange() {
    if (seconds == 0 && rest == false) {
      seconds = breakTime + 1;
      rest = true;
      changeToRest();
    } else if (seconds == 0 && rest == true) {
      seconds = intervalTime + 1;
      rest = false;
      changeToGo();
    }
  }

  function changeToRest() {
    $("body").css("background", "cyan");
    statusHeader.innerText = "Rest";
  }

  function changeToGo() {
    $("body").css("background", "pink");
    statusHeader.innerText = "Go!";
  }

}
