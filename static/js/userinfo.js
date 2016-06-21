viewinfo = function(user){
// var storuser = sessionStorage.getItem("user");
// userobj = fromJSON(storuser);
// console.log(userobj);
var changeVue = new Vue({
    el:"#infovue",
    data:{
        username:user.user_name,
        sex:user.sex,
        maxbook:10,
        role:user.role_name,
        email:user.email,
        tel:user.phone,
        addr:user.addr,
        register_time:user.register_time,
        fine:user.fine,
        emailgood:false,
        namegood:false,
        telgood:false,
    },
    computed:{
        emailgood:function () {
            var reg =/^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
            return reg.test(this.email);
        },
        namegood:function () {
            return this.username.length < 30;
        },
        telgood:function () {
            return this.tel.length == 11;
        },
    },
    methods: {
        dochange: function (event) {
            if(!this.emailgood){
                alert("邮箱格式不正确");
            }
            else if(!this.namegood){
                alert("姓名过长");
            }
            else if(!this.telgood){
                alert("请输入正确的手机号");
            }
            else{
                var storlogin = sessionStorage.getItem("login");
                loginobj = fromJSON(storlogin);
                var url = '/myapp/user/change_info';
                var post_data={
                    token:loginobj.data.token,
                    user:{
                        user_name:this.username,
                        user_sex:this.sex,
                        phone:this.tel,
                        addr:this.addr,
                    }
                };
                if (this.email != user.email){
                    post_data.user.email = this.email;
                }
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
}