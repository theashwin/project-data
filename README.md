# Building ETL Pipeline Off an SQS Queue

## Installation

### What You'll Need
- Clone of the repository
- Docker (the shipping container for your code)
  - Everything else is fetched by docker through docker-compose.

### Setting Up

1. Clone the repository.
2. Execute `docker-compose up -d` (set up every needed dependency).
3. Test your setup,:
  - Fetch a message from the queue: `awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue`
  - Connect to PostgreSQL and peek at your table: `psql -d postgres -U postgres -p 5432 -h localhost -W` and then `SELECT * FROM user_logins;`

## The Blueprint

```
project-data/
├─ src/                        - Main source folder for the application
│    ├─ services/              - Contains logic for connecting to multiple external services
│      ├─ postgres.py          - Abstract class for managing Postgres Database connections
│      ├─ sqs.py               - Contains logic for SQS queue implementation
│      ├─ user_logins.py       - Manages user login data processing
│    ├─ main.py                - Main entry point for the application
├─ tests/                      - Contains unit tests for the application
│    ├─ test_pii.py            - Tests for PII data masking
├─ .gitignore                  - Specifies files and directories to be ignored by Git
├─ LICENSE                     - License file for the project
├─ docker-compose.yml          - Docker Compose configuration file
├─ Dockerfile                  - Dockerfile to build the application's Docker image
├─ requirements.txt            - Lists required Python packages
├─ README.md                   - Documentation and general information about the project
```

## Test the System

Run `pytest tests/` and see how your code holds up. **This is automatically run while spinning up a docker container**

## Assumptions & Caveats

1. Your SQS Queue isn't a mess; the JSON structure is consistent.
2. PII data needs to irreversibly masked, thus, SHA-256 or SHA-512 is the perfect masking technique which is collision proof.
3. PostgreSQL has its tables set, which it is. **Excluding the fact that "app_version" is integer which forces to remove "."s and convert the string to integer.**
4. Data in the messages are important, which is to say that if a particular field is missing the row is still kept with default values. However, rows containing no important values are discarded.

## Leveling Up

1. Implement error handling and retries (when anything fails).
2. Add logging and monitoring, because you can't fix what you can't see.
3. Schedule this or run it as a service.
4. Batch process for faster performance.
5. Add more robust testing, for now, we are only testing if the masking is correct.

## Going Big League (Production)

1. Consider container orchestration with AWS Fargate or Kubernetes.
2. Add centralized logging with AWS CloudWatch or ELK Stack.
3. Monitor and alert with Grafana, Prometheus, or Datadog.
4. Automate your life with a CI/CD pipeline.

## Scaling Like a Pro

1. Add more instances for horizontal scaling.
2. Tune your database with indexing, partitioning, and sharding.
3. Consider message brokers like Apache Kafka or Amazon Kinesis for high throughput.

Please send your questions and suggestions at anpatil2@illinois.edu