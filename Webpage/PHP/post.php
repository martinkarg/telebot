<?php
    session_start();
    $text = $_POST['text'];
    echo($text);
    $fp = fopen("log.html", 'a');
    fwrite($fp, $text);
    echo($x);
    fclose($fp);
?>