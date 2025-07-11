# personal-notes-manager-7444eae1

## Backend API (Django REST)

### User Authentication
- **POST /api/auth/register/** — Register a new user. Request JSON: `{ "username": "user", "password": "pass" }`
- **POST /api/auth/login/** — Login and obtain token. Request JSON: `{ "username": "user", "password": "pass" }`  
  Response: `{ "token": "...", "user": ... }`
- **POST /api/auth/logout/** — Logout (revoke token, requires authentication).
- **GET /api/auth/user/** — Get current authenticated user's data.

### Notes CRUD & Search (All require login token in `Authorization: Token <token>` header)
- **GET /api/notes/** — List notes (supports `search=<query>`, order by `?ordering=created_at`).
- **POST /api/notes/** — Create note. Body: `{ "title": "...", "content": "..." }`
- **GET /api/notes/{id}/** — Retrieve note.
- **PUT/PATCH /api/notes/{id}/** — Update note.
- **DELETE /api/notes/{id}/** — Delete note.

### Health
- **GET /api/health/** — Check status.

### Schema & API Documentation
- **/docs/** — Swagger UI API docs.
- **/redoc/** — ReDoc API docs.
- **/swagger.json** — OpenAPI schema.

> Token authentication is default; include header `Authorization: Token <token>` in all requests after login.

---

### Database
Default: SQLite (`db.sqlite3`).  
To upgrade to PostgreSQL, see `notes_database.md`.

---

### Setup
- Run migrations: `python manage.py makemigrations && python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Run server: `python manage.py runserver`