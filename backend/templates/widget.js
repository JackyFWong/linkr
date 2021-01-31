var context = {{ context }};
var has_account = context.has_account;
var email = context.email;
var user_name = context.name;
var img_src = context.picture_src;
var other_user = Object.keys(context.connections)[0];

function connect_users(user) {
	/*$.post("https://127.0.0.1:5000/change_connection", {
		"username": user
	});*/
	$.ajax({
        type: "POST",
        url: "https://e-links.herokuapp.com/change_connection",
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

function join_email(sender_email, sender_name) {
	Email.send({
		SecureToken: "bf9d6c7f-aa99-4805-9a60-37d4648ee0f1",
		To: sender_email,
		From: "noreply@example.com",
		Subject: "Join Linkr today!",
		Body: "Hello " + sender_name + ", join Linkr today!"
	}).then(
		message => alert(message)
	);
}

function conn_email(sender_email, sender_name, reciever_email, reciever_name) {
	Email.send({
		SecureToken: "bf9d6c7f-aa99-4805-9a60-37d4648ee0f1",
		To: reciever_email,
		From: sender_email,
		Subject: "Hi " + reciever_name + ", I want to connect with you!",
		Body: "Hello " + reciever_name + ", I've used Linkr to connect with you. Here's my \
		email: " + sender_email + ". Let's link up! Thank you, " + sender_name
	}).then(
		message => alert(message)
	);
}

function email_wrapper() {
	console.log("inside the wrapper");
	console.log(has_account);
	var sender_email = $("#s_email").val();
	var sender_name = $("#s_name").val();
	var reciever_email = email;
	var reciever_name = user_name;
	// send linkr join email
	if (!has_account) {
		console.log("called join_email()")
		join_email(sender_email, sender_name);
	}
	// send connection request email
	console.log("called conn_email()")
	conn_email(sender_email, sender_name, reciever_email, reciever_name);
}

$(document).ready( () => {
	console.log(context);
	var widget_div = $("#linkr_template");
	
	var content = $("<table style=\'width:200px;\'> \
	<tr> \
		<td>" + user_name + "</td> \
		<td><div style=\'display:inline-block;background:url(\"" + img_src + "\") center center/50px auto no-repeat;width:50px;height:50px;\'></div></td> \
	</tr> \
	<tr> \
		<td colspan=\'2\'> \
			<form onsubmit=\'email_wrapper();\'> \
				<input id=\'s_name\' name=\'s_name\' type=\'text\' placeholder=\'Name\' required> \
				<input id=\'s_email\' name=\'s_email\' type=\'text\' placeholder=\'Email\' required> \
				<button type=\'submit\'>Link up!</button> \
			</form> \
		</td> \
	</tr> \
	</table>");
	widget_div.append(content);

	//var connect_button = $("<button onclick='connect_users(\""+username+"\")'>Connect</button>");
	//widget_div.append(connect_button);

});
