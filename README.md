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
│── src/ # Source code 
│── deploy/ # Scripts for deployment 
├── setup_cloudwatch_event.sh #Bash script for CloudWatch event configuration
│   ├── database/ # Database interactions 
│   │   ├── __init__.py 
│   │   ├── connection.py # PostgreSQL connection (asyncpg) 
│   │   ├── queries.py # SQL queries 
│   │   ├── repository.py # Fetching data (100-record chunks) 
│   ├── services/ # Core business logic 
│   │   ├── __init__.py 
│   │   ├── feed_generator.py # Generates JSON feed files 
│   │   ├── metadata_generator.py # Creates metadata file 
│   │   ├── s3_uploader.py # Uploads to AWS S3 (aioboto3) 
│   │   ├── scheduler.py # Scheduled execution (AWS Fargate) 
│   ├── utils/ # Utility modules 
│   │   ├── __init__.py 
│   │   ├── config.py # Configuration (dotenv) 
│   │   ├── logger.py # Logging 
│   │   ├── error_handler.py # Error handling 
│── tests/ # Unit and integration tests 
│   ├── test_database.py # Mock database test 
│   ├── test_feed_generator.py # JSON feed generator test 
│   ├── test_metadata_generator.py # Metadata generator test 
│   ├── test_s3_uploader.py # Mock AWS S3 upload test 
│   ├── test_scheduler.py # Mock scheduler test 
│── .github/ # CI/CD pipeline 
│   ├── workflows/ 
│   │   ├── ci-cd.yml # GitHub Actions for deployment 
│── Dockerfile # Docker container definition
├── .dockerignore # Ignore unnecessary files 
├── README.md # Project documentation 
│── .env.sample # Sample environment variables 
│── requirements.txt # Dependencies 
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