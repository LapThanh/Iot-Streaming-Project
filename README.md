Chào mừng bạn đến với dự án Iot-Streaming-Project! Đây là một dự án mô phỏng và xử lý dữ liệu IoT theo thời gian thực, áp dụng các công nghệ tiên tiến như Apache Kafka, Apache Spark, và TimescaleDB. Mục tiêu của dự án là xây dựng một hệ thống có khả năng tạo, truyền tải, xử lý, và lưu trữ dữ liệu IoT từ các cảm biến giả lập.

Mục Tiêu Dự Án
Dự án này được thiết kế nhằm đáp ứng nhu cầu xử lý dữ liệu thời gian thực trong các hệ thống IoT. Cụ thể, nó giúp thu thập và xử lý dữ liệu từ nhiều loại cảm biến như cảm biến nhiệt độ, cảm biến chuyển động, chất lượng không khí, và dữ liệu hành trình của phương tiện.

Các Thành Phần Chính
Tạo Dữ Liệu Giả Lập:

Script: FakeData.py, Fake_Error.py
Mô tả: Sử dụng thư viện Faker để tạo dữ liệu giả lập cho các thiết bị IoT, bao gồm cả việc tạo lỗi có chủ đích để mô phỏng các tình huống thực tế.
Truyền Dữ Liệu Lên Kafka:

Script: ProducerToToppic.py
Mô tả: Dữ liệu được truyền tải lên các topic của Kafka để phục vụ cho việc xử lý thời gian thực.
Xử Lý Dữ Liệu Với Apache Spark:

Script: SparkConsumer.py
Mô tả: Dữ liệu từ Kafka được Spark xử lý, bao gồm cả việc làm sạch và chuẩn hóa dữ liệu trước khi lưu trữ vào TimescaleDB.
Lưu Trữ Dữ Liệu Vào TimescaleDB:

Script: CreateHypertable.sql
Mô tả: Dữ liệu sau khi được xử lý sẽ được lưu trữ trong TimescaleDB dưới dạng các hypertable, giúp tối ưu hóa cho các truy vấn thời gian thực.
Dockerized Environment:



Xây dựng và khởi động các container:
bash
Copy code
docker-compose up --build
Tạo Dữ Liệu Giả Lập:

Chạy script tạo dữ liệu và truyền tải lên Kafka:
bash
Copy code
python FakeData.py
Xử Lý Dữ Liệu:

Chạy Spark để xử lý dữ liệu từ Kafka:
bash
Copy code
spark-submit SparkConsumer.py
Kiến Trúc Hệ Thống
Kafka: Nhận và quản lý các stream dữ liệu từ các thiết bị IoT giả lập.
Spark: Xử lý và làm sạch dữ liệu theo thời gian thực trước khi lưu trữ.
TimescaleDB: Lưu trữ dữ liệu đã được xử lý cho các truy vấn phân tích sau này.
Dự án này không chỉ là một bài tập kỹ thuật, mà còn là một minh họa mạnh mẽ về cách sử dụng các công cụ dữ liệu lớn và thời gian thực để giải quyết các bài toán phức tạp trong lĩnh vực IoT.

