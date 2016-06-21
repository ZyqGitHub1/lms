$('.login').click(function(){
	var logemail = $('#lognemail').val();
	var logpsw = $('#logpsw').val();

	var postData = {
		'user':{
			'email': logemail,
			'password': logpsw,
		}
	}

	var url = '/myapp/login';
    request.post(url)
    .send(postData)
    .set('Accept', 'application/json')
    .end(function(error,response){
        if (!error && response.body.successful) {
				alert("login Success");
			} else {
				alert("login FAILED");
			}
		});
})