function DoSubmit(){
  document.passform.password.value = md5(document.getElementById("pwd").value+salt);
  document.getElementById("myform").submit();
}

var input = document.getElementById("pwd");

function checkSubmit(e) {
   if(e && e.keyCode == 13) {
      document.getElementById("submit").click();
   }
}
