;var list_of_entries = null;

window.setTimeout(function(){
list_of_entries = document.getElementsByClassName("database_content");
list_of_entries_delete = document.getElementsByClassName("database_content_delete");
var search = document.getElementById("document_search_input");



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
    
    xml.open("GET","/u0123gg1/ab12345/admin/comments/delete/?id="+name)
    xml.send()
}

function request_js(filename){
    var request = new XMLHttpRequest();

    request.onreadystatechange = function(){
        if(request.readyState === 4 && request.status === 200){
            eval(request.responseText);
        }
    }

    request.open("GET",filename);
    request.send();
}

search.onclick = function(){
    
    name = encodeURIComponent(document.getElementById("search_input").value);
    if(name){
    let xml = new XMLHttpRequest();
    
    
    xml.onreadystatechange = function(){
        if(xml.readyState === 4 && xml.status === 200){
            callback(xml.responseText);
            request_js("/static/assets/js/comments.js");
        }
    }
    
    xml.open("GET","/u0123gg1/ab12345/admin/comments/?title="+name)
    xml.send()
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



