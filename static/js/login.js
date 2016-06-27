var request = window.superagent;
var resigerVue = new Vue({
    el:"#lognvue",
    data:{
        post_data:{
            user:{
                email:'',
                password:'',
            }
        },
        emailgood:false,
        passwordgood:false
    },
    computed:{
        emailgood:function () {
            var reg =/^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
            return reg.test(this.post_data.user.email);
        },
        passwordgood:function () {
            return this.post_data.user.password != '';
        }
    },
    methods: {
    dologin: function (event) {
        if(!this.emailgood){
            alert("邮箱格式不正确");
        }
        else if(!this.passwordgood){
            alert("请输入密码");
        }
        else{
            var url = '/myapp/login';
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
                        console.log(response.body);
                        if (response.body.confirmed == false) {
                        	alert("邮箱未验证");
                        	sessionStorage.setItem('login',toJSON(response.body));
                        	window.location.href = "/static/html/unconfirmed.html";
                        } else {
                        	if (response.body.role_name == "管理员") {
                        		alert('登陆成功');
		                        sessionStorage.setItem('login',toJSON(response.body));
		                        window.location.href = "/static/html/system.html";
                        	} else{
                        		alert('登陆成功');
		                        sessionStorage.setItem('login',toJSON(response.body));
		                        window.location.href = "/static/html/system_for_user.html";
                        	}
                        }
                        
                    }
                });
        }
    }
  }
})