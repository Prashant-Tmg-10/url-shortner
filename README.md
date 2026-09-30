URL Shortener API

A backend service that converts long URLs into short, unique codes and redirects visitors back to the original link — built to practice authentication, ownership validation, unique ID generation, and production-style API design.

Features
User authentication — registration with hashed passwords (bcrypt), JWT-based login
Create short URLs — authenticated users submit a long URL and receive a short code
Redirect — visiting a short URL redirects (302) to the original, tracking click count and last-accessed time
View my URLs — authenticated users see only the links they created (ownership-enforced)
Tech Stack
Framework: FastAPI
Database: PostgreSQL
ORM: SQLAlchemy
Auth: JWT (python-jose), bcrypt password hashing (pwdlib)
Testing: pytest
Project Structure
src/
├── url/          # URL feature: models, dtos, controller, router
├── user/         # Auth feature: models, dtos, controller, router
├── utils/        # Shared: db connection, settings, helpers (base62), auth dependency
└── main.py       # App entrypoint
tests/            # pytest test suite
Key Design Decisions
Short codes use a counter + base62 encoding, not hashing. Hashing is deterministic — the same URL always produces the same hash, making it impossible to guarantee unique codes across different users. Using the database's auto-incrementing id, converted to base62, guarantees uniqueness with zero collision risk.
Redirects use HTTP 302, not 301. A 301 (permanent) redirect gets cached by browsers, meaning repeat visits could skip the server entirely — silently undercounting clicks. 302 ensures every visit is tracked accurately.
Ownership is enforced at the query level, not just hidden in the UI — every "my links" request filters by the authenticated user's ID, preventing one user from viewing another's data (IDOR prevention).
Login uses email only (not username) — a deliberate simplicity choice for this project's scope; username remains a display-only field.
Login errors are intentionally generic ("Invalid credentials") whether the email doesn't exist or the password is wrong — this prevents user enumeration attacks.
Setup
Clone the repo and create a virtual environment:
   python -m venv env
   env\Scripts\Activate.ps1   # Windows PowerShell
Install dependencies:
   pip install -r requirements.txt
Create a .env file in the project root:
   DB_connection=postgresql://<user>:<password>@localhost:5432/<dbname>
   SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
   ALGORITHM=HS256
   EXP_TIME=30
Run the server:
   uvicorn src.main:app --reload
API docs available at http://localhost:8000/docs
Running Tests
pytest -v
API Endpoints
Method	Path	Auth required	Description
POST	/user/register	No	Register a new user
POST	/user/login	No	Log in, receive a JWT
POST	/url/create	Yes	Create a new short URL
GET	/url/	Yes	View your own short URLs
GET	/url/{short_code}	No	Redirect to the original URL
Roadmap
 Redis caching for redirect lookups
 Rate limiting
 Dockerfile
 Deployment