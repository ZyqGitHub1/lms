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
               	url: "/bookManage/allLost",
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
                data: "book_id",
            },
            {
                data : "book_name",
            },
            {
                data : "user_id",
            },
            {
                data : "pay_money",
            },
            {
                data : "pay_date",
            },
            {
            	data : "admin_id"
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
            var $btnDel = $('<a>删除</a>');
            $btnDel.on(
                'click',
                function () {
                    showRefind(data);
                }
            );
            console.log(data);
            $('td', row).eq(7).append($btnDel);
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

function showRefind(data) {
	$("#refind_book_id").val(data.book_id);
	$("#refind_operate_date").val(data.pay_date);
    $("#refindModal").modal("show");
}

function dorefindbook() {
    var url = '/bookManage/deleteLostBook';
    var post_data={
        token:loginobj.data.token,
        book:{
            'book_id':$("#refind_book_id").val()
        },
        date:{
        	'operate_date':$("#refind_operate_date").val()
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
                alert("成功删除遗失信息");
                _table.ajax.reload();
                $("#refindModal").modal('toggle');
            }
    	})
}