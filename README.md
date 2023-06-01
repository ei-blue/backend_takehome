
<!-- docker build -t etl-app . -->
<!-- docker run -p 8000:5000 etl-app -->
<!-- curl -X POST http://localhost:8000/etl -->

<!-- 2. Build and the Docker container:
`docker build -t etl-app .`

4. Run the Docker container:
`docker run -p 8000:5000 etl-app` -->

# ETL Pipeline with Flask and Docker

## Description
This project implements a simple ETL (Extract, Transform, Load) pipeline using Flask, Docker, and PostgreSQL. It provides an API endpoint to trigger the ETL process, processes CSV files, derives features, and uploads the processed data into a PostgreSQL database table.

## Prerequisites

Before running the application, make sure you have the following installed on your machine:

- Docker
- PostgreSQL

## Build and Run the Application
1. Clone the repository and navigate to the project directory:

`git clone https://github.com/ei-blue/backend_takehome.git`

`cd backend_takehome`

2. Build and run the Docker containers:
`docker-compose up`

The application will be accessible at http://localhost:8000.


## Check Database Content
To verify the state of the database, you can make an HTTP POST request using any tool that can send HTTP requests, such as curl or Postman.

### Check the Database Before ETL
You can use the following command to check if the database is empty before running the ETL process:
`curl -X POST http://localhost:8000/database`

This should return the response: `{"user_features":[]}`, indicating that the database is currently empty.

## Trigger the ETL process
To trigger the ETL process, you can make an HTTP POST request to the designated endpoint.

### Trigger the ETL Process Using curl
You can use curl to trigger the ETL process by running the following command:
`curl -X POST http://localhost:8000/etl`

This will initiate the ETL process.

## Query the Populated Database Table
After the ETL process has been triggered and completed, you can query the populated database table.

### Check the Database After ETL
To view the populated database content, you can use the following command:
`curl -X POST http://localhost:8000/database`

This will return the response containing the populated user_features table data.

