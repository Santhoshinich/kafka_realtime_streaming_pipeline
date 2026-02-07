# Real-Time Earthquake Streaming Data Pipeline

Kafka • Spark Structured Streaming • Python • WSL

# Executive Summary

Designed and implemented a production-style real-time data streaming pipeline that ingests live earthquake events, processes them using Apache Spark Structured Streaming, and persists structured outputs for analytics.
This project demonstrates hands-on experience with event-driven architectures, stream processing, and fault-tolerant data pipelines using industry-standard tools.

# Why This Project Matters

Modern data engineering roles demand experience beyond batch ETL.
This pipeline mirrors real-world streaming systems used in:

1. Fraud detection platforms

2. IoT and telemetry pipelines

3. Financial transaction processing

4. Time monitoring and alerting systems

# High-Level Architecture

Live Earthquake API
        ↓
Kafka Producer (Python)
        ↓
Kafka Topic (earthquakes)
        ↓
Spark Structured Streaming
        ↓
Persistent CSV Output (Micro-batches)

# Technology Stack

1. Apache Kafka (KRaft mode) – Distributed event streaming

2. Apache Spark 3.5 (Structured Streaming) – Stream processing engine

3. Python – Kafka producer and Spark job

4. WSL (Ubuntu) – Linux-based execution environment on Windows

5. CSV File Sink – Downstream analytics-ready output

6. Spark Checkpointing – Fault tolerance & recovery

# Project Structure

realtime-earthquake-spark/
│
├── producer/
│   └── earthquake_producer.py      # Kafka producer (Python)
│
├── spark/
│   └── spark_streaming_job.py       # Spark Structured Streaming consumer
│
├── output/
│   ├── csv/                         # Streamed output data (part files)
│   └── checkpoint/                  # Spark streaming state & offsets
│
├── .gitignore
└── README.md

# Data Ingestion

Earthquake data is fetched from a public seismic data feed

## Each event includes:

Event ID

Location

Magnitude

Event timestamp

Latitude & longitude

Events are serialized as JSON and published to Kafka

# Streaming Workflow Breakdown
1️. Kafka Producer

Polls live earthquake data at regular intervals

Transforms raw API responses into structured JSON

Publishes messages to a Kafka topic (earthquakes)

Enables decoupled ingestion and replayability

2️. Kafka Topic

Acts as a durable streaming buffer

Ensures resilience between producers and consumers

Supports scalable, real-time data flow

3️. Spark Structured Streaming

Reads events directly from Kafka

Parses JSON payloads into typed Spark DataFrames

Processes data in micro-batches

Writes structured output to disk with checkpointing enabled

# Output & Storage Behavior

Spark Structured Streaming writes data incrementally:

part-*.csv → actual processed data

_checkpoint/ → streaming metadata for fault tolerance

Checkpoint files are binary and not human-readable — this is expected behavior.

# View processed data:

ls output/csv/
cat output/csv/part-*.csv

# How to Run the Pipeline (WSL – Recommended)

## Prerequisites

WSL (Ubuntu)

Java 11+

Python 3.10+

Apache Kafka 3.7+

Apache Spark 3.5+

Step 1: Start Kafka
cd ~/kafka_2.13-3.7.0
bin/kafka-server-start.sh config/kraft/server.properties

Step 2: Start Kafka Producer
cd /mnt/c/Users/<your-user>/OneDrive/Documents/realtime-earthquake-spark
source venv/bin/activate
python producer/earthquake_producer.py

# Producer output:

Sent: {'id': 'nc75309702', 'place': 'California', 'magnitude': 1.2, ...}

Step 3: Start Spark Streaming Job
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.8 \
  spark/spark_streaming_job.py


# Expected behavior:

Streaming query started. Waiting for data...
-------------------------------------------
Batch: 1
-------------------------------------------
| id | place | magnitude | time | longitude | latitude |

## Data Engineering Concepts Demonstrated

Real-time event ingestion

Kafka-based decoupling

Stream processing with Spark Structured Streaming

Micro-batch execution model

Fault tolerance using checkpoints

Linux-first data engineering (WSL)

Production-aligned pipeline design
