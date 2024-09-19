$(document).ready(function() {
   
    function loaddata(dateRange){
        var endpointUrl = window.endpointUrl;
        var table = $('#table-3').DataTable();
        $.ajax({
            url: endpointUrl,
            type: 'GET',
            data: {
                dateRange: dateRange // Gửi dateRange như một tham số trong yêu cầu
            },
            dataType: 'json',
            success: function(data) {
                // Xóa dữ liệu cũ trong bảng
                table.clear();
                // Thêm các hàng dữ liệu mới
                data.forEach(function(item) {
                    table.row.add([
                        item['timestamp'] || 'N/A',
                        item['hostname'] || 'N/A',
                        item['protocol_type'] || 'N/A',
                        item['src_ip'] || 'N/A',
                        item['src_port'] || 'N/A',
                        item['dst_ip'] || 'N/A',
                        item['dst_port'] || 'N/A',
                        item['action'] || 'N/A'
                    ]).draw();
                });
            },
            error: function(xhr, status, error) {
                $('#result-pfsense').html('<p>Error occurred: ' + error + '</p>');
            }
        });
    }
    loaddata();
});

