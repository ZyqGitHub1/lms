var request = window.superagent;
var resigerVue = new Vue({
	el:"#regvue",
	data:{
		post_data:{
			user:{
				email:'',
				password:'',
				repassword:''
			}
		},
		emailgood:false,
		passwordgood:false,
		repasswordgood:false
	},
	computed:{
    	emailgood:function () {
    		var reg =/^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
			return reg.test(this.post_data.user.email);
    	},
    	passwordgood:function () {
			return this.post_data.user.password.length >= 8;
    	},
    	repasswordgood:function () {
			return (this.post_data.user.password == this.post_data.user.repassword && this.post_data.user.repassword);
    	}
    },
    methods: {
    doregister: function (event) {
    	if(!this.emailgood){
    		alert("邮箱格式不正确");
    	}
    	else if(!this.passwordgood){
    		alert("密码小于8位");
    	}
    	else if(!this.repasswordgood){
    		alert("两次输入的密码不同");
    	}
    	else{
      		var url = '/myapp/register';
    		request.post(url)
    		.send(this.post_data)
    		.set('Accept', 'application/json')
    		.end(function(error,response){
    		    if (error) {
						alert("网络异常");
					}
					else if(!response.body.successful) {
						alert(response.body.error.msg);
					}
					else{
						alert('注册成功');
					}
				});
    	}
    }
  }
})