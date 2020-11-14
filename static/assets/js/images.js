;window.setTimeout(function(){
    var delete_button = document.getElementsByClassName("image_delete_button");
    for(var i = 0; i < delete_button.length; i++){
        delete_button[i].onclick = function(){
            let xml = new XMLHttpRequest();
            xml.onreadystatechange = function(){
                if(xml.readyState === 4 && xml.status === 200){
                    window.location.reload();
                }
            }
            name = this.getAttribute("data-imgid");
            xml.open("GET","/u0123gg1/ab12345/admin/images/delete/?id="+name);
            xml.send();
        }
    }
},2000);