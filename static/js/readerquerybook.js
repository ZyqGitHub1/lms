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
               url: "/bookManage/allBook",
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
                "class":          'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            {
                data: "book_id",
            },
            {
                data: "book_no",
            },
            {
                data : "book_name",
            },
            {
                data : "book_class",
            },
            {
                data : "book_state",
            },
            {
                data : "book_rno",
            },
            ],
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