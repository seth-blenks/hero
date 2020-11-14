;var list_of_entries = null;

window.setTimeout(function(){
list_of_entries = document.getElementsByClassName("database_content");
list_of_entries_delete = document.getElementsByClassName("database_content_delete");



//This function updates the screen
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

function loading(){
    var obj = document.createElement("div");
    var main_obj = document.getElementById("main_obj");
    obj.innerHTML = '<img src="/static/assets/images/debian.jpg" alt="loading ...">';
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
    
    xml.open("GET","/u0123gg1/ab12345/admin/customers/delete/?id="+name)
    xml.send()
}



//This function is called when ever the preview button is clicked
// It sends a request to the server to get the objects data
// and updates the screen with the callback function
function preview(name,callback){
    
    var xml = new XMLHttpRequest();

    xml.onreadystatechange = function(){
        if(xml.readyState === 4 && xml.status === 200){
            callback(xml.responseText);
        }
        if(xml.readyState === 3){
            loading();
        }
    }
    xml.open("GET","/u0123gg1/ab12345/admin/customers/?id="+name)
    xml.send()
    
}

for(var i in list_of_entries){
    list_of_entries[i].onclick = function(){
        preview(this.getAttribute("data-val"),callback);
    }
}


for(var i in list_of_entries_delete){
    list_of_entries_delete[i].onclick = function(){
        var reply = window.confirm("Do you want to delete file: "+this.getAttribute("data-val")+"?");
        if(reply === true){
            send_delete(this.getAttribute("data-val"));};
        
    }

    
}

},700);



