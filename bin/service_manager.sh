#!/bin/bash 
source ~/.smarthomelight

ACTION="$1"
MODULE_NAME="$2"
MODULE_ITEM="$3"


if [ "$2" == "" ] ; then
    echo "$0 {start|stop|restart|status} module_name item"
    exit 2
fi


module_status () {
    PID=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G PIDS $MODULE_NAME $MODULE_ITEM 2> /dev/null )
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

    echo "Starting $MODULE_NAME $MODULE_ITEM ... "
    cd "$SMARTHOME_DIR/modules/$MODULE_NAME"
    ./$MODULE_ITEM.sh  &
    PID=$!


    if [[ "$MODULE_ITEM" =~ ^(start_modules|memorydb_server)$ ]]; then
       echo "item ignored in db"
    else
       echo "PID: $PID"
       $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM $PID
    fi
}

module_stop () {
    if [ ! -d "$SMARTHOME_DIR/modules/$MODULE_NAME" ]; then
      echo "Module dir not found: $SMARTHOME_DIR/modules/$MODULE_NAME"
      exit 2
    fi

    echo "Stopping $MODULE_NAME $MODULE_ITEM... "
    PID=$(module_status)
    if [ "$PID" == "0" ] ; then
      echo "Module is not running"
    else
      $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM 0 &> /dev/null
      if [ "$PID" -ne "-1" ] ; then
         pkill -P $PID &> /dev/null
         kill $PID &> /dev/null
      fi
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
