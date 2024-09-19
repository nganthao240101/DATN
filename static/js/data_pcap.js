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
                console.log("tes",dateRange)
                // Xóa dữ liệu cũ trong bảng
                table.clear();
                // Thêm các hàng dữ liệu mới
                data.forEach(function(item) {
                    table.row.add([
                        item.timestamp ||'N/A',
                        item.flow_id || 'N/A',
                        item.source_ip|| 'N/A',
                        item.source_port || 'N/A',
                        item.destination_ip|| 'N/A',
                        item.destination_port|| 'N/A',
                        item.flow_duration|| 'N/A',
                        item.label|| 'N/A',
                    ]).draw();
                });
            },
            error: function(xhr, status, error) {
                $('#result').html('<p>Error occurred: ' + error + '</p>');
            }
        });
    }
    loaddata();
    $('#send-data').click(function(event) {
        event.preventDefault();
        var dateRange = $('input[name="daterange-with-time"]').val(); // Lấy giá trị từ input
        console.log("Date Range:", dateRange); 
        loaddata(dateRange);
    });
});