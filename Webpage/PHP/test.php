<?php
$myfile = fopen("t.txt", "w");
$txt = "John Doe\n";
echo "hola";
fwrite($myfile, $txt);
$txt = "Jane Doe\n";
fwrite($myfile, $txt);
fclose($myfile);
?>