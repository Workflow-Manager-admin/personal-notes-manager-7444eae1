# Notes Database Dependency

This file documents the foundational structure for the `notes_database` dependency, which the `notes_backend` Django service relies on to store and retrieve notes and user data.

## Current Database Setup

- The backend is currently configured to use **SQLite** by default ([see config/settings.py](notes_backend/config/settings.py)).
- This is sufficient for development or lightweight deployments.
- No separate `notes_database` folder or service is required at this stage.

## Production Upgrade Path & Containerization

For production, or to enable independent scaling of the database, follow this approach:
1. **Switch to PostgreSQL (recommended):**
   - Install PostgreSQL and the Python driver (`psycopg2`).
   - Update the `DATABASES` setting in `notes_backend/config/settings.py` as follows:

     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'notes_db',
             'USER': 'youruser',
             'PASSWORD': 'yourpassword',
             'HOST': 'db',  # Use 'localhost' if not using Docker or a separate service
             'PORT': '5432',
         }
     }
     ```

   - Apply Django migrations as usual.
2. **Containerization:**
   - Use a Dockerfile/docker-compose.yml to run a PostgreSQL container named `notes_database`.
   - Set the environment variables for DB access (`DB_NAME`, `DB_USER`, etc.), and update Django settings to use these via `os.environ.get`.

## Migrations & Management

- Run `python manage.py makemigrations` and `python manage.py migrate` to sync models with the database.
- Database files (for SQLite) are created in the project root as `db.sqlite3` by default.

## Connection Example

If you decide to modularize the database into its own container, ensure that any backend code connecting to the DB uses environment variables
for all credentials and endpoints.

### Example .env Variables

```
DB_HOST=notes_database
DB_PORT=5432
DB_NAME=notes_db
DB_USER=notesuser
DB_PASSWORD=...
```

In `settings.py`:

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'notes_db'),
        'USER': os.environ.get('DB_USER', 'notesuser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

---

**Note:**  
No separate code is necessary at this time for `notes_database`, as database interactions are abstracted via Django ORM and settings.
To switch to a different backend, only settings/config/migrations need editing—code does not depend on a custom database interface.
