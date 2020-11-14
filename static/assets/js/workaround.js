;

feather.replace()

var Files_button = document.getElementById("Files");
var statistics_button = document.getElementById("statistics");
var Upload_Files = document.getElementById("Upload_Files");
var images = document.getElementById("images");
var subscribers = document.getElementById("Subscribers");
var comment_button = document.getElementById("comments");
var customers = document.getElementById("customers");
var document_search_input = null;

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

function make_request_for_files(method,url,callback){
    var requester = new XMLHttpRequest();

    requester.onreadystatechange = function(){
        if(requester.readyState === 4 && requester.status === 200){
            callback(requester.responseText)
        }

        if(requester.readyState === 3){
            loading();
        }


    }

    requester.open(method,url);
    requester.send()
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
Files_button.onclick = function(){
    make_request_for_files("GET","/u0123gg1/ab12345/admin/posts",callback);
    request_js("/static/assets/js/document_script.js");
}

Upload_Files.onclick = function(){
    make_request_for_files("GET","/u0123gg1/ab12345/admin/upload/",callback);
}

images.onclick = function(){
    make_request_for_files("GET","/u0123gg1/ab12345/admin/upload/images/",callback);
    request_js("/static/assets/js/images.js")
}


statistics_button.onclick = function(){
    make_request_for_files("GET","/u0123gg1/ab12345/admin/statistics/",callback);
}

subscribers.onclick = function(){
    make_request_for_files("GET","/u0123gg1/ab12345/admin/subscribers/",callback);
}

comment_button.onclick = function(){
    make_request_for_files("GET","/u0123gg1/ab12345/admin/comments/",callback);
    request_js("/static/assets/js/comments.js");
}   

customers.onclick = function(){
    make_request_for_files("GET","/u0123gg1/ab12345/admin/customers/",callback);
    request_js("/static/assets/js/customers.js");
}