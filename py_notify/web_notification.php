<h4> EMAIL Notification SENT</h4>
<?php
if($_POST['emailto'] != '')
{

    $email = $_POST['emailto'];
    $locomotive = $_POST['locomotives'];
    $device = $_POST['device'];
    $status = $_POST['status'];
    $recursion = $_POST['alert'];

    echo "FROM .php: ".$email." ".$locomotive." ".$device." ".$status." ".$recursion."<hr>";
    $command = system("./phpCall.sh ".$email." ".$locomotive." ".$device." ".$status." ".$recursion);
}
?>

<script>
function goBack() {
    window.history.back();
}
</script>
<br>
<br>
<button type="submit" onclick="goBack()">[BACK]</button>
