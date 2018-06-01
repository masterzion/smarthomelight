function DoSubmit(){
  document.passform.password.value = md5(document.getElementById("pwd").value+salt);
  document.getElementById("myform").submit();
}
