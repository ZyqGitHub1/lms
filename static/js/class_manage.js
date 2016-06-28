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
               url: "/bookManage/allBookClasses",
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
                   $.alert("查询失败");
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
                data: "book_class_id",
            },
            {
                data: "book_class_name",
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
                    showedit(data);
                }
            );
            var $btnDel = $('<a>删除</a>');
            $btnDel.on(
                'click',
                function () {
                    showdeleteclass(data);
                }
            );
            console.log(data);
            //$('td', row).eq(7).empty();
            $('td', row).eq(2).append($btnEdit).append("|").append($btnDel);
        },
    })).api()
var $btnadd = $('<a href="#" aria-controls="dataTables-example" tabindex="0" data-toggle="modal" dtarget="#addBookModal" class="btn btn-default"><span>添加</span></a>');
$btnadd.on(
    'click',
    function(){
        showaddclass();
    }
    )
$("div.dt-buttons").append($btnadd);
function showclassedit(data) {
    $("#b_id").val(data.book_id);
    $("#b_state").val(data.book_state);
    $("#classModal").modal("show");
}
function showaddclass() {
    $("#addclassModal").modal("show");
}
function showdeleteclass(data) {
    $("#delete_class_name").val(data.book_class_name);
    $("#deleteclassModal").modal("show");
}
function doclassedit() {
    var url = '/bookManage/updateBook';
    var post_data={
        token:loginobj.data.token,
        book:{
            'book_id':$("#b_id").val(),
            'book_no':$("#b_index").val(),
            'book_name':$("#b_name").val(),
            'book_writer':$("#b_auth").val(),
            'book_publish':$("#b_addr").val(),
            'book_price':$("#b_price").val(),
            'book_date':$("#b_date").val(),
            'book_class':$("#b_class").val(),
            'book_main':$("#b_main").val(),
            'book_prim':$("#b_prim").val(),
            'book_state':$("#b_state").val(),
            'book_rno':$("#b_pos").val()
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
                $("#bookModal").modal('toggle');
            }
    })
}
function doaddclass() {
    var url = '/bookManage/addBookClasses';
    var post_data={
        token:loginobj.data.token,
        book:{
            'book_class':$("#add_class_name").val(),
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
                $("#addclassModal").modal('toggle');
            }
    })
}
function dodeltetclass() {
    var url = '/bookManage/deleteBookClasses';
    var post_data={
        token:loginobj.data.token,
        book:{
            'book_class':$("#delete_class_name").val(),
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
                $("#deleteclassModal").modal('toggle');
            }
    })
}