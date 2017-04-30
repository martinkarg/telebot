<html>
	
	<head>
		<title>Login</title>
		<meta charset="UTF-8">
   		<link rel="stylesheet" type="text/css" href="CSS/style.css">
	</head>
	
	<body>
		<div class="backgroundIntro">
			<br><br><br>
			<div class = "login-block">
				<center>
					<h1>Login</h1> 
					<?php include 'PHP/login.php';?>
					<form method = "post" >
						<input type = "text" value = "" id = "username" name = "username" placeholder = "username"></br>
						<input type = "password" value = "" id = "password" name = "password" placeholder = "password" required>
						<br>
						<span class="text-danger"><?php echo $msg; ?></span><br>
						<button type = "submit" name = "login">login</button>
					</form>
					<button name = "register" onclick="location.href = 'register.php';">register</button><br><br>				</center>
				</center>
			</div>
			<div class = "fill-page">
				<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
			</div>
		</div>
      
	</body>
</html>