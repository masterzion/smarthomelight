function DoSubmit(){
  document.passform.myinput.value = md5(document.getElementById("pwd").value+salt);
  document.getElementById("myform").submit();
}
