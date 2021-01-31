var context = {{ context }};
var username = context.full_name;
var other_user = Object.keys(context.connections)[0];

function connect_users(user) {
	/*$.post("https://127.0.0.1:5000/change_connection", {
		"username": user
	});*/
	$.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/change_connection",
		data: JSON.stringify({"username": user, "other_user": other_user}),
		contentType: "application/json",
        //async:true,
        //dataType : 'jsonp',   //you may use jsonp for cross origin request
        crossDomain:true,
        success: function(data, status, xhr) {
            alert(xhr.getResponseHeader('Location'));
        }
		});
}

function join_email()

function email_wrapper(sender, reciever) {
	// send linkr join email

	// send connection request email

}

$(document).ready( () => {
	console.log(context);
	var widget_div = $("#linkr_template");
	
	var header = $("<h3>"+context.full_name+"</h3>");
	var connect_button = $("<button onclick='connect_users(\""+username+"\")'>Connect</button>");
	
	widget_div.append(header);
	widget_div.append(connect_button);
});
