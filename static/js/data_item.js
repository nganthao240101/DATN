$(document).ready(function() {
    
    // logpcap
    function loadLogpcap(dateRange){
        var endpointUrl = window.endpointUrl;
        var table = $('#table-3').DataTable();
        $.ajax({
            url: endpointUrl,
            type: 'GET',
            data: {
                dateRange: dateRange // Gửi dateRange như một tham số trong yêu cầu
            },
            dataType: 'json',
            beforeSend: function() {
                $('#load-runing').html('<div class="alert alert-warning-fill alert-dismissible fade in" role="alert"> <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button> <h4>!!! Đang tải dữ liệu</h4> </div>');
            },
            success: function(response) {
                // Xóa dữ liệu cũ trong bảng
                table.clear();
                
                // Thêm các hàng dữ liệu mới
                response.rows.forEach(function(item) {
                    console.log(item)
                    if (item.label==1) {
                        item.label = 'PortScan';
                    } else {
                        item.label = 'BEGIN';
                    }
                    var rowNode = table.row.add([
                        item.timestamp || 'N/A',
                        item.flow_id || 'N/A',
                        item.source_ip || 'N/A',
                        item.source_port || 'N/A',
                        item.destination_ip || 'N/A',
                        item.destination_port || 'N/A',
                        item.flow_duration || 'N/A',
                        item.label || 'N/A',
                    ]).draw().node(); // Lấy node của dòng vừa thêm
                
                    if (item.label === 'PortScan') {
                        $(rowNode).addClass('red-row');
                    }
                });
                $('#count-ip-pcap').text(response.total);
            },
            error: function(xhr, status, error) {
                $('#load-runing').html('<p>Error occurred: ' + error + '</p>');
            },
            complete: function() {
                $('#load-runing').html(''); // Hoặc bạn có thể thay đổi nội dung nếu cần
            }
        });
    }
    loadLogpcap();
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
        loaddata(dateRange);
    });
    // Gọi hàm fetchData mỗi 3 phút
    setInterval(loadLogpcap, 30000);

    // detect
    function loadDetect(){
        $('#detect-submit').click(function(event) {
            event.preventDefault();
            var detectUrl = window.detectUrl;
            // Lấy file từ input
            var fileData = $('#pcap-file').prop('files')[0];
            // Tạo đối tượng FormData
            var formData = new FormData();
            formData.append('pcap-file', fileData);

            // Gửi file qua AJAX
            $.ajax({
                url: detectUrl,  // Đường dẫn đến server xử lý
                type: 'POST',
                data: formData,
                processData: false,  // Không xử lý dữ liệu gửi đi
                contentType: false,  // Không thiết lập loại nội dung (mặc định sẽ tự động thiết lập)
                success: function(response) {
                    console.log("test123",response)
                    $('#content-detect').html(
                        `<h5 class="mb-2">Thống kê</h5><div class="row row-md">
							<div class="col-lg-3 col-md-4 col-sm-6 col-xs-12">
								<div class="box box-block tile tile-2 bg-danger mb-2">
									<div class="t-icon right"><i class="ti-shopping-cart-full"></i></div>
									<div class="t-content">
										<h1 class="mb-1">`+response.count+`</h1>
										<h6 class="text-uppercase">Nghi ngờ tấn công</h6>
									</div>
								</div>
							</div>
						</div>`
                    );
                    // Tạo HTML cho bảng dữ liệu
                    var tableBody = '';
                    response.data.forEach(function(item) {
                        console.log("test909",item)
                        let dstIpColor = ''; // Biến để lưu màu sắc của dòng
                        let portScanCount = 0; 
                    
                        // Kiểm tra và thay đổi giá trị của 'Label'
                        if (item['Label'] ==1) {
                            item['Label'] = 'PortScan';
                            dstIpColor = 'background-color:#e7b6b6'; 
                            portScanCount++;// Đặt màu nền đỏ nếu 'Label' là '1.0'
                        } else {
                            item['Label'] = 'BEGIN';
                        }
                        // console.log("so dem ",portScanCount)
                        // if(item["Label"]==='PortScan'){
                        //     dstIpColor = 'background-color:#e7b6b6'
                        // }
                    
                        // Tạo dòng cho bảng với màu sắc và nội dung phù hợp
                        tableBody += `
                            <tr style="${dstIpColor}">
                                <td>${item['Timestamp']}</td>
                                <td>${item['Dst IP']}</td>
                                <td>${item['Src IP']}</td>
                                <td>${item['Src Port']}</td>
                                <td>${item['Destination Port']}</td>
                                <td>${item['Label']}</td>
                            </tr>`;
                    });
                    $('#table-detect').html(
                        
                        `<div class="box box-block bg-white">
                            <h5 class="mb-1">Danh sách dữ liệu phân tích</h5>
                            <div class="overflow-x-auto">
                                <table class="table table-striped table-bordered dataTable" id="table-3">
                                    <thead>
                                        <tr>
                                            <th>Thời gian</th>
                                            <th>Dst IP</th>
                                            <th>Src IP</th>
                                            <th>Src Port</th>
                                            <th>Destination Port</th>
                                            <th>Label</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ` + tableBody + `
                                    </tbody>
                                </table>
                            </div>
                        </div>`
                    );
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    // Xử lý lỗi
                    alert('Có lỗi xảy ra trong quá trình tải lên');
                }
            });
        });
    };
    loadDetect();

    // phần a sửa tìm kiếm
    $('#send-data-time-detect').click(function(e) {
        e.preventDefault();
        
        var daterange = $('#daterange-input').val();
        var dateRangeArray = daterange.split(' - ');
        
        var startDate = new Date(dateRangeArray[0]);
        var endDate = new Date(dateRangeArray[1]);
    
        function formatDate(date) {
            var day = String(date.getDate()).padStart(2, '0');
            var month = String(date.getMonth() + 1).padStart(2, '0');
            var year = date.getFullYear();
    
            var hours = date.getHours();
            var minutes = String(date.getMinutes()).padStart(2, '0');
            var seconds = String(date.getSeconds()).padStart(2, '0');
    

            var ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12;
            hours = hours ? hours : 12; 
    
            return `${day}/${month}/${year} ${hours}:${minutes}:${seconds} ${ampm}`;
        }
    
        function parseCustomDate(dateString) {
            var dateTimeParts = dateString.split(' '); 
            var dateParts = dateTimeParts[0].split('/'); 
            var timeParts = dateTimeParts[1].split(':'); 
            var ampm = dateTimeParts[2]; 
    
            var day = parseInt(dateParts[0], 10);
            var month = parseInt(dateParts[1], 10) - 1; 
            var year = parseInt(dateParts[2], 10);
    
            var hours = parseInt(timeParts[0], 10);
            var minutes = parseInt(timeParts[1], 10);
            var seconds = parseInt(timeParts[2], 10);
    
            if (ampm === 'PM' && hours < 12) {
                hours += 12;
            }
            if (ampm === 'AM' && hours === 12) {
                hours = 0;
            }
    
            return new Date(year, month, day, hours, minutes, seconds);
        }
    
    
        $('#table-3 tbody tr').each(function() {
            var rowTime = $(this).find('td:first').text();
            
            var rowDate = parseCustomDate(rowTime);
    
            if (!isNaN(rowDate.getTime())) {
                var formattedRowDate = formatDate(rowDate);
    
                if (rowDate >= startDate && rowDate <= endDate) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
    
                $(this).find('td:first').text(formattedRowDate);
            } else {
                console.error('Lỗi chuyển đổi thời gian cho hàng: ', rowTime);
            }
        });
    });
    // hết phần a sửa tìm kiếm
    
});