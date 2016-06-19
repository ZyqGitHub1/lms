$('.login').click(function(){
	var logname = $('#logname').val();
	var logpsw = $('#logpsw').val();
	var rememberMe = $('#rememberMe').is(':checked');
	
	var postData = {
		'username': logname,
		'password': logpsw,
		'rememberme': rememberMe
	}
	
	$.ajax({
		type: 'POST',
		url: '/home/login',
		data: String.toJSON(postData),
		dataType: 'JSON',
		success: function(result){
			if (result[isSuccessful]) {
				alert("Login Success");
			} else {
				alert("Login FAILED");
			}
		}
	})
})