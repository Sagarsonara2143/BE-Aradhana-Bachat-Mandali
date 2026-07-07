# Aaradhana Bachat — Backend (Phase 2)

Django + DRF backend and admin for the Aaradhana Bachat website. Provides public
APIs for the Next.js frontend, JWT-authenticated admin/member APIs, a
content-managed Django admin, and OpenAPI docs.

## Tech stack

- **Django 5.1** + **Django REST Framework**
- **JWT** auth via `djangorestframework-simplejwt` (with blacklist)
- **PostgreSQL** in production (via `DATABASE_URL`); **SQLite** local fallback
- **drf-spectacular** for OpenAPI/Swagger
- Backend media storage (local), upgradeable to S3-compatible later

## Getting started

```bash
cd backend
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt   # Windows
# source .venv/bin/activate && pip install -r requirements.txt  # macOS/Linux

cp .env.example .env
python manage.py migrate
python manage.py seed_demo            # optional reference data
python manage.py createsuperuser
python manage.py runserver
```

- API base: `http://localhost:8000/api/v1/`
- Swagger docs: `http://localhost:8000/api/docs/`
- Django admin: `http://localhost:8000/admin/`

## Database

Configured via `DATABASE_URL`. Leave it unset for a zero-setup local **SQLite**
database. For PostgreSQL parity (recommended, matches production):

```bash
docker compose up -d      # starts Postgres 16
# in .env:
DATABASE_URL=postgres://ab_user:ab_pass@localhost:5432/ab_db
python manage.py migrate
```

## Apps

```txt
apps/
  core/          # audit base model, website settings, envelope renderer, validators
  accounts/      # custom User (roles), JWT auth, permissions
  plans/         # Plan + PlanTableRow, public/admin APIs, maturity calculator
  content/       # legal documents, events/news
  media_library/ # gallery categories/images, videos
  enquiries/     # public enquiry submission + admin management
  members/       # member profiles + admin management
```

## API response envelope

All responses use a consistent shape:

```json
{ "success": true, "data": {}, "message": "Success" }
{ "success": false, "error": {}, "message": "Validation error" }
```

> Frontend note: unwrap `response.data.data` (a single response interceptor in
> `apiClient` handles this cleanly). Paginated lists appear as
> `data: { count, next, previous, results }`.

## Public API contract (for the frontend)

```txt
GET  /api/v1/website-settings/
GET  /api/v1/plans/            GET /api/v1/plans/{slug}/    GET /api/v1/plans/{slug}/tables/
POST /api/v1/plans/calculate/
GET  /api/v1/legal-documents/  GET /api/v1/legal-documents/{slug}/
GET  /api/v1/gallery/categories/   GET /api/v1/gallery/images/?category={slug}
GET  /api/v1/videos/
GET  /api/v1/events/           GET /api/v1/events/{slug}/    (also /news/)
POST /api/v1/enquiries/
POST /api/v1/auth/login/       POST /api/v1/auth/refresh/   POST /api/v1/auth/logout/   GET /api/v1/auth/me/
GET  /api/v1/member/profile/
```

Admin (JWT + admin role) equivalents live under `/api/v1/admin/...`.

## Testing

```bash
python manage.py test
```

Covers auth, public plans list/detail, calculator, admin permissions, legal,
gallery filter, events, and enquiry submission.

## Security

- Env-based secrets; CORS restricted to the frontend origin(s)
- JWT auth; admin APIs require an admin role; public APIs never expose inactive records
- Upload type/size validation; throttling on enquiry + login endpoints

## Before production

- Set `DEBUG=False`, a strong `SECRET_KEY`, real `ALLOWED_HOSTS` / `DATABASE_URL` / `CORS_ALLOWED_ORIGINS`
- `python manage.py collectstatic`; serve behind Gunicorn; persist the media volume
- Confirm the calculator formula with the business before go-live
