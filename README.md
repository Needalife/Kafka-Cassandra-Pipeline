
# Kafka-Cassandra Data Pipeline Setup Guide

Welcome to the Kafka-Cassandra data pipeline setup guide. Follow these steps to get everything up and running smoothly.

## 1. Network Setup

First, create separate networks for Kafka and Cassandra to avoid using the default network.

### Kafka Network
```bash
docker network create kafka-network
```

### Cassandra Network
```bash
docker network create cassandra-network
```

## 2. Setting Up Cassandra

### Build the Cassandra Container
```bash
docker-compose -f cassandra/docker-compose.yml up -d
```

### Initialize Keyspaces
Enter the Cassandra container and run the following commands to set up the `faker` and `mathfact` keyspaces:

```bash
cqlsh -f schema-faker.cql
cqlsh -f schema-mathfact.cql
```

### Verify Keyspaces
To verify that the keyspaces are correctly set up, run:

```bash
DESC mathfactdata;   # For mathfact data
DESC fakerdata;      # For faker data
```

## 3. Setting Up Kafka

### Build the Kafka Container
```bash
docker-compose -f kafka/docker-compose.yml up -d
```

### Create a Kafka Cluster
Visit [http://localhost:9000](http://localhost:9000) and create a cluster with the following credentials:

- **Username:** `admin`
- **Password:** `bigbang`
- **Zookeeper Host:** `zookeeper:2181`

### Initialize Sinks
Ensure all sinks are initialized by running the following script in the `kafka-connect` container:

```bash
./start-and-wait.sh
```

## 4. Setting Up Producers and Consumers

### 4.1. OpenWeatherMap Producer

Start the producer that retrieves weather data, including data for Hanoi and London:

```bash
docker-compose -f owm-producer/docker-compose.yml up -d
```

Check the logs to confirm the producer is running correctly.

### 4.2. Faker Producer

Start the Faker producer with 10 data fields:

```bash
docker-compose -f faker-producer/docker-compose.yml up -d
```

Verify the data in the `fakerdata` table:

```bash
SELECT * FROM fakerdata;
```

### 4.3. MathFact Producer

Start the MathFact producer:

```bash
docker-compose -f mathfact-producer/docker-compose.yml up -d
```

Verify the data in the `mathfactdata` table:

```bash
SELECT * FROM mathfactdata;
```

### 4.4. Consumers Setup

Start the consumers (Note: 4 consumers should run, but you'll use only 3):

```bash
docker-compose -f consumers/docker-compose.yml up
```

- **WeatherConsumer:** Check the logs in the `weatherconsumer` container.
- **Cassandra Verification:** Verify the data in Cassandra:

```bash
USE kafkapipeline;

SELECT location, COUNT(*) 
FROM weatherreport 
GROUP BY location;  # Data for each city

SELECT * 
FROM weatherreport;  # All data
```

## 5. Setting Up Visualization

Build the visualization container:

```bash
docker-compose -f data-vis/docker-compose.yml up -d
```

After the container is running, access the visualization tool at:

[http://localhost:8888/lab/tree/blog-visuals.ipynb](http://localhost:8888/lab/tree/blog-visuals.ipynb)

Run the script to visualize your data.

## 6. Stopping All Services

When you're finished, tear down the services in the correct order to avoid errors:

### Stop Services (One by one)
```bash
docker-compose -f data-vis/docker-compose.yml down
docker-compose -f consumers/docker-compose.yml down
docker-compose -f mathfact-producer/docker-compose.yml down
docker-compose -f faker-producer/docker-compose.yml down
docker-compose -f owm-producer/docker-compose.yml down
docker-compose -f kafka/docker-compose.yml down
docker-compose -f cassandra/docker-compose.yml down
```

### Flush Docker (Remove unused containers and images)
```bash
docker system prune -a
```

