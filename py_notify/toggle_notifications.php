<h4> STATUS CHANGED: </h4>
<?php
$menu = $_POST['action'];

switch ($menu) {
    case 'start':
        echo "| SCRIPT TURNED ON | ";
        system("./recursive_notification_check.py >/dev/null 2>/dev/null &");
        break;

    case 'stop':
        echo "| SCRIPT TURNED OFF | ";
        system("sudo kill $(ps aux | grep 'recursive_notification_check' | awk '{print $2}')");
        system("sudo sh logTail.sh");
        break;

    default:
        echo "| inside default | ";
        break;
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
