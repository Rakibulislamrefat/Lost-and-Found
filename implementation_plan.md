# Lost & Found Portal — Full-Stack Implementation Plan (Django)

A campus/community web application where users can report lost items, post found items, search listings, and submit claim requests. Built with Django, SQLite, and vanilla HTML/CSS/JS.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.x (Python) |
| Database | SQLite (default, dev-friendly) |
| Frontend | Django Templates + Vanilla CSS + JS |
| Auth | Django built-in `auth` system |
| Media/Static | Django `MEDIA_ROOT` for uploaded images |
| Admin | Django Admin Panel |

---

## Project Structure

```
lost_and_found_portal/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── media/                    # Uploaded item images
│   └── items/
├── static/                   # CSS, JS, images
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── portal/                   # Main Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── items/                    # Core app — items & claims
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templatetags/
│       └── custom_filters.py
├── accounts/                 # Auth app — login, register
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
└── templates/                # All HTML templates
    ├── base.html
    ├── home.html
    ├── accounts/
    │   ├── login.html
    │   ├── register.html
    │   └── profile.html
    └── items/
        ├── item_list.html
        ├── item_detail.html
        ├── item_form.html
        ├── my_items.html
        ├── claim_list.html
        └── search_results.html
```

---

## Database Models

### `items/models.py`

#### Model: `Item`
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField (PK) | Auto-generated |
| `user` | ForeignKey → User | Who posted the item |
| `title` | CharField(200) | Item name |
| `description` | TextField | Detailed description |
| `category` | CharField (choices) | Electronics, Documents, Clothing, Accessories, Others |
| `item_type` | CharField (choices) | **"lost"** or **"found"** |
| `location` | CharField(200) | Where it was lost/found |
| `date_reported` | DateField | When it was lost/found |
| `image` | ImageField (optional) | Photo of the item |
| `status` | CharField (choices) | **Active**, **Claimed**, **Closed** |
| `created_at` | DateTimeField (auto) | Post creation timestamp |

#### Model: `ClaimRequest`
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField (PK) | Auto-generated |
| `item` | ForeignKey → Item | Which item is being claimed |
| `claimant` | ForeignKey → User | Who is claiming |
| `message` | TextField | Proof/description of ownership |
| `status` | CharField (choices) | **Pending**, **Approved**, **Rejected** |
| `created_at` | DateTimeField (auto) | Claim timestamp |

---

## User Roles & Permissions

| Role | Capabilities |
|------|-------------|
| **Anonymous** | View item listings, search |
| **Registered User** | Post lost/found items, submit claim requests, manage own items, approve/reject claims on own items |
| **Admin (superuser)** | Full access via Django Admin panel — manage all items, users, claims |

---

## App: `accounts` — Authentication

### Views
| View | URL | Method | Description |
|------|-----|--------|-------------|
| `register` | `/accounts/register/` | GET/POST | User registration form |
| `login` | `/accounts/login/` | GET/POST | Login form |
| `logout` | `/accounts/logout/` | POST | Logout user |
| `profile` | `/accounts/profile/` | GET | User profile page |

### Forms
- `RegisterForm` — extends Django's `UserCreationForm` with email field

---

## App: `items` — Core Features

### Views
| View | URL | Method | Description |
|------|-----|--------|-------------|
| `home` | `/` | GET | Landing page with recent items |
| `item_list` | `/items/` | GET | All items (paginated, filterable) |
| `item_detail` | `/items/<id>/` | GET | Single item with claim button |
| `item_create` | `/items/new/` | GET/POST | Post a new lost/found item |
| `item_edit` | `/items/<id>/edit/` | GET/POST | Edit own item |
| `item_delete` | `/items/<id>/delete/` | POST | Delete own item |
| `my_items` | `/items/my/` | GET | Dashboard of user's own items |
| `search` | `/items/search/` | GET | Search by keyword, category, type |
| `submit_claim` | `/items/<id>/claim/` | GET/POST | Submit a claim request |
| `manage_claims` | `/items/<id>/claims/` | GET | View claims on own item |
| `update_claim` | `/claims/<id>/update/` | POST | Approve/reject a claim |

---

## Page-by-Page UI Plan

### 1. **Home Page** (`/`)
- Hero section with title & search bar
- Quick filter buttons (Lost / Found)
- Grid of recent items (6–8 cards)
- "Post an Item" call-to-action button

### 2. **Item Listing** (`/items/`)
- Sidebar filters: Category, Type (Lost/Found), Date
- Item cards in a responsive grid (image, title, type badge, location, date)
- Pagination

### 3. **Item Detail** (`/items/<id>/`)
- Large image, title, description, category, location, date
- Status badge (Active / Claimed / Closed)
- "Claim This Item" button (for logged-in users, not item owner)
- Owner info (username)

### 4. **Post Item Form** (`/items/new/`)
- Fields: Title, Description, Category (dropdown), Type (Lost/Found radio), Location, Date, Image upload
- Form validation with error messages

### 5. **My Items Dashboard** (`/items/my/`)
- Table/cards showing user's posted items
- Status indicators
- Edit / Delete / View Claims buttons per item

### 6. **Login / Register Pages**
- Clean, centered form cards
- Social-style design with logo

---

## Proposed Changes

### Django Project Setup

#### [NEW] [requirements.txt](file:///C:/Users/ASUS/.gemini/antigravity/scratch/lost_and_found_portal/requirements.txt)
- `django>=5.0`, `Pillow` (for ImageField)

---

### Portal Config

#### [NEW] [settings.py](file:///C:/Users/ASUS/.gemini/antigravity/scratch/lost_and_found_portal/portal/settings.py)
- Configure `INSTALLED_APPS` with `items`, `accounts`
- Set `MEDIA_URL`, `MEDIA_ROOT`, `STATIC_URL`, `STATICFILES_DIRS`
- Set `LOGIN_URL`, `LOGIN_REDIRECT_URL`
- Template dirs pointing to project-level `templates/`

#### [NEW] [urls.py](file:///C:/Users/ASUS/.gemini/antigravity/scratch/lost_and_found_portal/portal/urls.py)
- Include `items.urls`, `accounts.urls`
- Serve media files in debug mode

---

### Accounts App

#### [NEW] `accounts/` app
- `forms.py` — `RegisterForm` extending `UserCreationForm`
- `views.py` — `register`, `login_view`, `logout_view`, `profile`
- `urls.py` — URL patterns for auth

---

### Items App

#### [NEW] `items/` app
- `models.py` — `Item` and `ClaimRequest` models
- `forms.py` — `ItemForm`, `ClaimForm`
- `views.py` — All views listed above
- `urls.py` — URL patterns
- `admin.py` — Register models with custom admin display

---

### Templates

#### [NEW] `templates/` directory
- `base.html` — Navbar, footer, block content
- `home.html` — Landing page
- `items/*.html` — All item-related pages
- `accounts/*.html` — Auth pages

---

### Static Assets

#### [NEW] `static/css/style.css`
- Modern dark-themed design with gradients, glassmorphism cards, smooth animations
- Responsive grid layout
- Premium typography (Google Fonts — Inter)

#### [NEW] `static/js/main.js`
- Image preview on upload, filter toggle, minor UI interactions

---

## Verification Plan

### Automated Tests
1. **Run Django's built-in check:**
   ```
   python manage.py check
   ```
2. **Run migrations successfully:**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Create superuser and verify admin panel:**
   ```
   python manage.py createsuperuser
   ```

### Browser Verification
1. **Start dev server:** `python manage.py runserver`
2. Open `http://127.0.0.1:8000/` — verify home page renders
3. Register a new user → verify redirect to login
4. Login → verify dashboard access
5. Post a new "Lost" item with image → verify it appears in listing
6. Post a "Found" item → verify it appears with correct badge
7. Search for an item by keyword → verify results
8. Click an item → verify detail page
9. Submit a claim on another user's item → verify claim appears
10. Go to "My Items" → verify claims are visible, approve/reject works
11. Visit `/admin/` → verify all models are manageable
