#!/bin/bash 
source ~/.bashrc

MODULE_NAME="$1"
ACTION="$2"



if [ "$2" == "" ] ; then
    echo "$0 module_name {start|stop|restart|status}"
    exit 2
fi


module_status () {
    PID=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G PIDS $MODULE_NAME 2> /dev/null )
    if [ "$PID" == "" ] ; then 
       PID="0"
    fi
    echo $PID
}

module_start () {
    if [ ! -d "$SMARTHOME_DIR/modules/$MODULE_NAME" ]; then
      echo "Module dir not found: $SMARTHOME_DIR/modules/$MODULE_NAME"
      exit 2
    fi

    echo "Starting $MODULE_NAME... "    
    cd "$SMARTHOME_DIR/modules/$MODULE_NAME"
    ./start.sh  &
    PID=$!
    sleep 2
    echo "PID: $PID"
    $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $PID
}

module_stop () {
    if [ ! -d "$SMARTHOME_DIR/modules/$MODULE_NAME" ]; then
      echo "Module dir not found: $SMARTHOME_DIR/modules/$MODULE_NAME"
      exit 2
    fi

    echo "Stopping $MODULE_NAME... "
    PID=$(module_status)
    if [ "$PID" == "0" ] ; then
      echo "Module is not running"
    else
      $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME 0 &> /dev/null
      pkill -P $PID &> /dev/null
    fi
}


case "$ACTION" in
    start)
        PID=$(module_status)
        if [ "$PID" == "0" ] ; then
          module_start
        else
          echo "ERROR: Module is running"
          exit 2
        fi
        ;;
    stop)
        module_stop
        ;;
    restart|force-reload)
        module_stop
        sleep 2
        module_start
        ;;
    status)
        PID=$(module_status)
        if [ "$PID" == "0" ] ; then
          echo "Not running"
        else
          echo "Running: " $(module_status)
        fi
        ;;
esac
