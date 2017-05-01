<?php
session_start();
?>
<!DOCTYPE html>
<html>
    <head>
      <!--Import Google Icon Font-->
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <!--Import materialize.css-->
      <link type="text/css" rel="stylesheet" href="materialize/css/materialize.min.css"  media="screen,projection"/>

      <!--Let browser know website is optimized for mobile-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <title>PRUEBAAAAA</title>
    
    <body background="bck.jpg" class="responsive-image" id="body" >
        <h4 class="white-text" id="welcome"></h4>
        <div>
            <button class="waves-effect waves-light btn" id="btn-open-room" >START CLASS</button>
            <button class="waves-effect waves-light btn" id="help" onmouseover="showDiscovery();" onmouseout="hideDiscovery();">Help</button>
        </div>
    <div class=container id="video-container">
        <video id="professor" ></video>
        <video id="room" ></video>
        <video id="robot" ></video>
        
    </div>
    
    <!-- Tap Target Structure -->
            <div id="discovery-wrapper" class="tap-target-wrapper " style="right: -348px; bottom: -327px; position: fixed;">
                <div class="tap-target" style="background-color:rgba(0, 93, 255, 0.6);" data-activates="menu">
                    <div class="tap-target-content white-text" style="width: 456px; height: 400px; top: 0px; right: 0px; bottom: 0px; left: 0px; padding: 130px; vertical-align: bottom;">
                        <h5>Commands:</h5>
                        <p class="white-text"> 'Q' --> turn counter clock-wise</p>
                        <p class="white-text"> 'W' --> move forwards</p>
                        <p class="white-text"> 'E' --> turn  clock-wise</p>
                        <p class="white-text"> 'A' --> turn left</p>
                        <p class="white-text"> 'S' --> stop</p>
                        <p class="white-text"> 'D' --> turn right</p>
                        <p class="white-text"> 'X' --> move backwards</p>
                    </div>
                </div>
                <div class="tap-target-wave" style="top: 344px; left: 344px; width: 112px; height: 112px;">
                    <a class="btn btn-floating btn-large tap-target-origin" style="background-color:rgba(0, 93, 255, 0.6);">
                        <i class="material-icons">menu</i>
                    </a>
                </div>
            </div>
    
    <h1 id="user"></h1>
    
        
      </body>  
    
    
    <script src="https://rtcmulticonnection.herokuapp.com/dist/RTCMultiConnection.min.js"></script>
    <script src="https://rtcmulticonnection.herokuapp.com/socket.io/socket.io.js"></script>
    <script src="https://code.jquery.com/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
    <script type="text/javascript" src="materialize/js/materialize.min.js"></script>
    <script src="DetectRTC.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            document.getElementById("user").style.visibility="hidden";
            document.getElementById("user").innerHTML= "<?php  echo $_SESSION['professor']; ?>";
            var user = document.getElementById("user").innerHTML;
            console.log(user);
            if (user==="profe"){
                var msg= "calling";
                $.post("/PHP/init_call.php", {text: msg});
                preformat_professor();
            }
            else if(user==="robot"){
                preformat_robot();
            }
            
        });
       
        var connection = new RTCMultiConnection();
        var opened = false;
        var joined = false;
        var counter= 0;
        var remote_counter=0;
        // this line is VERY_important
        connection.socketURL = 'https://rtcmulticonnection.herokuapp.com:443/';
        
        // all below lines are optional; however recommended.
        
        connection.session = {
            audio: true,
            
            video: true
        };
        
        connection.sdpConstraints.mandatory = {
            OfferToReceiveAudio: true,
            OfferToReceiveVideo: true
        };
        
        connection.mediaConstraints = {
        audio: {
            mandatory: {
                echoCancellation: true, // enabl audio processing
                googAutoGainControl: true,
                googNoiseSuppression: true,
                googHighpassFilter: true,
                googTypingNoiseDetection: true,
                //googAudioMirroring: true
            }
        },
        video: {
            mandatory: {
                minWidth: 400,
                maxWidth: 400,
                minHeight: 400,
                maxHeight: 400
            },
            optional: []
            }
        }
        
        connection.setDefaultEventsForMediaElement = null;
        

       
        
       
        var predefinedRoomId = 'Qro6301';
        
        document.getElementById('btn-open-room').onclick = function() {
            document.getElementById("welcome").innerHTML=predefinedRoomId;
            opened=true;
            console.log(joined + "   " + opened)
            var counter = 0;
            this.disabled = true;
            connection.openOrJoin( predefinedRoomId );
          
        };
        
        
        
        
        
        
        connection.onstream = function(event){
            
            var videos = document.getElementById("video-container");
            var robot = document.getElementById("robot");
            var prof = document.getElementById("professor");
            var room = document.getElementById("room");
            var type = document.getElementById("user").innerHTML;
            console.log("user type: " + type);
            if (type === "profe"){
                
                if(event.type=== "local"){
                    console.log("STREAM ID: "  + "TYPE: " + event.type);
                    if(counter==0){
                        console.log(event.blobURL);
                        counter++;
                        prof.setAttribute("src", event.blobURL);
                    }
            
                    
                }//end if type local
                else if(event.type==='remote'){
                    console.log("THERE´S REMOTE CONNECTION!!!!!!!!");
                    if(remote_counter===0){
                        robot.setAttribute("src", event.blobURL);
                        remote_counter++;
                    }else if(remote_counter===1){
                        room.setAttribute("src", event.blobURL)
                        remote_counter++;
                    }
                }
                
        }
        else if (type === "robot"){
            console.log("entered as robot");
                if(event.type=== "local"){
                    console.log("STREAM ID: " + event.streamid + "TYPE: " + event.type);
                    if(counter==0){
                        console.log(event.blobURL);
                        counter++;
                        room.setAttribute("src", event.blobURL);
                    }
                    else if (counter==1){
                        console.log(event.blobURL);
                        counter++;
                        robot.setAttribute("src", event.blobURL);
                    }
                    //videos.appendChild(event.mediaElement);
                    //prof.setAttribute("src", event.blobURL)
                    DetectRTC.load(function() {
                    var secondaryCamera = DetectRTC.videoInputDevices[1];
                    if (!secondaryCamera) {
                        alert('Please attach another camera device.');
                        return;
                    }
                
                    connection.mediaConstraints = {
                        audio: true,
                        video: {
                            mandatory: {
                                minWidth: 150,
                                maxWidth: 150,
                                minHeight: 150,
                                maxHeight: 150
                            },
                            optional: [{
                                sourceId: secondaryCamera.id
                            }]
                        }
                    };
                    
                    connection.addStream({ video: true, audio:true });
                    //videos.appendChild(event.mediaElement);
                    }); //end Detect rtc function
                }//end if type local
                else if(event.type==='remote'){
                    
                    console.log("THERE´S REMOTE CONNECTION!!!!!!!!")
                    //videos.appendChild(event.mediaElement);
                    prof.setAttribute("src", event.blobURL)
                }
            } //end if robot
        } // end onstream function
        
        $('#body').keyup(function(event) {
            var x = event.key;               
            if(x==='a' || x==='w' || x==='s' || x==='d'
                || x==='q' || x === 'e' || x === 'x'){
                var msg = x;
                console.log("event called" + x);
		        $.post("/PHP/post.php", {text: msg});				
	        	
		        return false;
            }
        });
        
        
        function preformat_professor (){
            var robot = document.getElementById("robot");
            var prof = document.getElementById("professor");
            var room = document.getElementById("room");
            $('#professor').css({'background': 'url(/professor.png)', position : 'absolute', height : 150, width:150, left:850, top:200, 'background-size': 'contain', 'z-index':1000});
            $('#room').css({'background':'url(/room.png)', position : 'absolute', height : 500, width:650, left:350, top:200, 'background-size': 'contain', 'background-repeat':'no-repeat'});
            $('#robot').css({'background': 'url(/robot.png)',  position : 'absolute', height : 200, width:200, left:800, top:500, 'background-size': 'contain'});
            
        }
        
        function preformat_robot (){
            var robot = document.getElementById("robot");
            var prof = document.getElementById("professor");
            var room = document.getElementById("room");
            $('#professor').css({'background': 'url(/professor.png)', position : 'absolute', height : 700, width:800, left:50, top:100, 'background-size': 'contain', 'background-size': 'cover'});
            $('#room').css({'background':'url(/room.png)', position : 'absolute', height : 0, width:0, left:50, top:200, 'background-size': 'contain', });
            
            $('#robot').css({'background': 'url(/robot.png)',  position : 'absolute', height : 0, width:0, left:800, top:200, 'background-size': 'contain'});
        }
        
        function showDiscovery() {
            var discovery = document.getElementById("discovery-wrapper");
            discovery.classList = "tap-target-wrapper open";
        }

        function hideDiscovery() {
            var discovery = document.getElementById("discovery-wrapper");
            discovery.classList = "tap-target-wrapper";
        }

        
    </script>
</html>