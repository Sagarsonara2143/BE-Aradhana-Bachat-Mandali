# Phase 2 - Backend, Admin Panel, PostgreSQL and Storage Task Breakdown

## Project
Backend and admin system for modern rebuild of `aradhanabachat.com` using **Django DRF + PostgreSQL + Backend-managed storage**.

## Goal
Create a secure backend and admin system to manage website content, plans, legal documents, gallery, videos, events/news, enquiries, members, and login-related APIs.

## Tech Stack

- Backend: Django
- API: Django REST Framework
- Database: PostgreSQL
- Storage: Backend local/media storage initially, upgradeable to S3-compatible storage later
- Auth: JWT-based authentication for admin/member APIs
- Admin: Django Admin plus optional custom admin APIs
- Documentation: Swagger/OpenAPI using drf-spectacular

---

# 1. Backend Project Setup

## 1.1 Create Django Project

### Task
Create Django backend project with DRF.

### Suggested Apps

```txt
apps/
  core/
  accounts/
  plans/
  content/
  enquiries/
  media_library/
  members/
```

### Expected Output
- Django project initialized
- DRF installed and configured
- PostgreSQL configured
- Environment variables configured
- Media/static configuration added

### Acceptance Criteria
- Server runs successfully
- PostgreSQL connection works
- `.env` based configuration exists
- Project has clean app structure

---

# 2. Environment and Configuration

## 2.1 Add Environment Variables

### Required Variables

```txt
DEBUG=
SECRET_KEY=
ALLOWED_HOSTS=
DATABASE_URL=
CORS_ALLOWED_ORIGINS=
MEDIA_ROOT=
MEDIA_URL=
JWT_ACCESS_TOKEN_LIFETIME=
JWT_REFRESH_TOKEN_LIFETIME=
```

### Acceptance Criteria
- No secret is hardcoded
- Local and production config can be separated
- CORS is configured for frontend URL

---

# 3. Database Setup

## 3.1 PostgreSQL Configuration

### Task
Configure PostgreSQL database.

### Acceptance Criteria
- Django migrations run successfully
- Database indexes added where needed
- Admin user can be created

---

# 4. Common Base Models

## 4.1 Create Audit Base Model

### Task
Create reusable abstract model.

### Fields

```txt
id
created_at
updated_at
created_by
updated_by
is_active
```

### Acceptance Criteria
- Common model is reused across apps
- created_by and updated_by are optional where needed
- Soft delete strategy is decided

---

# 5. Authentication and User Management

## 5.1 User Model

### Task
Create custom user model or extend Django user properly.

### Roles
- Super Admin
- Website Admin
- Content Manager
- Member

### Fields
- email
- mobile_number
- full_name
- role
- is_active
- is_staff
- is_superuser

### Acceptance Criteria
- User can login using email/mobile based on requirement
- Admin roles can access admin panel
- Member role can access member APIs only

---

## 5.2 JWT Authentication

### Task
Implement JWT login, refresh, logout APIs.

### APIs

```txt
POST /api/v1/auth/login/
POST /api/v1/auth/refresh/
POST /api/v1/auth/logout/
GET  /api/v1/auth/me/
```

### Acceptance Criteria
- Login returns access and refresh token
- Protected APIs require authentication
- Logout invalidates refresh token if blacklist is used

---

## 5.3 Role-Based Permissions

### Task
Add permission classes.

### Acceptance Criteria
- Public APIs are accessible without login
- Admin create/update/delete APIs require admin role
- Member APIs require member role

---

# 6. Plans Module

## 6.1 Plan Model

### Task
Create savings plan model.

### Fields

```txt
name
slug
plan_type
short_description
description
benefits
terms_conditions
is_featured
sort_order
is_active
```

### Plan Types
- RD Plan
- Term Plan
- DT Plan
- SN Plan

### Acceptance Criteria
- Admin can create/update/delete plans
- Public API can list only active plans
- Slug is unique

---

## 6.2 Plan Table Model

### Task
Create model for plan table rows.

### Example Use Cases
- RD Plan maturity table
- Term Plan premium/fund/surrender table

### Suggested Fields

```txt
plan
label
duration_years
deposit_amount
premium_amount
maturity_amount
interest_rate
fund_value
surrender_value
family_protection
monthly_income
sort_order
metadata JSONField
is_active
```

### Acceptance Criteria
- Flexible enough for different plan tables
- Public API returns table rows under plan detail
- Admin can manage table rows

---

## 6.3 Plans APIs

### Public APIs

```txt
GET /api/v1/plans/
GET /api/v1/plans/{slug}/
GET /api/v1/plans/{slug}/tables/
```

### Admin APIs

```txt
POST   /api/v1/admin/plans/
PATCH  /api/v1/admin/plans/{id}/
DELETE /api/v1/admin/plans/{id}/
POST   /api/v1/admin/plans/{id}/table-rows/
PATCH  /api/v1/admin/plan-table-rows/{id}/
DELETE /api/v1/admin/plan-table-rows/{id}/
```

### Acceptance Criteria
- Public APIs do not expose inactive records
- Admin APIs are protected
- Pagination exists where needed

---

# 7. Plan Calculator API

## 7.1 Calculator Logic

### Task
Create calculator endpoint.

### API

```txt
POST /api/v1/plans/calculate/
```

### Request Example

```json
{
  "plan_type": "RD",
  "monthly_amount": 1000,
  "duration_years": 6
}
```

### Response Example

```json
{
  "total_deposit": 72000,
  "estimated_maturity": 95000,
  "estimated_benefit": 23000,
  "disclaimer": "This calculation is indicative only. Final values are subject to official plan terms."
}
```

### Acceptance Criteria
- Formula is configurable or based on plan table
- API validates inputs
- Disclaimer is always returned
- Business must approve calculation formula before production

---

# 8. Legal Documents Module

## 8.1 Legal Document Model

### Fields

```txt
title
slug
category
document_file
description
published_date
sort_order
is_active
```

### Acceptance Criteria
- Admin can upload PDF/image documents
- Public API lists active documents
- File download URL is returned

---

## 8.2 Legal APIs

### Public APIs

```txt
GET /api/v1/legal-documents/
GET /api/v1/legal-documents/{slug}/
```

### Admin APIs

```txt
POST   /api/v1/admin/legal-documents/
PATCH  /api/v1/admin/legal-documents/{id}/
DELETE /api/v1/admin/legal-documents/{id}/
```

### Acceptance Criteria
- File validation exists
- Only allowed file types accepted
- Download link works

---

# 9. Media Library / Storage

## 9.1 Backend Storage Setup

### Task
Configure backend media storage.

### Initial Storage
- Django local media storage

### Future Upgrade Option
- AWS S3
- DigitalOcean Spaces
- MinIO
- Wasabi

### Acceptance Criteria
- Uploaded files are stored through backend
- File URLs are returned in API response
- File size/type validation exists

---

## 9.2 Media Upload Validation

### Allowed Image Types

```txt
jpg
jpeg
png
webp
```

### Allowed Document Types

```txt
pdf
jpg
jpeg
png
```

### Allowed Video Options
- Store YouTube URL preferred
- Direct upload only if needed and size limit is defined

### Acceptance Criteria
- Invalid file type rejected
- Large files rejected based on configured limit
- Clear validation errors returned

---

# 10. Gallery Module

## 10.1 Gallery Category Model

### Fields

```txt
name
slug
sort_order
is_active
```

## 10.2 Gallery Image Model

### Fields

```txt
title
category
image
caption
event_date
sort_order
is_featured
is_active
```

### Acceptance Criteria
- Admin can manage gallery categories and images
- Public API lists active gallery images
- Featured images can be shown on homepage

---

## 10.3 Gallery APIs

### Public APIs

```txt
GET /api/v1/gallery/categories/
GET /api/v1/gallery/images/
GET /api/v1/gallery/images/?category=events
```

### Admin APIs

```txt
POST   /api/v1/admin/gallery/categories/
PATCH  /api/v1/admin/gallery/categories/{id}/
DELETE /api/v1/admin/gallery/categories/{id}/
POST   /api/v1/admin/gallery/images/
PATCH  /api/v1/admin/gallery/images/{id}/
DELETE /api/v1/admin/gallery/images/{id}/
```

### Acceptance Criteria
- Pagination exists
- Category filter works
- Image URL is returned

---

# 11. Video Gallery Module

## 11.1 Video Model

### Fields

```txt
title
description
video_type
youtube_url
video_file
thumbnail
published_date
sort_order
is_active
```

### video_type Choices
- YOUTUBE
- UPLOAD

### Acceptance Criteria
- YouTube videos can be added
- Uploaded video support is optional
- Public API lists active videos

---

## 11.2 Video APIs

### Public APIs

```txt
GET /api/v1/videos/
GET /api/v1/videos/{id}/
```

### Admin APIs

```txt
POST   /api/v1/admin/videos/
PATCH  /api/v1/admin/videos/{id}/
DELETE /api/v1/admin/videos/{id}/
```

### Acceptance Criteria
- YouTube URL validation exists
- Thumbnail is optional
- Inactive videos are hidden from public API

---

# 12. Events and News Module

## 12.1 Event/News Model

### Fields

```txt
title
slug
type
short_description
content
image
event_date
published_date
is_featured
sort_order
is_active
```

### type Choices
- EVENT
- NEWS

### Acceptance Criteria
- Admin can manage news/events
- Public API lists active items
- Latest items can be shown on homepage

---

## 12.2 Event APIs

### Public APIs

```txt
GET /api/v1/events/
GET /api/v1/events/{slug}/
GET /api/v1/news/
GET /api/v1/news/{slug}/
```

### Admin APIs

```txt
POST   /api/v1/admin/events/
PATCH  /api/v1/admin/events/{id}/
DELETE /api/v1/admin/events/{id}/
```

### Acceptance Criteria
- Latest sorting works
- Detail API works by slug
- Featured filter available if needed

---

# 13. Enquiry Module

## 13.1 Enquiry Model

### Fields

```txt
full_name
mobile_number
email
subject
message
status
admin_notes
created_at
updated_at
```

### Status Choices
- NEW
- IN_PROGRESS
- CLOSED

### Acceptance Criteria
- Public user can submit enquiry
- Admin can view and update status
- Validation exists

---

## 13.2 Enquiry APIs

### Public API

```txt
POST /api/v1/enquiries/
```

### Admin APIs

```txt
GET   /api/v1/admin/enquiries/
GET   /api/v1/admin/enquiries/{id}/
PATCH /api/v1/admin/enquiries/{id}/
```

### Acceptance Criteria
- Spam prevention strategy is considered
- Admin can filter by status
- Public API does not expose all enquiries

---

# 14. Contact and Website Settings

## 14.1 Website Settings Model

### Fields

```txt
site_name
logo
primary_phone
secondary_phone
email
address
google_map_embed_url
facebook_url
instagram_url
youtube_url
whatsapp_number
office_hours
```

### Acceptance Criteria
- Admin can update website settings
- Public API returns settings
- Frontend can use this for header/footer/contact page

---

## 14.2 Website Settings API

### Public API

```txt
GET /api/v1/website-settings/
```

### Admin API

```txt
PATCH /api/v1/admin/website-settings/
```

### Acceptance Criteria
- Only one active settings record is used
- Public API is cache-friendly

---

# 15. Member Module

## 15.1 Member Model

### Task
Create basic member model for future login/member portal.

### Fields

```txt
user
member_code
full_name
mobile_number
email
address
status
joined_date
```

### Status Choices
- ACTIVE
- INACTIVE
- BLOCKED

### Acceptance Criteria
- Member can be linked with user account
- Admin can manage members
- Member APIs are protected

---

## 15.2 Member APIs

### Member APIs

```txt
GET /api/v1/member/profile/
```

### Admin APIs

```txt
GET   /api/v1/admin/members/
POST  /api/v1/admin/members/
GET   /api/v1/admin/members/{id}/
PATCH /api/v1/admin/members/{id}/
```

### Acceptance Criteria
- Member can only view own data
- Admin can manage members
- Member code is unique

---

# 16. Admin Panel

## 16.1 Django Admin Configuration

### Task
Register all models in Django Admin.

### Required Admin Features
- Search fields
- List filters
- Ordering
- Readonly audit fields
- Image/file preview links where possible

### Models To Register
- Users
- Plans
- Plan table rows
- Legal documents
- Gallery categories
- Gallery images
- Videos
- Events/news
- Enquiries
- Website settings
- Members

### Acceptance Criteria
- Admin can manage all website content
- Admin list pages are usable
- File upload works from admin

---

# 17. API Response Standard

## 17.1 Standard Response Format

### Success Example

```json
{
  "success": true,
  "data": {},
  "message": "Success"
}
```

### Error Example

```json
{
  "success": false,
  "error": {},
  "message": "Validation Error"
}
```

### Acceptance Criteria
- API responses are consistent
- Validation errors are frontend-friendly
- Nested validation errors are handled carefully

---

# 18. Pagination, Filtering and Search

## 18.1 Add Pagination

### Task
Use DRF pagination for listing APIs.

### Acceptance Criteria
- Gallery, events, legal documents, enquiries and members are paginated
- Page size is configurable

---

## 18.2 Add Filters

### Required Filters

```txt
plans: plan_type, is_featured
legal: category
Gallery: category, is_featured
Videos: video_type
Events: type, is_featured
Enquiries: status
Members: status
```

### Acceptance Criteria
- Filters work correctly
- Search works for admin list APIs where needed

---

# 19. Security Checklist

## 19.1 Backend Security

### Checklist
- Use environment variables
- Enable CORS only for allowed frontend domains
- Validate file uploads
- Protect admin APIs
- Use JWT authentication
- Add throttling for public enquiry API
- Add throttling for login API
- Do not expose inactive/private records publicly
- Sanitize rich text content if used

### Acceptance Criteria
- Public APIs are safe
- Admin APIs cannot be accessed without auth
- Upload endpoints reject unsafe files

---

# 20. Swagger/OpenAPI Docs

## 20.1 API Documentation

### Task
Add drf-spectacular.

### URLs

```txt
/api/schema/
/api/docs/
```

### Acceptance Criteria
- Swagger docs open successfully
- Public and admin APIs are documented
- Request/response examples are added for important APIs

---

# 21. Testing

## 21.1 Unit and API Tests

### Required Tests
- Auth login success/failure
- Public plans list/detail
- Admin plan create/update/delete
- Legal document list
- Gallery list/filter
- Event list/detail
- Enquiry submit
- Admin enquiry update
- File upload validation
- Permission checks

### Acceptance Criteria
- Tests run successfully
- Critical APIs covered
- Permission tests included

---

# 22. Deployment Preparation

## 22.1 Production Checklist

### Task
Prepare backend for deployment.

### Checklist
- Gunicorn config
- Static files collection
- Media storage path
- PostgreSQL production config
- Allowed hosts
- CORS production URL
- Logging config
- Error handling
- Dockerfile optional
- Docker Compose optional

### Acceptance Criteria
- Backend can run in production mode
- Migrations can be applied safely
- Media files persist after deployment

---

# 23. Frontend Integration Contract

## 23.1 Confirm API Contract With Frontend

### Task
Provide final API contract to frontend.

### Required Public APIs

```txt
GET  /api/v1/website-settings/
GET  /api/v1/plans/
GET  /api/v1/plans/{slug}/
POST /api/v1/plans/calculate/
GET  /api/v1/legal-documents/
GET  /api/v1/gallery/categories/
GET  /api/v1/gallery/images/
GET  /api/v1/videos/
GET  /api/v1/events/
GET  /api/v1/events/{slug}/
POST /api/v1/enquiries/
POST /api/v1/auth/login/
GET  /api/v1/member/profile/
```

### Acceptance Criteria
- Frontend has stable API paths
- Response format is documented
- Error format is documented

---

# 24. Claude Execution Prompt

Use this prompt in Claude:

```txt
You are a senior Django backend architect and DRF engineer.

Build Phase 2 backend/admin system for a modern premium rebuild of aradhanabachat.com using Django DRF, PostgreSQL, and backend-managed storage.

Important:
- Do not copy any old website code.
- Build clean APIs for the new Next.js frontend.
- Use PostgreSQL as the database.
- Use backend media storage initially, but keep the design upgradeable to S3-compatible storage later.
- Create admin-manageable modules for plans, plan tables, legal documents, gallery, videos, events/news, enquiries, website settings, and members.
- Follow this markdown file task by task.
- Break implementation into small commits/tasks.
- For every task, explain files changed, models added, APIs added, migrations created, and how to test.
- Add proper validation, permissions, pagination, filtering, and Swagger documentation.
```

---

# 25. Definition of Done

Phase 2 is complete when:

- Django DRF backend is running
- PostgreSQL is configured
- Admin panel can manage website content
- Public APIs are ready for frontend
- JWT auth works
- Member profile API exists
- Plan calculator API exists
- Legal, gallery, video, event, enquiry APIs exist
- File upload/storage works from backend
- API docs are available
- Permissions and validations are implemented
- Tests cover critical APIs
- Backend is deployment ready
