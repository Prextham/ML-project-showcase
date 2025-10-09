<div align="center">

</div>

Real-Time Fraud Detection Platform & MLOps Showcase
This repository showcases the core architecture and MLOps principles behind a high-throughput, real-time fraud detection system. The goal was to build not just a model, but a robust, scalable, and automated platform capable of processing a live stream of transactions and adapting over time.

Note: This repository contains high-level code snippets and an architectural overview. The full, private codebase is available upon request.

Chapter 1: The Challenge - The Need for Speed and Scale
In fraud detection, a correct prediction that arrives a few seconds too late is useless. The core challenge was twofold:

High Throughput & Low Latency: We needed to process a high-volume stream of transactions and deliver a fraud score in milliseconds (< 200ms per request).

Resilience: The system had to be robust, ensuring no transactions are lost even if one component temporarily fails.

Chapter 2: The Architecture - An Event-Driven Approach
To meet these demands, we designed a scalable, event-driven architecture using a modern data and MLOps stack. This decoupled design allows each component to be scaled and updated independently.

Data Ingestion (Apache Kafka): Acts as the system's central nervous system. Kafka handles the high-velocity stream of incoming transaction data, providing a durable buffer that ensures data integrity.

Model Serving (FastAPI & Docker): The trained XGBoost model was containerized using Docker and served via a high-performance FastAPI endpoint. This setup is built for speed and can handle a large number of concurrent requests efficiently.

The Data Flow: A producer service simulates new transactions by sending them to a Kafka topic. A dedicated consumer service listens to this topic, and upon receiving a new transaction, it immediately calls the FastAPI endpoint to get a fraud prediction.

MLOps & Monitoring (Prometheus & Grafana): The architecture was designed for a full MLOps lifecycle. We built a monitoring stack with Prometheus and Grafana to continuously track model performance (like fraud capture rate and concept drift) and system health (like API latency), ensuring the platform remains reliable and effective over time.

Chapter 3: The Model - XGBoost for Production Performance
For the core prediction task, we chose an XGBoost classifier.

Why XGBoost? In a production environment handling tabular data, XGBoost is an industry champion. It's incredibly fast, memory-efficient, and consistently delivers state-of-the-art performance.

The Core Challenge: Class Imbalance: The most significant modeling challenge was the severe class imbalance (~0.17% fraud cases). A naive model could achieve 99.8% accuracy by simply guessing "not fraud" every time. We solved this by using the scale_pos_weight parameter during training. This technique forces the model to pay significantly more attention to the rare but critical fraudulent class, optimizing for high recall (catching the frauds). The final model successfully identified approximately 85% of fraudulent transactions in the unseen test set.

Chapter 4: Visuals & Results
(This is where you can add a screenshot of a Grafana dashboard showing live metrics, a diagram of the system architecture, or a table of performance metrics like the fraud capture rate.)

Chapter 5: Conclusion
This project was a successful implementation of a complete, end-to-end MLOps platform. We achieved a high fraud capture rate on unseen data while meeting stringent low-latency requirements. More importantly, we built a scalable and automated system that can adapt and improve over time, demonstrating a robust approach to deploying machine learning in a real-world, high-impact environment.