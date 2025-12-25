# Product Catalog Django

A structured Django starter with DRF, environment-based settings, custom user model, and Docker Compose.

## Quick start (local)

1. Create and activate a virtualenv.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy env template and adjust values:

```bash
cp .env.template .env
```

4. Run migrations and start server:

```bash
python manage.py migrate
python manage.py runserver
```

## Docker

```bash
docker compose up --build
```

## Settings

- Default settings module: `core.settings.dev` (local dev)
- Production entrypoint: `core.settings.prod`

## Notes

- Custom user model: `users.CustomUser`
- Auditable base model: `common.AuditableModel`
