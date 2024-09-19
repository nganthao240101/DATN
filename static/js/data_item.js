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
                console.log("test1",response)               // Xóa dữ liệu cũ trong bảng
                table.clear();
                
                // Thêm các hàng dữ liệu mới
                response.rows.forEach(function(item) {
                    let dstIpColor = '';
                    if (item.label=== 1.0) {
                        item.label= 'PortScan';
                    } else {
                        item.label = 'BEGIN';
                    }
                    var rowNode = table.row.add([
                        item.timestamp ||'N/A',
                        item.flow_id || 'N/A',
                        item.source_ip|| 'N/A',
                        item.source_port || 'N/A',
                        item.destination_ip|| 'N/A',
                        item.destination_port|| 'N/A',
                        item.flow_duration|| 'N/A',
                        item.label|| 'N/A',
                    ]).draw().node(); // Lấy node của dòng vừa thêm
                
                    if (item.label=== 'PortScan') {
                        dstIpColor = 'background-color:#e7b6b6';
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
                console.log("demo",dateRange)
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
    setInterval(loadLogpcap, 60000);

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
                    console.log("test:",response)
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
                    response.data.forEach(function(item) {
                        if (item['label'] === '1.0') {
                            item['label'] = 'PortScan';
                        } else {
                            item['label'] = 'BEGIN';
                        }
                    });
    
                    // Sắp xếp dữ liệu với các dòng 'PortScan' lên đầu
                    response.data.sort(function(a, b) {
                        if (a['label'] === 'PortScan' && b['label'] !== 'PortScan') return -1;
                        if (a['label'] !== 'PortScan' && b['label'] === 'PortScan') return 1;
                        return 0;
                    });
                    
                    // Tạo HTML cho bảng dữ liệu
                    var tableBody = '';
                    response.data.forEach(function(item) {
                        let dstIpColor = ''; // Biến để lưu màu sắc của dòng
                    
                        // Kiểm tra và thay đổi giá trị của 'Label'
                         // Kiểm tra và thay đổi giá trị của 'Label'
                    if (item['label'] === 'PortScan') {
                        dstIpColor = 'background-color:#e7b6b6';
                    }
                        console.log(item)
                    
                        // Tạo dòng cho bảng với màu sắc và nội dung phù hợp
                        tableBody += `
                            <tr style="${dstIpColor}">
                                <td>${item['timestamp']}</td>
                                <td>${item['destination_ip']}</td>
                                <td>${item['source_ip']}</td>
                                <td>${item['source_port']}</td>
                                <td>${item['destination_port']}</td>
                                <td>${item['label']}</td>
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
                                            <th>Dst Port</th>
                                            <th>Lable</th>
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

    // lọc theo thời gian
    function filterDataDetect(){
        $('#send-data-time-detect').click(function(event) {
            event.preventDefault();
            var detectFilterTimeUrl = window.detectFilterTimeUrl;
            
            // Gửi file qua AJAX
            $.ajax({
                url: detectFilterTimeUrl,  // Đường dẫn đến server xử lý
                type: 'POST',
                processData: false,  // Không xử lý dữ liệu gửi đi
                contentType: false,  // Không thiết lập loại nội dung (mặc định sẽ tự động thiết lập)
                success: function(response) {
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
                        let dstIpColor = ''; // Biến để lưu màu sắc của dòng
                    
                        // Kiểm tra và thay đổi giá trị của 'Label'
                        if (item['label'] === '1.0') {
                            item['label'] = 'PortScan';
                            dstIpColor = 'background-color:#e7b6b6'; // Đặt màu nền đỏ nếu 'Label' là '1.0'
                        } else {
                            item['label'] = 'BEGIN';
                        }
                    
                        // Tạo dòng cho bảng với màu sắc và nội dung phù hợp
                        tableBody += `
                            <tr style="${dstIpColor}">
                                <td>${item['timestamp']}</td>
                                <td>${item['destination_ip']}</td>
                                <td>${item['source_ip']}</td>
                                <td>${item['source_port']}</td>
                                <td>${item['destination_port']}</td>
                                <td>${item['label']}</td>
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
                                            <th>Dst Port</th>
                                            <th>Lable</th>
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
    filterDataDetect();
});