var storlogin = sessionStorage.getItem("login");
var loginobj = fromJSON(storlogin);
var request = window.superagent;
//var $wrapper = $('#dataTable_wrapper');
var $table = $('#dataTables-example');
var _table = $table.dataTable($.extend(
    true,{},CONSTANT.DATA_TABLES.DEFAULT_OPTION, {
        //"data":TESTDATA.BOOKMANAGE,
        "ajax" : function(data, callback, settings) {//ajax配置为function,手动调用异步查询
           var param = {
               token:loginobj.data.token,
           };
           $.ajax({
               type: "POST",
               url: "/userManage/allUser",
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
                    //封装返回数据，这里仅演示了修改属性名
                    var returnData = {};
                    console.log(result.data);
                    returnData.data = result.data;
                    //关闭遮罩
                    //$wrapper.spinModal(false);
                    //调用DataTables提供的callback方法，代表数据已封装完成并传回DataTables进行渲染
                    //此时的数据需确保正确无误，异常判断应在执行此回调前自行处理完毕
                    callback(returnData);
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                   alert("查询失败");
                   //$wrapper.spinModal(false);
                }
            });
        },
            "dom": 'Bfrtip',
            "buttons": [
            'copy', 'excel', 'csv'
            ],
            columns: [
            {
                "class":          'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            {
                data: "user_id",
            },
            {
                data: "user_email",
            },
            {
                data : "user_name",
            },
            {
                data : "user_sex",
            },
            {
                data : "user_borrow",
            },
            {
                data : "user_fine",
            },
            {
                className : "td-operation",
                data: null,
                defaultContent:"",
                orderable : false,
            }
            ],
            "createdRow": function ( row, data, index ) {
            //行渲染回调,在这里可以对该行dom元素进行任何操作
            //不使用render，改用jquery文档操作呈现单元格
            var $btnEdit = $('<a>编辑</a>');
            $btnEdit.on(
                'click',
                function () {
                    showuseredit(data);
                }
            );
            var $btnDel = $('<a>删除</a>');
            $btnDel.on(
                'click',
                function () {
                    showdeleteuser(data);
                }
            );
            console.log(data);
            //$('td', row).eq(7).empty();
            $('td', row).eq(7).append($btnEdit).append("|").append($btnDel);
        },
    })).api()
$('#dataTables-example tbody').on(
        'click', 'td.details-control',
        function () {
            var tr = $(this).closest('tr');
            var row = _table.row( tr );
            if ( row.child.isShown() ) {
                // This row is already open - close it
                row.child.hide();
                tr.removeClass('shown');
            }
            else {
                // Open this row
                row.child( format(row.data()) ).show();
                tr.addClass('shown');
            }
        }
    );
var $btnadd = $('<a href="#" aria-controls="dataTables-example" tabindex="0" data-toggle="modal" dtarget="#addBookModal" class="btn btn-default"><span>添加</span></a>');
$btnadd.on(
    'click',
    function(){
        showadduser();
    }
    )
$("div.dt-buttons").append($btnadd);


function showuseredit(data) {
    $("#user_id").val(data.user_id);
    $("#role_name").val(data.role_name);
    $("#user_email").val(data.user_email);
    $("#user_name").val(data.user_name);
    $("#user_maxborrow").val(data.user_maxborrow);
    $("#user_borrow").val(data.user_borrow);
    $("#user_sex").val(data.user_sex);
    $("#user_phone").val(data.user_phone);
    $("#user_addr").val(data.user_addr);
    $("#user_confirmed").val(data.user_confirmed);
    $("#user_fine").val(data.user_fine);
    $("#user_totalborrow").val(data.user_totalborrow);
    $("#userModal").modal("show");
}
function showadduser() {
    $("#addUserModal").modal("show");
}
var temp_user_id;
function showdeleteuser(data) {
    //$("#b_id").val(data.book_id);
    //$("#b_state").val(data.book_state);
    //$("#b_price").val(data.book_price);
    //$("#b_name").val(data.book_name);
    //$("#b_index").val(data.book_name);
    //$("#b_class").val(data.book_class);
    //$("#b_pos").val(data.book_rno);
    //$("#b_auth").val(data.book_writer);
    //$("#b_addr").val(data.book_publish);
    //$("#b_date").val(data.book_date);
    //$("#b_main").val(data.book_main);
    //$("#b_prim").val(data.book_prim);
    $("#deleteModal").modal("show");
    temp_user_id = data.user_id;

}
function douseredit() {
    var url = '/userManage/updateUserInfo';
    var post_data={
        token:loginobj.data.token,
        user:{
            'user_id': $("#user_id").val(),
            'role_name': $("#role_name").val(),
            'user_email': $("#user_email").val(),
            'user_name': $("#user_name").val(),
            'user_maxborrow': $("#user_maxborrow").val(),
            'user_borrow': $("#user_borrow").val(),
            'user_sex': $("#user_sex").val(),
            'user_phone': $("#user_phone").val(),
            'user_addr': $("#user_addr").val(),
            'user_fine': $("#user_fine").val(),
            'user_totalborrow': $("#user_totalborrow").val(),
            'user_confirmed': $("#user_confirmed").val(),
            'new_password': $("#user_password").val(),
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
                alert("修改成功");
                _table.ajax.reload();
                $("#userModal").modal('toggle');
            }
    })
}
function doadduser() {
    var url = '/userManage/addUser';
    var post_data={
        token:loginobj.data.token,
        user:{
            'user_id': $("#add_user_id").val(),
            'role_name': $("#add_role_name").val(),
            'user_email': $("#add_user_email").val(),
            'user_name': $("#add_user_name").val(),
            'user_maxborrow': $("#add_user_maxborrow").val(),
            'user_borrow': $("#add_user_borrow").val(),
            'user_sex': $("#add_user_sex").val(),
            'user_phone': $("#add_user_phone").val(),
            'user_addr': $("#add_user_addr").val(),
            'user_fine': $("#add_user_fine").val(),
            'user_totalborrow': $("#add_user_totalborrow").val(),
            'user_confirmed': $("#add_user_confirmed").val(),
            'new_password': $("#add_user_password").val(),
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
                alert("添加成功");
                _table.ajax.reload();
                $("#addUserModal").modal('toggle');
            }
    })
}
function dodeltetuser() {
    var url = '/userManage/deleteUser';
    var post_data={
        token:loginobj.data.token,
        user:{
            'user_id':temp_user_id,
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
                alert("删除成功");
                _table.ajax.reload();
                $("#deleteModal").modal('toggle');
            }
    })
}