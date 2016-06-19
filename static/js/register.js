$('.register').click(function(){
	var regname = $('#regname').val();
	var regpsw = $('#regpsw').val();
	var regema = $('#regema').val();
	var conpsw = $('#conpsw').val();
	
	var postData = {
		'user': {
			'name': regname,
			'password': regpsw,
			'email': regema,
			'repassword': conpsw,
		}
	}
	
	$.ajax({
		type: 'POST',
		url: '/myapp/register',
		data: JSON.stringify(postData),
		contentType: "application/json",
		dataType: 'json',
		success: function(result){
			if (result.successful) {
				alert("Register Success");
			} else {
				alert("Register FAILED");
			}
		}
	})
})