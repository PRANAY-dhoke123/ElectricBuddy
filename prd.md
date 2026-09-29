PRD: Electricbuddy - Electricity Bill Tracker & Slab Calculator

Working name: Electricbuddy (change freely) Version: 1.0 | Type: Portfolio project (full-stack) | Target build time: 6 to 7 weeks Tagline: Know your units. Understand your bill.

1. Overview

Electricbuddy is a web app where a household enters the details of its monthly electricity bill and gets a clear breakdown: how many units fell into each tariff slab, what each slab cost, the estimated total, and how it compares with the actual bill. Users also see history, trends, charts, and a what-if calculator.

Version 1 uses manual input. Automatic bill reading (PDF/photo OCR) is a planned later upgrade that replaces only the data-entry step.

2. Problem Statement

Most people only see a final bill amount. They don't know:

Why the bill rose when usage rose only slightly (slab tariffs make extra units cost more).
Whether the amount charged matches what the tariff should produce.
How this month compares with earlier months.
What a given number of units would cost.
3. Goals and Non-Goals

Goals

Explain a bill through a slab-by-slab cost breakdown.
Keep a private, month-by-month history with charts and trends.
Let users estimate future bills with a what-if calculator.
Keep tariff data editable (stored as data, not hard-coded).
Ship a deployed, tested, documented portfolio project.

Non-Goals (Version 1)

OCR / automatic reading of bill images or PDFs.
Live smart-meter integration or device APIs.
Payments, bill reminders through SMS, or provider integrations.
Multi-household sharing or mobile apps.
Any AI features.

4. Users and Roles
Role	Description	Access
User	Household member tracking their bills	Own bills, own stats, read tariff plans, calculator
Admin (P1)	Maintains tariff plans	Create/edit tariff plans and slabs

In the MVP, tariff plans are loaded by a seed script; the admin role comes later.

5. User Stories
As a user, I can register and log in so my data stays private.
As a user, I can add a bill for a month by entering units (or previous and current meter readings).
As a user, I can see a slab-wise breakdown and the estimated total for each bill.
As a user, I can enter the actual amount charged and see the difference from the estimate.
As a user, I can view my bill history and edit or delete entries.
As a user, I can see charts of units and rupees per month.
As a user, I can try "what if I use X units?" without saving anything.
As a user, I can see trends: change from last month, highest, lowest, and average.

6. Functional Requirements

Priority: P0 = must have, P1 = should have, P2 = nice to have.

6.1 Authentication
ID	Requirement	Priority
A1	Register with name, email, password	P0
A2	Login with email and password; passwords hashed with bcrypt	P0
A3	JWT access token with expiry; protected endpoints	P0
A4	Every bill query is scoped to the logged-in user	P0
A5	Admin role for tariff management	P1
6.2 Tariff Plans
ID	Requirement	Priority
T1	Store tariff plans with slabs (from unit, to unit, rate per unit)	P0
T2	Seed one real plan through a script; record its source and date	P0
T3	Plan settings: fixed charge and tax percent	P1
T4	Admin can create and edit plans and slabs	P1
T5	Slab validation: no gaps, no overlaps, last slab open-ended	P1
6.3 Bills
ID	Requirement	Priority
B1	Add a bill: month, units, plan, optional actual amount	P0
B2	Alternative input: previous and current meter reading; units are calculated	P1
B3	Calculate and store slab breakdown and estimated amount on save	P0
B4	List, edit, and delete own bills; recalculate estimate on edit	P0
B5	One bill per user per month	P0
B6	Bill check: show actual minus estimated, flag large differences	P1
6.4 Analytics
ID	Requirement	Priority
S1	Charts: units per month and rupees per month	P1
S2	Summary: average, highest, lowest, latest change from previous month (units and %)	P1
S3	What-if calculator: units and plan in, breakdown out, nothing saved	P1
S4	Next-month projection from recent months	P2
S5	Budget alert when the estimate crosses a user-set limit	P2
S6	CSV export of bill history	P2
7. Business Rules and Calculations

Slab calculation. For each slab, units charged = the number of units that fall inside that slab's range; slab cost = units charged x rate. The energy charge is the sum of all slab costs.

Illustrative example (made-up rates):

Slab	Units	Rate
1	0 to 100	4
2	101 to 200	6
3	Above 200	8

For 250 units: 100 x 4 + 100 x 6 + 50 x 8 = 1,400.

Estimated total = (energy charge + fixed charge) + tax, where tax = tax percent x (energy charge + fixed charge). Assumption: the real tax and surcharge rules differ by provider; document the exact rule used for the seeded plan in the README.

Other rules

Units must be zero or more; meter readings must satisfy current >= previous.
Month format is YYYY-MM; one bill per user per month.
All money values use decimal types, not floats; round to 2 decimals (half up).
Bill check: difference = actual - estimated; flag when the absolute difference exceeds 5% of the estimate (configurable).
Projection (P2): average units of the last 3 bills run through the same slab calculation.
A bill keeps the plan it was calculated with; editing a plan later must not silently change past estimates (store the estimated amount and breakdown on the bill).
8. Data Model
Table	Key columns
users	id, name, email (unique), password_hash, role, created_at
tariff_plans	id, name, provider, fixed_charge, tax_percent, source_note, effective_from, is_active
tariff_slabs	id, plan_id (FK), from_unit, to_unit (null for last slab), rate_per_unit
bills	id, user_id (FK), plan_id (FK), month (YYYY-MM), units, previous_reading, current_reading, actual_amount, estimated_amount, breakdown (JSON), created_at, updated_at

Constraints: unique (user_id, month) on bills; unique (plan_id, from_unit) on slabs; check units >= 0; foreign keys on all relations.

9. API Endpoints
Area	Endpoint	Purpose
Auth	POST /auth/register, POST /auth/login, GET /auth/me	Account and token
Tariffs	GET /tariffs, GET /tariffs/{id}	Plans with slabs
Tariffs (P1 admin)	POST /tariffs, PUT /tariffs/{id}	Manage plans
Bills	POST /bills, GET /bills, GET /bills/{id}, PUT /bills/{id}, DELETE /bills/{id}	Bill CRUD
Calculator	POST /calculate	What-if breakdown, not saved
Stats	GET /stats/summary, GET /stats/monthly	Trends and chart data

Response conventions: 200 read/update, 201 created, 204 deleted, 401 not authenticated, 403 not allowed, 404 not found in the caller's scope, 409 duplicate month, 422 validation error.

10. UI Pages (Bootstrap + JavaScript)
Page	Contents
login.html / register.html	Forms and error messages
dashboard.html	Summary cards, units and rupees charts, latest bill
add-bill.html	Month, units or readings, plan, actual amount; live estimate preview
bills.html	History table with edit and delete
bill-detail.html	Slab breakdown table, estimate vs actual
calculator.html	What-if calculator
tariffs.html	Tariff chart for the selected plan

Every data page needs loading, empty, and error states.

11. Non-Functional Requirements
Security: bcrypt hashing, JWT expiry, server-side ownership checks, Pydantic validation, secrets in .env (commit only .env.example), safe error messages.
Accuracy: decimal arithmetic for all money values.
Usability: responsive layout; clear validation messages next to fields.
Maintainability: business logic in service files, routers kept thin.
Data integrity: database constraints back up validation rules.
12. Tech Stack
Layer	Choice
Backend	FastAPI, SQLAlchemy, Pydantic
Database	SQLite for development, PostgreSQL for deployment
Auth	JWT + bcrypt
Frontend	HTML, CSS, Bootstrap 5, JavaScript (fetch), Chart.js; served by FastAPI
Testing	Pytest + FastAPI TestClient
Deployment	Render

13. Project Structure
Electricbuddy/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   ├── dependencies.py
│   ├── models/        # user, tariff_plan, tariff_slab, bill
│   ├── schemas/
│   ├── services/      # tariff_service.py, stats_service.py
│   └── routers/       # auth, tariffs, bills, calculator, stats
├── scripts/
│   └── seed_tariffs.py
├── static/            # html, css, js (api.js, auth.js, one file per page)
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_tariff_service.py
│   ├── test_bills.py
│   └── test_authorization.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
14. Testing Strategy
Group	Examples
Slab calculation	0 units; exactly at a slab limit; one unit above a limit; above the last slab; decimal units
Bills	Duplicate month returns 409; negative units rejected; reading order validated; edit recalculates estimate
Authorization	User A cannot read, edit, or delete User B's bill
Auth	Wrong password; expired token; missing token
Stats	Month-over-month change; highest/lowest; empty history
15. Milestones
Week	Deliverable	Done when
1	Setup, models, register/login	Login works in /docs
2	Tariff seed, calculation service, tests	Slab tests pass
3	Bills CRUD with ownership scoping; basic deployment	Live API, users isolated
4	Stats and calculator endpoints; frontend login and add-bill	Add a bill from the browser
5	History table, charts, breakdown view	Dashboard shows real data
6	Bill check, trends, validation polish	Clear errors on bad input
7	Final tests, deployment, README, demo data	Live link and complete README

16. Definition of Done
All P0 and core P1 requirements work end to end.
Live deployment with a demo account and sample data.
Slab calculation and authorization covered by automated tests.
README includes problem statement, features, tariff source and date, setup steps, API notes, and screenshots.
No secrets committed to Git.
The project can be explained in two minutes.
17. Risks and Mitigations
Risk	Mitigation
Tariff rules differ from the real bill	Document the source and the formula; store fixed charge and tax as plan settings
Frontend learning slows progress	Finish the API first; keep the UI simple with Bootstrap
Scope creep	Freeze P0 and P1 first; P2 and OCR only after deployment
Rounding errors in money	Use decimal types and test the rounding rule
Deployment problems late	Deploy a basic API in week 3
18. Open Decisions
Which provider's tariff will be seeded for the demo?
Are fixed charge and tax part of version 1, or slab charges only?
Final application name.

19. Future Enhancements
PDF bill upload with text extraction, then photo upload with OCR and a confirm-and-correct screen.
Simulated or real smart-meter readings sent to the API.
Monthly PDF report, CSV export, and budget alerts.
Multiple homes per user and shared household access.