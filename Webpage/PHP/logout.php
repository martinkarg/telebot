<!--
	Author: Martin Karg
	Date: 4/11/2016
	Function: destroys current session
-->

<?php
    session_start();
    unset($_SESSION['login']);
    unset($_SESSION['valid']);
    session_unset();
    session_destroy();
    header('Location: /index.php');
    exit;
?>