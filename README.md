# Real-Time Smart City Data Pipeline

## Project Overview
This project implements a real-time end-to-end big data pipeline for smart city traffic monitoring.
The pipeline processes streaming traffic data (city, speed, congestion) using Apache Kafka and
Spark Structured Streaming, stores results in PostgreSQL, and visualizes insights using Grafana.

This project is a custom rebuild of an open-source GitHub project as part of the ICS 574 course.

---

## System Architecture

Kafka (Data Ingestion)
→ Spark Streaming (Processing)
→ PostgreSQL (Storage)
→ Grafana (Visualization)

---

## Technologies Used
- Apache Kafka
- Apache Spark (Structured Streaming)
- PostgreSQL
- Grafana
- Docker & Docker Compose
- Python (PySpark)

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/smartcity-data-pipeline.git
cd smartcity-data-pipeline


2. Start all services
docker compose up --build

3. Run Spark Streaming Job
docker exec -it smartcity-spark-master bash
/opt/spark/bin/spark-submit /opt/spark-apps/kafka_to_postgres.py

4. Send Data via Kafka Console
docker exec -it smartcity-kafka bash
kafka-console-producer.sh --broker-list localhost:9092 --topic smartcity_events


Example message:

{"city":"Riyadh","speed":65,"congestion":3}

Grafana Dashboards

The following dashboards were created:

Top 5 Most Congested Cities

Top 5 Speeding Cities