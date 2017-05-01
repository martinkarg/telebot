<html>
	<div id="container">
	<head>
		<title>Login</title>
		<meta charset="UTF-8">
		<!--Import Google Icon Font-->
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <!--Import materialize.css-->
        <link type="text/css" rel="stylesheet" href="materialize/css/materialize.css"  media="screen,projection"/>
   		<link rel="stylesheet" type="text/css" href="CSS/style.css">
	</head>
	<body >
		<div class="backgroundIntro" id="main">
			<br><br><br>
			<div class = "login-block">
				<center>
					<h1>Login</h1> 
					<?php include 'PHP/login.php';?>
					<form method = "post" >
						<input  type = "text" value = "" id = "username" name = "username" placeholder = "username"></br>
						<input type = "password" value = "" id = "password" name = "password" placeholder = "password" required>
						<br>
						<span class="red-text"><?php echo $msg; ?></span><br>
						<button href="#!" class= "btn waves-effect waves-green" type = "submit" name = "login">login</button>
					</form>
					
				</center>
			</div>
		</div> 
			<footer id="footer" >
		          <div class="row" id="login-footer">
		              <div class="col l3 s12">
		                <img src="tec.jpg" alt="" class="circle responsive-img" id="tec">
		                
		              </div>
		              <div class="col l2 s12">
		                <h5 class="white-text">Proyecto de Robótica</h5>
		                <p class="grey-text text-lighten-4">Para más información visite: .</p>
		              </div>
		              <div class="col l6  s12">
		                <h5 class="white-text center-align">Integrantes: </h5>
		                <div class="col l3 s6" >
		                	<p class="white-text footer-names">Roberto Ruano  </br>Martin Karg</p>	
		                </div>
		                <div class="col l3 6">
		                	<p class="white-text footer-names">Ciao Hernandez   </br>Zuriel Alcaraz</p>
		                </div>
		                <div class="col l3 s6">
		                	<p class="white-text footer-names">Luis Herrería    </br>Rafael Suarez</p>	
		                </div>
		                <div class="col l3 6">
		                	<p class="white-text footer-names">Alfonso Mucio    </br>Carlos Cabezas</p>
		                </div>
		                
		           	  </div>
		           	  
		           	  </div>
		              
		            
		          </div>
		          
        	</footer>
		
      
     
	</body>
	</div>
</html>