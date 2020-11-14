;var list_of_entries = null;

window.setTimeout(function(){
list_of_entries = document.getElementsByClassName("database_content");
list_of_entries_delete = document.getElementsByClassName("database_content_delete");


function callback(responseText){
    var obj = document.createElement("div");
    var main_obj = document.getElementById("main_obj");
    obj.innerHTML = responseText;
    obj.id = "new_obj";
    
    //removing old element
    if(document.getElementById("new_obj")) main_obj.removeChild(document.getElementById("new_obj"));

    //adding new element
    main_obj.appendChild(obj);

}



function send_delete(name){
    let xml = new XMLHttpRequest();
    xml.onreadystatechange = function(){
        if(xml.readyState === 4 && xml.status === 200){
            window.location.reload();
        }
    }
    
    xml.open("GET","/u0123gg1/ab12345/admin/upload/delete/?id="+name)
    xml.send()
}


function send_update(name,callback){
    let xml = new XMLHttpRequest();
    xml.onreadystatechange = function(){
        if(xml.readyState === 4 && xml.status === 200){
            callback(xml.responseText);
        }
    }
    
    xml.open("GET","/u0123gg1/ab12345/admin/upload/edit/?id="+name)
    xml.send()
}

for(var i in list_of_entries){
    list_of_entries[i].onclick = function(){
        send_update(this.getAttribute("data-val"),callback);
    }
}

for(var i in list_of_entries){
    list_of_entries_delete[i].onclick = function(){
        var reply = window.confirm("Do you want to delete file: "+this.getAttribute("data-val")+"?");
        if(reply === true){
            send_delete(this.getAttribute("data-val"));};
        
    }

    
}

},700);



