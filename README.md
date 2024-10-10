# Superhero Tracking API

## Description

The **Superhero Tracking API** is designed to facilitate the management of superheroes and their powers. This API enables users to create, read, update, and delete superhero and power entries, as well as link them through the `HeroPower` model.


## Demo

To explore or contribute to the project, follow the setup instructions below.

## Setup/Installation Requirements

To get started, you need the following:

- **Python 3.12** installed on your system.
- A **SQLite3** database for managing hero and power data.
- A terminal (Linux, macOS, or Windows) for running the API.

### Setup Steps:

1. **Clone the Repository**:
   - Go to the repository URL: `https://github.com/yourusername/superhero-tracking-api`.
   - Copy the SSH URL.
   - In your terminal, navigate to your preferred directory and run:
     ```bash
     git clone <SSH URL>
     ```

2. **Install Dependencies**:
   - Open the cloned repository:
     ```bash
     cd server/
     ```
   - Install required Python libraries using pip:
     ```bash
     $ pipenv install 
     $ pipenv shell
     ```

3. **Seed Data**:
   - If needed, you can seed the database with initial data for heroes and powers.
    ```
      $ python seed.py
      ```

6. **Run the Application**:
   - Start the Flask API:
     ```bash
     flask run/ python app.py
     ```

7. **Test the API**:
   - Use Postman to test the endpoints as defined in the provided collection.

## Technologies Used

- **Python 3.12**: Core language used to build the API.
- **Flask**: Web framework for building the API.
- **SQLite3**: Database for storing hero and power information.
- **SQLAlchemy**: ORM used for database interactions and ensuring data integrity.
- **Flask-Migrate**: Extension for handling database migrations.
- **Postman**: Tool for testing API endpoints.

---
