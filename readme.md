## Basic Setup Commands

Follow these steps to set up and run the project:

### 1. Clone the Repository

```bash
git clone https://github.com/amritBskt/restaurantBackendAPI.git
cd restaurantBackendAPI
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

Before running the server, apply migrations to set up your database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```
- `makemigrations` creates new migration files based on the changes detected in your models.
- `migrate` applies those migrations to your database, creating or updating tables as needed[1][2][3].

### 5. Run the Development Server

```bash
python manage.py runserver
```
- The server will start, typically at `http://127.0.0.1:8000/` (check your console output).

## API Documentation

Interactive API documentation is available at the **Swagger endpoint** (=`/swagger/`). Visit this URL in your browser after starting the server to explore and test the API endpoints.

**Note:** Adjust the Swagger URL if your project uses a different path for documentation.
