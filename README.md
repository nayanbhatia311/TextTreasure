
## Introduction

`TextTreasure` is a Flask-based application designed to provide an interface for users to interact and make queries. The main entry point is the `app.py` file which serves the `index.html` for the front end.

## Features

1. **User Authentication**: Users can register and manage their accounts.
2. **Natural Language Processing**: Utilizes the OpenAI language model for various tasks, potentially for generating embeddings or answering questions.
3. **Database Integration**: Uses Astra DB (a cloud-native Cassandra database) for storing and retrieving data.


## Environment Setup:

1. Ensure you have Python 3.8 installed. You can check your Python version with the following:

```
python --version
```

If you have multiple versions of Python installed, you might need to use `python3.8` instead of `python`.

2. Set the required environment variables (.env):

```
FLASK_SECRET_KEY=<your_flask_secret_key>
FLASK_DEBUG=True
FLASK_SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3
FLASK_SQLALCHEMY_ECHO=True
ASTRA_DB_SECURE_BUNDLE_PATH=<your_astra_db_secure_bundle_path>
ASTRA_DB_APPLICATION_TOKEN=<your_astra_db_application_token>
ASTRA_DB_CLIENT_ID=<your_astra_db_client_id>
ASTRA_DB_SECRET=<your_astra_db_secret>
ASTRA_DB_KEYSPACE=<your_astra_db_keyspace>
OPENAI_API_KEY=<your_openai_api_key>
FLASK_JWT_SECRET_KEY=<your_jwt_secret_key>
```

Ensure to replace placeholders (e.g., `<your_flask_secret_key>`) with your actual values.


## File Structure:

auth.py: Handles user authentication and JWT token management. Provides routes for login, logout, and token refresh.
home.py: Contains the main application routes, integrates with Cassandra for database interactions, and supports document text extraction.
models.py: Defines the ORM models for the application, such as the User model.
users.py: Provides routes for user-related operations like fetching user details.
add_vector_embeddings.py: Integrates with the Cassandra database to add vector embeddings from the `docx` folder. Uses the OpenAI API for vector generation.
app.py: Initializes the Flask app, loads environment variables, and registers blueprints.
schemas.py: Contains Marshmallow schemas for data serialization, including the UserSchema.
requirements.txt: Lists all the Python package dependencies required to run the application.
extensions.py: Initializes extensions like SQLAlchemy and JWTManager for the Flask app.



## Setup

1. Install the required packages using the provided `requirements.txt`.
2. Initialize the database and run migrations if necessary.
3. Start the Flask application.

## Steps:


### Setting Up a Virtual Environment

Before you begin, please make sure you have Python 3.8 installed. 

1. **Install virtualenv** (if you haven't already):

```bash
pip install virtualenv
```

2. **Navigate to your project directory**:

```bash
cd path_to_your_project_directory
```

3. **Create a virtual environment**:

```bash
virtualenv venv
```

This will create a new directory named `venv` in your project directory.

4. **Activate the virtual environment**:

- **On macOS and Linux**:

```bash
source venv/bin/activate
```

- **On Windows**:

```bash
.\venv\Scripts\activate
```

Once activated, your terminal prompt will change to show the name of the activated environment.

5. **Install the required packages inside the virtual environment**:

```bash
pip install -r requirements.txt
```

Now, you can run your project inside this virtual environment. When you're done working on your project, you can deactivate the virtual environment by simply typing:

```bash
deactivate
```




#### Convert DOCX to Embeddings:

Execute the following command to convert DOCX files into vector embeddings:

```bash
python add_vector_embeddings.py
```

#### Start the Flask Server:

Once the embeddings are generated, run the Flask server using:

```bash
python app.py
```

This will start the Flask application, and you should be able to access it via your web browser on port 5001.




