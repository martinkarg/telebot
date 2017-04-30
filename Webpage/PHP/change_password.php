<!--
	Author: Martin Karg
	Date: 4/11/2016
	Function: Provides functionality for changing passwords in the database
-->

<?php

	$message = "No Error";
	
	$servername = getenv('IP');
	$username = getenv('C9_USER');
	$password = "";
	$dbname = "queretarocks";
	$dbport = 3306;
	
	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);
	// Check connection
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
		echo "ERRORRRRRRRRRRRRRRRR";
	}
	
	
	if (isset($_POST['change_password'])) {   
		$username = $_POST['username'];
		$current_password = hash('sha256', $_POST['actual_password']);
		$password = hash('sha256', $_POST['password']);
		$password_confirm = hash('sha256', $_POST['password_confirm']);
		
		// Cleanup inputs
	  	
		$current_password = strip_tags($current_password);
		$current_password = htmlspecialchars($current_password);
		
		$password = strip_tags($password);
		$password = htmlspecialchars($password);
		
		$password_confirm = strip_tags($password_confirm);
		$password_confirm = htmlspecialchars($password_comfirm);
		
		// Validate that password matches the confirmed password
		if(strcmp($password,$password_confirm) != 0){
		    $message = "Las contraseñas deben ser iguales";
		}
		
		if($message = "No Error"){
			// Prepare SQL statement
			$sql = "SELECT password FROM users WHERE username = '".$_SESSION['login']."';";
			$result = $conn->query($sql);
			
			$message = "";
			
			// output data of each row
			while($row = $result->fetch_assoc()) 
			{
				$password_db = $row["password"];
			}
			
			// Check if password in form matches password in database
			if (hash('sha256',$_POST['actual_password']) == $password_db) 
			{
				// Prepare SQL statement
				$sql = "UPDATE users SET  password = '".$password."' WHERE username = '".$_SESSION['login']."';";
				$conn->query($sql);
			}
			else 
			{
				$message = 'Contraseaña incorrecta';
			}
		}
	}
?>