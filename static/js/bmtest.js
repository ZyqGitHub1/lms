var $wrapper = $('#dataTable_wrapper');
                var $table = $('#dataTables-example');
                var _table = $table.dataTable($.extend(
        true,{},CONSTANT.DATA_TABLES.DEFAULT_OPTION, {
        "data":TESTDATA.BOOKMANAGE,
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