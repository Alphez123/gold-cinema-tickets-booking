<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "moviehub";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $firstName = $_POST['firstName'];
  $lastName = $_POST['lastName'];
  $city = $_POST['city'];
  $address = $_POST['address'];
  $zipCode = $_POST['zipCode'];
  $email = $_POST['email'];
  $phone = $_POST['phone'];
  $password = password_hash($_POST['password'], PASSWORD_DEFAULT);

  $sql = "INSERT INTO users (firstname, lastname, city, address, zipcode, email, phone, password)
          VALUES ('$firstName', '$lastName', '$city', '$address', '$zipCode', '$email', '$phone', '$password')";

  if ($conn->query($sql) === TRUE) {
    echo "<script>alert('Registration successful! You can now log in.'); window.location.href='login.html';</script>";
  } else {
    echo "Error: " . $sql . "<br>" . $conn->error;
  }
}

$conn->close();
?>
