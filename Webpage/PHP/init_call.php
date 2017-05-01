<?php
    session_start();
    $text = $_POST['text'];
    $fp = fopen("call.html", 'a');
    fwrite($fp, $text);
    fclose($fp);
?>