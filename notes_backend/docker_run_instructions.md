# Running Django (notes_backend) on Port 3001

To run the backend API such that it is accessible on port 3001 from outside the container, use:

```bash
python manage.py runserver 0.0.0.0:3001
```

- `0.0.0.0` ensures Django listens on all network interfaces.
- Port `3001` matches the exposed/expected port.

## Docker Compose Example:

```yaml
services:
  notes_backend:
    build: .
    command: python manage.py runserver 0.0.0.0:3001
    ports:
      - "3001:3001"
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings
    volumes:
      - .:/app
```

> If using a Dockerfile or a deployment workflow, make sure to match the `command` above and port mapping!
