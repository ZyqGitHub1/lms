function format (d) {
    var child_table = $('<table class="table table-striped table-bordered"></table>')
    var child_table_th = $('<tr>\
                                <th>图书名称</th>\
                                <th>图书编号</th>\
                                <th>罚款金额</th>\
                            </tr>')
    child_table.append(child_table_th);
    $.each(d, function(i,val){
        if (i > 0){
            var tmptr = $('<tr></tr>');
            $('<td>'+ val.book_name +'</td>').appendTo(tmptr);
            $('<td>'+ val.book_id +'</td>').appendTo(tmptr);
            $('<td>'+ val.fine_money +'</td>').appendTo(tmptr);
            child_table.append(tmptr);
        }
    });
    return child_table;










    // return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
    //     '<tr>'+
    //         '<td>作者：</td>'+
    //         '<td>'+d.book_writer+'</td>'+
    //     '</tr>'+
    //     '<tr>'+
    //         '<td>出版社：</td>'+
    //         '<td>'+d.book_publish+'</td>'+
    //     '</tr>'+
    //     '<tr>'+
    //         '<td>价格：</td>'+
    //         '<td>'+d.book_price+'</td>'+
    //     '</tr>'+
    //     '<tr>'+
    //         '<td>日期：</td>'+
    //         '<td>'+d.book_date+'</td>'+
    //     '</tr>'+
    //     '<tr>'+
    //         '<td>摘要：</td>'+
    //         '<td>'+d.book_main+'</td>'+
    //     '</tr>'+
    //     '<tr>'+
    //         '<td>关键字：</td>'+
    //         '<td>'+d.book_prim+'</td>'+
    //     '</tr>'+
    // '</table>';
}