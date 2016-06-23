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
        "data":TESTDATA.BOOKMANAGE,
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
            var $btnEdit = $('<a data-toggle="modal" data-target="#bookModal">修改</a>');
            var $btnDel = $('<a>删除</a>');
            //$('td', row).eq(7).empty();
            $('td', row).eq(7).append($btnEdit).append("|").append($btnDel);
        },
    })).api();
        $('#dataTables-example tbody').on('click', 'td.details-control', function () {
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
        });
        var $btnadd = $('<a href="#" aria-controls="dataTables-example" tabindex="0" class="btn btn-default"><span>添加</span></a>');
        $("div.dt-buttons").append($btnadd);
        }
        });