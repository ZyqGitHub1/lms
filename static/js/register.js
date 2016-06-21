var request = window.superagent;
$('.register').click(function(){
	var regpsw = $('#regpsw').val();
	var regema = $('#regema').val();
	var conpsw = $('#conpsw').val();
	var postData = {
		'user': {
			'email': regema,
			'password': regpsw,
			'repassword': conpsw,
		}
	}
	var url = '/myapp/register';
    request.post(url)
    .send(JSON.stringify(postData))
    .set('Accept', 'application/json')
    .end(function(error,response){
        if (!error && response.body.successful) {
				alert("Register Success");
			} else {
				alert("Register FAILED");
			}
		});
})