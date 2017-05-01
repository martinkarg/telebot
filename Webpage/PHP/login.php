<!--
	Author: Martin Karg
	Date: 4/11/2016
	Function: Provides functionality for login-related queries in the database
-->

<?php

	/*
		Author: Martin Karg
		Date: 4/11/2016
	*/

	$msg = '';
	
	$servername = getenv('IP');
	$username = getenv('C9_USER');
	$password = "";
	$dbname = "telebot";
	$dbport = 3306;
	
	$table = "users";
	
	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);
	// Check connection
	if ($conn->connect_error) 
	{
		die("Connection failed: " . $conn->connect_error);
	}
	
	if (isset($_POST['login']) && !empty($_POST['username']) && !empty($_POST['password']))
	{
	   
		// Get username from form
		$login = $_POST['username'];
		
		$sql = "SELECT * FROM $table WHERE username = '".$login."'";
		
		$result = $conn->query($sql);
		
		if ($result->num_rows > 0) 
		{
			// output data of each row
			while($row = $result->fetch_assoc()) 
			{
				$password = $row["password"];
				$professor = $row["professor"];
			}
			
			// Check if password in form matches password in database
			if ($_POST['password'] == $password) 
			{
				session_start();
				$_SESSION['valid'] = true;
				$_SESSION['login']=$login;
				$_SESSION['local'] = 167;
				$_SESSION['time']=time();
				$_SESSION['professor']=$professor;
				$msg = '¡Bienvenido!';
				header( 'Location: /working.php' );
			}
			else 
			{
				$msg = 'Contraseña incorrecta';
				session_start();
				$_SESSION['login'] = '';
				$_SESSION['valid'] = false;
				$_SESSION['login']= '';
			}
		}
		else 
		{
			$msg = "Ese usuario no existe";
			header( 'Location: login.php' );
		}
		
	}
?>