$(document).ready(function() {
   
    function loaddata(dateRange){
        var endpointUrl = window.endpointUrl;
        var table = $('#table-3').DataTable();
        $.ajax({
            url: endpointUrl,
            type: 'GET',
            data: {
                dateRange: dateRange,
                limit: 50 // Giới hạn số bản ghi cần lấy là 50// Gửi dateRange như một tham số trong yêu cầu
            },
            dataType: 'json',
            success: function(res) {
        
                table.clear();
                // Thêm các hàng dữ liệu mới
                res.forEach(function(item) {
                    var actionValue = item['action'] === '0x0,' ? 'none' : (item['action'] || 'N/A');
                    table.row.add([
                        item['timestamp'] || 'N/A',
                        actionValue,
                        item['protocol_type'] || 'N/A',
                        item['src_ip'] || 'N/A',
                        item['src_port'] || 'N/A',
                        item['dst_ip'] || 'N/A',
                        item['dst_port'] || 'N/A',
                        item['interface'] || 'N/A',
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



