var storlogin = sessionStorage.getItem("login");
loginobj = fromJSON(storlogin);
console.log(loginobj);
var request = window.superagent;
var url = '/myapp/user/get_info';

var tokendata = {
        token: loginobj.data.token
};
    
request.post(url)
.send(tokendata)
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
            sessionStorage.setItem('user',toJSON(response.body.user));
            viewinfo(response.body.user)
        }
    });