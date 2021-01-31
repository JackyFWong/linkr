var context = {{context}};
var username = context.username;

function connect_users(user) {
	$.post("https://127.0.0.1:5000/change_connection", {
		"username": user
	});
	/*
	$.ajax({
        type: "POST",
        url: "https://127.0.0.1:5000/change_connection",
        data:{"username": user},
        //async:true,
        //dataType : 'jsonp',   //you may use jsonp for cross origin request
        crossDomain:true,
		/*
        success: function(data, status, xhr) {
            alert(xhr.getResponseHeader('Location'));
        }
		});*/
}

$(document).ready( () => {
	console.log(context);
	var widget_div = $("#elink_template");
	
	var header = $("<h3>"+context.full_name+"</h3>");
	var connect_button = $("<button onclick='connect_users(username)'>Connect</button>");
	
	widget_div.append(header);
	widget_div.append(connect_button);
});
