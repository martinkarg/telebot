<!--
	Author: Martin Karg
	Date: 4/11/2016
	Function: Provides functionality for registering users in the database
-->

<?php

	$message = "No Error";
	
	$servername = getenv('IP');
	$username = getenv('C9_USER');
	$password = "";
	$dbname = "telebot";
	$dbport = 3306;
	
	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);
	// Check connection
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
		echo "ERRORRRRRRRRRRRRRRRR";
	}
	
	
	if (isset($_POST['register'])) {   
		$username = $_POST['username'];
		$name = $_POST['name'];
		$last_name = $_POST['last_name'];
		$password = hash('sha256', $_POST['password']);
		$password_confirm = hash('sha256', $_POST['password_confirm']);
		$mail = $_POST['mail'];
		$mail_confirm = $_POST['mail_confirm'];
		
		// Cleanup inputs
	  	$name = strip_tags($name);
	  	$name = htmlspecialchars($name);
	  	
	  	$name = strip_tags($name);
	  	$name = htmlspecialchars($name);
	
	  	$last_name = strip_tags($last_name);
	  	$last_name = htmlspecialchars($last_name);
	
		$password = strip_tags($password);
		$password = htmlspecialchars($password);
		
		$password_confirm = strip_tags($password_confirm);
		$password_confirm = htmlspecialchars($password_comfirm);
		
		$mail = strip_tags($mail);
	  	$mail = htmlspecialchars($mail);
	  	
	  	$mail_confirm = strip_tags($mail_confirm);
	  	$mail_confirm = htmlspecialchars($mail_confirm);
		
		// Validate that password matches the confirmed password
		if(strcmp($password,$password_confirm) != 0){
		    $message = "Las contraseñas deben ser iguales";
		}
		
		// Validate that email matches the confirmed email
		if(strcmp($mail,$mail_confirm) != 0){
		    $message = "Los correos electronicos deben ser iguales";
		}
		
		// Validate size and content of name
		if (strlen($name) < 2) {
			$message = "Tu nombre tiene que tener al menos 2 caracteres";
		} else if (!preg_match("/^[a-zA-Z ]+$/",$name)) {
			$message = "Tu nombre tiene que contener sólo letras";
		}
		
		// Validate size and content of last name
		if (strlen($last_name) < 2) {
			$message = "Tu apellido debe tener al menos 2 caracteres";
		} else if (!preg_match("/^[a-zA-Z ]+$/",$last_name)) {
			$message = "Tu apellido tiene que contener sólo letras";
		}
		
		echo $message;
		
		if($message = "No Error"){
			// Prepare SQL statement
			$sql = "INSERT INTO `usuarios`(`id_tipos`, `username`, `password`, `puntos`, `nombre`, `apellidos`,`email`) 
					VALUES (2,'".$username."','".$password."',0,'".$name."','".$last_name."','".$mail."');";
			echo $sql;
			$conn->query($sql);
			
			// Initialize session
			session_start();
			$_SESSION['valid'] = true;
			$_SESSION['login'] = $username;
			$_SESSION['time'] = time();
			$_SESSION['user_type'] = 2;
			header( 'Location: index.php' );
		}
	}
?>