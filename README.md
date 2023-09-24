# chatgpt_query_bot

## Introduction

`chatgpt_query_bot` is a Flask-based application that provides user authentication functionalities and integrates with external services for natural language processing tasks.

## Features

1. **User Authentication**: Allows users to register and manage their accounts.
2. **Natural Language Processing**: Utilizes the OpenAI language model for various tasks, potentially for generating embeddings or answering questions.
3. **Database Integration**: Uses Astra DB (a cloud-native Cassandra database) for storing and retrieving data.

## Structure

- `main.py`: Initializes and sets up the Flask application.
- `auth.py`: Contains routes and functionalities related to user authentication.
- `models.py`: Defines the data models, including the User model.
- `extensions.py`: Sets up extensions like SQLAlchemy for database operations.
- `mini-qa.py`: Configures and establishes connections with external services like Astra DB and OpenAI.

## Setup

1. Install the required packages using the provided `requirements.txt`.
2. Populate the necessary environment variables in `mini-qa.py`.
3. Initialize the database and run migrations if necessary.
4. Start the Flask application.
