<?php

$conexion = mysqli_connect("localhost", "root1" , "" , "login_register_db");

if ($conexion) {
    echo 'conectado exitosamente ala base de datos';
}else{

echo 'no se a podido conectar a la base de datos';
}

?>