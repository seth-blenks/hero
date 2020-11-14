window.setTimeout(function(){
    var list_of_alerts = document.getElementsByClassName("alert");
    for(var i = 0; i < list_of_alerts.length;i++){
      document.removeChild(list_of_alerts[i]);
    }
  },1000);