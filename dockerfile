# Sử dụng Bitnami Spark image
FROM bitnami/spark:latest

# Cài đặt các gói Spark Kafka
RUN /opt/bitnami/spark/bin/spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 -i /dev/null || true

# Copy các file ứng dụng của bạn vào Docker image
COPY SparkConsumer.py /app/SparkConsumer.py

WORKDIR /opt/bitnami/spark
