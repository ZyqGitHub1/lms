var storlogin = sessionStorage.getItem("login");
var loginobj = fromJSON(storlogin);
var request = window.superagent;
var $table = $('#dataTables-example');
var _table = $table.dataTable($.extend(
    true,{},CONSTANT.DATA_TABLES.DEFAULT_OPTION, {
        "ajax": function(data, callback, settings) {//ajax配置为function,手动调用异步查询
            var param = {
                token:loginobj.data.token,
            };
            $.ajax({
                type: "POST",
                url: "/bookManage/allFine",
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
                data: null,
            },
            {
                data: null,
            },
            {
                data : null,
            },
            {
                data : null,
            },
            {
                data : null,
            },
            {
                data : null,
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
            $('td', row).eq(1).empty();
            $('td', row).eq(2).empty();
            $('td', row).eq(3).empty();
            $('td', row).eq(4).empty();
            $('td', row).eq(5).empty();
            $('td', row).eq(6).empty();
            $('td', row).eq(1).append(data[0].user_id);
            $('td', row).eq(2).append(data[0].user_email);
            $('td', row).eq(3).append(data[0].pay_money);
            $('td', row).eq(4).append(data[0].pay_state);
            $('td', row).eq(5).append(data[0].pay_date);
            $('td', row).eq(6).append(data[0].operate_id);
            var $btnBack = $('<a>缴纳</a>');
            $btnBack.on(
                'click',
                function () {
                    showfine(data);
                }
            );
            console.log(data);
            $('td', row).eq(7).append($btnBack);
        },
    })
).api()

$('#dataTables-example tbody').on(
    'click', 'td.details-control',
    function() {
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

function showfine(data) {
    $("#fine_user_id").val(data[0].user_id);
    $("#fine_money").val(data[0].pay_money);
    $("#fineModal").modal("show");
}

function dofine() {
    var url = '/bookManage/finePayment';
    var post_data={
        token:loginobj.data.token,
        user:{
            'user_id':$("#fine_user_id").val()
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
                alert("缴纳成功");
                _table.ajax.reload();
                $("#fineModal").modal('toggle');
            }
        })
}