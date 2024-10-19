<?php
session_start();
$servername = "localhost";
$username = "root";
$password = "xeyoss";
$dbname = "booklib";

// Veritabanı bağlantısı
$conn = new mysqli($servername, $username, $password, $dbname);

// Bağlantı kontrolü
if ($conn->connect_error) {
    die("Bağlantı hatası: " . $conn->connect_error);
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $user = $_POST['username'];
    $pass = $_POST['password'];

    // Kullanıcıyı veritabanından çekme
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->bind_param("s", $user);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        // Şifre kontrolü
        if (password_verify($pass, $row['password'])) {
            // Giriş başarılı, oturum bilgilerini ayarla
            $_SESSION['user_id'] = $row['id'];
            $_SESSION['username'] = $row['username'];
            $_SESSION['profile_image'] = $row['profile_image'];
            // Flask uygulamasına yönlendir
            header("Location: http://127.0.0.1:2000/");
            exit();
        } else {
            $error = "Geçersiz şifre";
        }
    } else {
        $error = "Kullanıcı bulunamadı";
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Giriş Yap</title>
</head>
<body>
    <form method="POST" action="">
        <input type="text" name="username" placeholder="Kullanıcı Adı" required>
        <input type="password" name="password" placeholder="Şifre" required>
        <button type="submit">Giriş Yap</button>
    </form>
    <?php if (isset($error)) echo "<p>$error</p>"; ?>
</body>
</html>
