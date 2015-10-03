<?php
    $pids = null;
    exec("pgrep -f recursive_notification_check", $pids);
    if( empty( $pids ) ) {
        echo "0";
    }
    else {
        echo "1";
    }
?>
