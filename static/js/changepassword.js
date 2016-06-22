var changepasswordVue = new Vue({
    el:"#changepassword",
    data:{
        oldpassword:'',
        newpassword:'',
        confnewpasssword:'',
        passworldlength:false,
        passwordgood:false,
    },
    computed:{
        passworldlength:function () {
            return this.newpassword.length >= 8;
        },
        passwordgood:function () {
            return this.newpassword == this.confnewpasssword;
        },
    },
    methods: {
        dochangepassword: function (event) {
            if(!this.passworldlength){
                alert("密码长度不足8位");
            }
            else if(!this.passwordgood){
                alert("两次密码不同");
            }
            else{
                var request = window.superagent;
                var storlogin = sessionStorage.getItem("login");
                loginobj = fromJSON(storlogin);
                var url = '/myapp/user/change_password';
                var post_data={
                    token:loginobj.data.token,
                    user:{
                        old_password:this.oldpassword,
                        new_password:this.newpassword,
                    }
                };
                request.post(url)
                .send(post_data)
                .set('Accept', 'application/json')
                .end(function(error,response){
                    if (error) {
                            alert("网络异常");
                        }
                        else if(!response.body.successful) {
                            alert(response.body.error.msg);
                        }
                        else{
                            alert('修改成功');
                        }
                    });
            }
        }
    },
})