
# Job Adverts Application

## Specifications

The application provides the following functionalities:

1. **User Authentication**
   - An API to login and logout users (token authentication is used).

2. **Job Adverts Management**
   - An API to return a list of Job adverts in the database.
     - The response should include:
       - Applicant count
       - Publish status
     - Ordering of the response:
       1. Published adverts
       2. Adverts with the highest applicant count
       3. Recently created adverts

   - An API to retrieve the details of a job advert.
   - An API to update a job advert.
   - An API to delete a job advert.
   - An API to publish and unpublish a job advert.

3. **Job Applications Management**
   - An API to retrieve all the job applications that belong to a job advert.
   - An API to retrieve the details of a single job application.
   - An API to submit a job application for a job advert.
   - An API to delete a job application.

Click here for [API Endpoints](job_posting.http)

## How to setup locally
# JobBoard

JobBoard is a simple Job Advert API.

## Prerequisites

Before you start, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone this repository:

    ```bash
    git clone https://github.com/OkayJosh/JobPostingApi.git
    cd JobPostingApi
    ```

2. Copy a `.env.example` file in the project root and create a new file as `.env` with the content:
    ```bash
    #!/bin/bash

    # Check if .env.tp exists
    if [ ! -f .env.example]; then
        echo "Error: .env.example file not found. Please make sure .env.example exists in the project root."
        exit 1
    fi

    # Copy .env.tp to .env
    cp .env.example .env

    echo "Successfully copied .env.example to .env"
    ```
3. Build and run the Docker containers:

    ```bash
    sudo chmod -R +rX .
   ```
   
   ```bash
    docker compose build
    docker compose up -d
    ```

    then run this seeding:

    ```bash
    docker compose run web
    ```

4. Open your web browser and navigate to [http://0.0.0.0:8000](http://localhost:8000) to access the Django app.
5.  Use password ```5478``` and username ```bent```

## Notes

- The Django app runs on port 8000. You can customize the port in the `docker-compose.yml` file.

- The PostgreSQL database is configured with the credentials specified in the `.env` file.

- Adjust the Django settings and configurations in the `JobPostingApi/settings.py` file as needed.

## Contributing

Feel free to contribute by opening issues or creating pull requests. Contributions are welcome!