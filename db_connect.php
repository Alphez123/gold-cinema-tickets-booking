<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "goldcinema_db"; // name of your database

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
