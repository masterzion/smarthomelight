export MIN_HOUR=11
export MAX_HOUR=22

function get_houseisempt() {
  if [ -f $FILE_HOUSEISEMPTY ]; then
     echo 1
   else
     echo 0
   fi

}


function get_cinemamode() {
  if [ -f $FILE_CINEMAMODE ]; then
     echo 1
   else
     echo 0
   fi

}