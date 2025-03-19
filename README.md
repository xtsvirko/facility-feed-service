# Facility Feed Service

## Overview
Facility Feed Service is an **asynchronous Python service** that:
- **Fetches facility data from PostgreSQL**
- **Generates JSON feed files**
- **Compresses them using GZIP and uploads them to AWS S3**
- **Creates metadata about uploaded files**
- **Runs on a schedule using AWS ECS Fargate**

---

## **Project Architecture**

# Facility Feed Service Project Structure

```
facility_feed_service/ 
│── src/ # Source code 
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
│── docker/ # Docker setup 
│   ├── Dockerfile # Docker container definition 
│   ├── docker-compose.yml # Local environment (PostgreSQL, service) 
│   ├── .dockerignore # Ignore unnecessary files 
│── docs/ # Documentation 
│   ├── README.md # Project documentation 
│   ├── architecture.md # Detailed architecture 
│── .env.sample # Sample environment variables 
│── pyproject.toml # Python project configuration (Poetry) 
│── requirements.txt # Dependencies 
│
