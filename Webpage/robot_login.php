<?php
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
	
	// Get username from url
	$login = htmlspecialchars($_GET["username"]);
	
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
		if (htmlspecialchars($_GET["pswrd"]) == $password) 
		{
			session_start();
			$_SESSION['valid'] = true;
			$_SESSION['login']=$login;
			$_SESSION['local'] = 167;
			$_SESSION['time']=time();
			$_SESSION['professor']=$professor;
			echo '¡Bienvenido!';
			header( 'Location: /working.php' );
		}
		else 
		{
			echo 'Contraseña incorrecta';
			session_start();
			$_SESSION['login'] = '';
			$_SESSION['valid'] = false;
			$_SESSION['login']= '';
		}
	}
	else 
	{
		echo "Ese usuario no existe";
		//header( 'Location: login.php' );
	}

?>