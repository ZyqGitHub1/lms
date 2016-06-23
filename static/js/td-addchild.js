function format ( d ) {
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>作者：</td>'+
            '<td>'+d.book_writer+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>出版社：</td>'+
            '<td>'+d.book_publish+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>价格：</td>'+
            '<td>'+d.book_price+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>日期：</td>'+
            '<td>'+d.book_date+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>摘要：</td>'+
            '<td>'+d.book_main+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>关键字：</td>'+
            '<td>'+d.book_prim+'</td>'+
        '</tr>'+
    '</table>';
}