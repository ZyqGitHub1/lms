$('#logout').click(function(){
	var request = window.superagent;
	var storlogin = sessionStorage.getItem('login');
	loginobj = fromJSON(storlogin);
	var url = '/myapp/user/get_info';
	var tokendata = {
		token: loginobj.data.token
	};
	request.post(url)
	.send(tokendata)
	.set('Accept','application/json')
	.end(function(error,response){
		if (error) {
			alert("网络异常");
		} else if(!response.body.successful) {
			alert(response.body.error.msg);
		} else {
			window.location.href = "../index.html";
		}
	});
})