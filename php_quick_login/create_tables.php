<!-- creates db -->
<?php
$dbhandle = sqlite_open('accounts.db', 0666, $error);
if (!$dbhandle) die ($error);

$stm = "CREATE TABLE IF NOT EXISTS accounts(username TEXT UNIQUE NOT NULL," .
       "password text NOT NULL,)";
$ok = sqlite_exec($dbhandle, $stm, $error);

if (!$ok)
   die("table creation error. $error");

sqlite_close($dbhandle);
?>
