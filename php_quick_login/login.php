<?php

// phpinfo(); //quick version checK:
// Apache/2.2.15 (Red Hat)
// PHP Version 5.3.3l

// hashes for comparisson
// 63a9f0ea7bb98050796b649e85481845 root
// a0b5c2f98cd558e8ee2c5dd3ab22501d pw1
// 0baea2f0ae20150db78f58cddac442a9 superuser
// 0affad4f1d0fe97e0092ceded0e6113a pw2

// starting no null
if ($_POST['username'] == "" or $_POST['password'] =="")
{
    echo "invalid empty input";
    //reload
}

//sanitize & hash PHP input
$_POST['username'] = filter_var($_POST['username'], FILTER_SANITIZE_STRING);
$user = $_POST['username'];
$user = trim($user);
$user = md5($user);

//clean password input
$_POST['password'] = filter_var($_POST['password'], FILTER_SANITIZE_STRING);
$pass = $_POST['password'];
$pass = trim($pass);
$pass = md5($pass);     //$pass = crypt($pass);

//database
$db = new SQLite3('accounts.db') or die('Unable to open database');

//simple request
$sql =<<<EOF
      SELECT * from accounts;
EOF;

$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC))
{
  $dbuser = $row['username'];
  $dbpass = $row['password'];

    if ($dbuser == $user and $dbpass == $pass)
    {
        echo " THIS FINNALY WORKS \n";                 //} elseif ($dbuser != $user or $dbpass != $pass){
        echo "HERE is where SAM's event is called!";
    }
}

?>
