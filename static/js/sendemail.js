var storlogin = sessionStorage.getItem("login");
var loginobj = fromJSON(storlogin);
var param = {
    token:loginobj.data.token,
};
function sendemail(){
$.ajax({
        type: "POST",
        url: "/myapp/user/reconfirm",
        contentType: 'application/json',
     	cache : false,  //禁用缓存
  		data: toJSON(param),    //传入已封装的参数
        dataType: "json",
        success: function(result) {
            //异常判断与处理
            if (!result.successful) {
                alert(result.error.msg);
                return;
            }
            alert("邮件已重新发送");
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("网络错误");
        }
            });
}