window.onload = function() {

  var seconds = 10;
  var rest = true;
  var interval;
  var giveup= false;
  var wait = true;
  var intervalTime = 20;
  var breakTime = 10;

  var intervalInput = document.getElementById("intervalTime");
  var breakInput = document.getElementById("breakTime");

  var startButton = document.getElementById("start");
  var resetButton = document.getElementById("reset");
  var giveupButton = document.getElementById("give_up");
  var resetTrainButton = document.getElementById("reset_train");

  var statusHeader = document.getElementById("status");
  var secondsSpan = document.getElementById("sec");
  var audio = new Audio('static/beep-09.wav');

  	// the input form value to connect to VM is populated automatically using the current URL
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

	var options = {
                onlyInteger: false
	};

	// In the global name space Chartist we call the Line function to initialize a line chart. 
	// As a first parameter we pass in a selector where we would like to get our chart created (in this case the chart div).
	// To select a div by its ID you use # + div id
	// Second parameter is the actual data object and as a third parameter we pass in our options
	var chart = new Chartist.Line('#chart', data, options);

	var initial_time = -1
  //################  START BUTTON #####################################
  //Starts workout and communication with the server
  
  startButton.onclick = function() {
    giveup= false;
    n_sets = document.getElementById("n_sets").value //reads the input 
    changeGetReady(); 
    interval = setInterval(countdownSeconds, 1000);

	// Tries to connect to the web socket end pointof our server. 	
	ws = new WebSocket('ws://' + document.getElementById("raspIP").value + ':9999/ws');
	var interval = null	
	// When the websocket opens, we will start sending messages requesting
	// data every 100 ms
	ws.onopen = function (event) {
		interval = setInterval(function(){
			n = document.getElementById("n_sets").value
			ws.send(JSON.stringify({type:'sendData', n_sets: n}))
			}, 100);
	}


	// This will handle the incoming messages. 
	//     - appendS the DATA message to the data variable until we have the last 1.5 seconds of data. 
	//       Afterwards we start to removing the first value.
	//     - plots the data into the chart 
	//     - if the class message is not '0', it displays the classification of the training segment  
	ws.onmessage = function (event) {
		msg = JSON.parse(event.data)
		// If condition to set the intial time
		if(initial_time==-1){
			initial_time = msg.timestamp
		}
		
		// The next piece of logic is to keep the size of both array
		// less or equal to 15 points, being a sliding window plot
		if(data.labels.length == 15){
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

		//Shows result of classifier, if given
		if(msg.class != 0){
			if(msg.class == 'Others'){
			    document.getElementById("exercise").innerHTML = "<h4>Others<br></h4> <img  src='static/others.png' style ='width: 7.5em'>"
			}
			if(msg.class == 'Squats'){
			    document.getElementById("exercise").innerHTML = "<h4>" + msg.n_reps + "<br>Squats</h4>" + "<img  src='static/squats.png' style ='width: 7.5em'>" 
			}
			if(msg.class == 'Lunges'){
			    document.getElementById("exercise").innerHTML = "<h4>" + msg.n_reps + "<br>Lunges</h4>" + "<img  src='static/lunges.png' style ='width: 7.5em'>"
			}
			if(msg.class == 'Push Ups'){
			    document.getElementById("exercise").innerHTML = "<h4>" + msg.n_reps + "<br>Push Ups</h4>" + "<img  src='static/pushups.png' style ='width: 7.5em'>"
						}

					}
					
				}
				// This handles any error, like connection drops.
				ws.onclose = function(evt) {
					clearInterval(interval)
					if (evt.code==1006){
						alert('Can not connect to the server.\nIs the raspberry IP correct?\nIs the server running?\nAre you connect to the "PI" network?')
					}
				}
  }
  //
  resetButton.onclick = function() {
    reset();
  }
  //################  RESET TRAIN BUTTON #####################################
  //restarts the timer and page display
  resetTrainButton.onclick = function() {
    location.reload();
  }
  //################  GIVE UP BUTTON #########################################
  //stops workout at any point and ends data acquisition
  giveupButton.onclick = function() {
	giveup= true;
	changegiveup()
        document.getElementById("reset").click();
	seconds = 1;
    	ws = new WebSocket('ws://' + document.getElementById("raspIP").value + ':9999/ws'); 
	var interval = null 
	// When the websocket opens, we will start sending messages requesting 
	//does not ask for data 
	ws.onopen = function (event) { 
	interval = setInterval(function(){ 
	ws.send(JSON.stringify({type:'end', n_sets:'3'})) }, 100); } 
	ws.onclose = function(evt) { clearInterval(interval) 
	if (evt.code==1006){
	 alert('Can not connect to the server.\nIs the raspberry IP correct?\nIs the server running?\nAre you connect to the "PI" network?') }
        }
  }
  
  //################  cOUNTDOWN FUCNTIONS #########################################
  function reset() {
    clearInterval(interval);
    seconds = 0;
    secondsSpan.innerText = seconds;
    rest = true;  
  }

  function countdownSeconds() {
    seconds -= 1;
    secondsSpan.innerText = seconds;
    checkForStateChange();
  }
  function checkForStateChange() {
      if (seconds == 0 && rest == false && wait == false && n_sets > 0  && giveup== false) {
      seconds = breakTime + 1;
      rest = true;
      changeToRest();
    } else if (seconds == 0 && rest == true && wait == false && n_sets > 0  && giveup== false) {
      seconds = intervalTime + 1;
      rest = false;
      changeToGo();
      n_sets = n_sets - 1;
    } else if (seconds == 0 && rest == true && wait == true && n_sets > 0  && giveup== false) {
      changeToGo();
      wait = false;
      seconds = intervalTime + 1;
      rest = false;
      n_sets = n_sets - 1;
    } else if (seconds <= 0 && wait == false && n_sets == 0  && giveup== false){
      seconds = 1;
      changeToDone();
    } else if (seconds <= 0 && giveup ==  true){
seconds = 1;
    }
  }
  function changeToRest() {
    audio.play();
    $("body").css("background", "#FDFD97");
    statusHeader.innerText = "Rest";
  }
  function changeToGo() {
    audio.play();
    $("body").css("background", "#B0FFAD");
    statusHeader.innerText = "Go!";
  }
  function changeGetReady(){ 
    $("body").css("background", "#FDFD97"); 
    statusHeader.innerText = "Get ready!"; 
  } 
function changegiveup(){
    audio.play(); 
    $("body").css("background", "#D3D3D3"); 
    statusHeader.innerText = "U Gave up :("; 
  }
  function changeToDone(){ 
    $("body").css("background", "#BDF2FF"); 
    statusHeader.innerText = "Workout done!";
    document.getElementById("reset").click();
  } 
}
