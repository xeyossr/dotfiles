<?php
session_start();
session_destroy();
header("Location: http://127.0.0.1:2000/");  // Flask uygulamasına yönlendir
exit();
