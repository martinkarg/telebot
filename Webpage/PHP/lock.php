<!--
	Author: Martin Karg
	Date: 4/11/2016
	Function: sends unsigned session to login page
-->

<?php
	session_start();
	if (isset($_SESSION['login'])) 
	{
		header ('Location: /login.php');
		exit;
	}
?>