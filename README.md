# Facility Feed Service

## Overview
Facility Feed Service is an **asynchronous Python service** that:
- **Fetches facility data from PostgreSQL**
- **Generates JSON feed files**
- **Compresses them using GZIP and uploads them to AWS S3**
- **Creates metadata about uploaded files**
- **Runs on a schedule using AWS ECS Fargate**

---

## 📦 Technologies

- Python 3.11
- Asyncio, asyncpg
- Docker
- AWS ECS Fargate
- AWS S3
- AWS EventBridge (CloudWatch Events)
- GitHub Actions

## **Project Architecture**


```
facility_feed_service/
│
├── src/                        # 📦 Main source code
│   ├── database/               # 📊 Database access layer (PostgreSQL)
│   │   ├── __init__.py
│   │   ├── connection.py       # Handles async DB connection via asyncpg
│   │   ├── queries.py          # Raw SQL queries
│   │   ├── repository.py       # Data fetching with pagination
│   │
│   ├── services/               # ⚙️ Core business logic
│   │   ├── __init__.py
│   │   ├── feed_generator.py   # Generates JSON feed data
│   │   ├── metadata_generator.py # Creates metadata JSON file
│   │   ├── s3_uploader.py      # Uploads files to AWS S3 via aioboto3
│   │   ├── main.py             # Entry point script (runs on schedule in AWS Fargate)
│   │
│   ├── utils/                  # 🔧 Utility and helper modules
│       ├── __init__.py
│       ├── config.py           # Loads environment variables via dotenv
│       ├── logger.py           # Logging configuration
│       ├── error_handler.py    # Optional error handling helpers
│
├── deploy/                    # 🚀 Deployment-related scripts and files
│   ├── setup_cloudwatch_event.sh # Bash script to configure AWS CloudWatch EventBridge
│
├── tests/                     # ✅ Unit and integration tests
│   ├── test_database.py
│   ├── test_feed_generator.py
│   ├── test_metadata_generator.py
│   ├── test_s3_uploader.py
│   ├── test_scheduler.py
│
├── .github/                   # ⚙️ GitHub Actions CI/CD workflows
│   └── workflows/
│       └── ci-cd.yml          # CI/CD pipeline configuration
│
├── Dockerfile                 # 🐳 Docker container definition
├── .dockerignore              # Files/folders to exclude from Docker builds
├── .env.sample                # Sample environment variable configuration
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
 
```
## 🚀 How to Run
1. Install Dependencies
```bash
  pip install -r requirements.txt
```
2. Set Environment Variables(use .env.sample)
#### Important: 
Make sure you have created database with valid credentials
3. Run the Scheduled Task Manually
    ```bash
    python src/services/main.py
    ```
#### 🐳 Optional: Run in Docker
```bash
    docker build -t facility-feed .
    docker run --env-file src/.env facility-feed  
```
## ☁️ Deployment via GitHub Actions
#### Add the following secrets:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- ECR_REPOSITORY
#### After pushing in main docker image will be automatically push the image to AWS ECR

## ⏱️ Automated Execution via CloudWatch
#### The project is configured to automatically trigger the ECS #task in the #cluster every hour using AWS EventBridge.

#### You can configure it using the deployment script:
```bash
  deploy/setup_cloudwatch_event.sh
```
### Important:
#### This script was tested for the region eu-north-1. For other regions it could be different!