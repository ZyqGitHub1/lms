var booklist = [[1,2,3,4,5,6,7,8,9,0,11,12,13]];
$(document).ready(function() {
    var request = window.superagent;

    var $wrapper = $('#dataTable_wrapper');
    var $table = $('#dataTables-example');
    var _table = $table.dataTable($.extend(
        true,{},CONSTANT.DATA_TABLES.DEFAULT_OPTION, {
        "data":booklist,
        "aoColumns": [
            {
                "mDataProp": "id",
                "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                    $(nTd).html("<input type='checkbox' name='checkList' value='" + sData + "'>");
    
            }
            },
            {"mDataProp": "name"},
            {"mDataProp": "job"},
            {"mDataProp": "date"},
            {"mDataProp": "note"},
            {
                "mDataProp": "id",
                "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                    $(nTd).html("<a href='javascript:void(0);' " +
                    "onclick='_editFun(\"" + oData.id + "\",\"" + oData.name + "\",\"" + oData.job + "\",\"" +  oData.note + "\")'>编辑</a>&nbsp;&nbsp;")
                        .append("<a href='javascript:void(0);' onclick='_deleteFun(" + sData + ")'>删除</a>");
                }
            },
    ],
        "createdRow": function ( row, data, index ) {
            //行渲染回调,在这里可以对该行dom元素进行任何操作
            //不使用render，改用jquery文档操作呈现单元格
            var $btnEdit = $('<button type="button" class="btn btn-small btn-primary btn-edit">修改</button>');
            var $btnDel = $('<button type="button" class="btn btn-small btn-danger btn-del">删除</button>');
            $('td', row).eq(12).append($btnEdit).append($btnDel);
        },
    })).api();
});

function query_book(){
    var storlogin = sessionStorage.getItem("login");
    loginobj = fromJSON(storlogin);
    var url = '/myapp/user/change_info';
    var post_data={
        token:loginobj.data.token
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
                booklist = body.books;
            }
        });
}