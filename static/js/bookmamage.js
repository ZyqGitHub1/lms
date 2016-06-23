var request = window.superagent;
    var storlogin = sessionStorage.getItem("login");
    loginobj = fromJSON(storlogin);
    var url = '/bookManage/allBook';
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
                console.log(response.body.data);
                booklist = response.body.data;
                var $wrapper = $('#dataTable_wrapper');
                var $table = $('#dataTables-example');
                var _table = $table.dataTable($.extend(
        true,{},CONSTANT.DATA_TABLES.DEFAULT_OPTION, {
        "data":booklist,
        // "aoColumns": [
        //     {"mDataProp": "book_id",},
        //     {"mDataProp": "book_no"},
        //     {"mDataProp": "book_name"},
        //     {"mDataProp": "book_writer"},
        //     {"mDataProp": "book_publish"},
        //     {"mDataProp": "book_price"},
        //     {"mDataProp": "book_date"},
        //     {"mDataProp": "book_class"},
        //     {"mDataProp": "book_main"},
        //     {"mDataProp": "book_prim"},
        //     {"mDataProp": "book_state"},
        //     {"mDataProp": "book_rno"},
        //     {"mDataProp": "book_id"},
        // ],
        columns: [
            {
                className : "ellipsis", //文字过长时用省略号显示，CSS实现
                data: "book_id",
                render : CONSTANT.DATA_TABLES.RENDER.ELLIPSIS,//会显示省略号的列，需要用title属性实现划过时显示全部文本的效果
            },
            {
                className : "ellipsis",
                data: "book_no",
                render : CONSTANT.DATA_TABLES.RENDER.ELLIPSIS,
                //固定列宽，但至少留下一个活动列不要固定宽度，让表格自行调整。不要将所有列都指定列宽，否则页面伸缩时所有列都会随之按比例伸缩。
                //切记设置table样式为table-layout:fixed; 否则列宽不会强制为指定宽度，也不会出现省略号。
                width : "80px"
            },
            {
                data : "book_name",
                width : "80px",
            },
            {
                data : "book_writer",
                width : "80px"
            },
            {
                data : "book_publish",
                width : "80px"
            },
            {
                data : "book_price",
                width : "80px"
            },
            {
                data : "book_date",
                width : "80px"
            },
            {
                data : "book_class",
                width : "80px"
            },
            {
                data : "book_main",
                width : "80px"
            },
            {
                data : "book_prim",
                width : "80px"
            },
            {
                data : "book_state",
                width : "80px"
            },
            {
                data : "book_rno",
                width : "80px"
            },
            {
                className : "td-operation",
                data: null,
                defaultContent:"",
                orderable : false,
                width : "120px"
            }
        ],
        "createdRow": function ( row, data, index ) {
            //行渲染回调,在这里可以对该行dom元素进行任何操作
            //不使用render，改用jquery文档操作呈现单元格
            var $btnEdit = $('<button type="button" class="btn btn-small btn-primary btn-edit">修改</button>');
            var $btnDel = $('<button type="button" class="btn btn-small btn-danger btn-del">删除</button>');
            $('td', row).eq(12).empty();
            $('td', row).eq(12).append($btnEdit).append($btnDel);
        },
    })).api();
            }
        });