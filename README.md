# Sample_CRUD_REST_API

Sample CRUD REST API based on Python's FastAPI framework and MySQL database.<br><br>
This project was created as a recruitment task and demonstrates basic CRUD (Create, Read, Update, Delete) operations.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Created by](#created-by)

## Features

- **CRUD Operations**: Create, Read, Update, Delete operations for Parents and Children entities.
- **TDD**: The application was made according to the TDD methodology.
- **MySQL Integration**: Persistent storage using a MySQL database.
- **Pydantic**: Pydantic is used for data modeling, ensuring structured and automatically validated data.
- **Dockerized Setup**: Easy deployment and testing with Docker and Docker Compose.
- **API Documentation**: Automatically generated API docs using FastAPI's Swagger UI.
- **Continuous Integration**: CI implemented using Github Actions.

## Tech Stack

- Python version: 3.11
- FastAPI version: 0.112.1
- MySQL version: 8.0
- Others: see "requirements.txt"

## Installation

### Prerequisites

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

### Setup

**Clone the repository**:

    ```
    git clone https://github.com/yourusername/Sample_CRUD_REST_API.git
    cd Sample_CRUD_REST_API
    ```

## Running the Application

After installing docker and cloning git repository, build backend locally by entering:

    ```
    docker-compose up --build
    ```

This will start the MySQL database, Redis, and FastAPI application.<br>
The API will be accessible at http://localhost:8000.

## API Documentation

FastAPI automatically generates interactive API documentation at:

Swagger UI: http://localhost:8000/docs

## Created by

Radomir Niewiadomski

