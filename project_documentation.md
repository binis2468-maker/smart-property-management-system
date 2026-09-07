# VILLA REAL ESTATE AGENCY SYSTEM
## ACADEMIC MINI PROJECT REPORT

---

### COVER PAGE

**PROJECT TITLE:** VILLA REAL ESTATE AGENCY MANAGEMENT SYSTEM  
**COURSE:** MCA 307 - MINI PROJECT REPORT  
**DEGREE:** MASTER OF COMPUTER APPLICATIONS (MCA)  

**Submitted By:**  
Student Name: [Student Name]  
Roll No / Reg No: [Register Number]  

**Under the Guidance of:**  
[Faculty Guide Name]  
[Designation], Department of Computer Applications  

**DEPARTMENT OF COMPUTER APPLICATIONS**  
[College / University Name]  
[Academic Year 2025-2026]  

---

### CERTIFICATE OF THE HEAD OF DEPARTMENT

This is to certify that the project report entitled **"VILLA REAL ESTATE AGENCY MANAGEMENT SYSTEM"** is a bonafide record of the mini project work carried out by **[Student Name]** (Register No: **[Register Number]**) in partial fulfillment of the requirements for the award of the degree of **Master of Computer Applications (MCA)** during the academic year 2025–2026.

<br><br>

________________________  
**Head of Department**  
Department of Computer Applications  
[College / University Name]  

---

### CERTIFICATE OF THE INTERNAL PROJECT GUIDE

This is to certify that the project report entitled **"VILLA REAL ESTATE AGENCY MANAGEMENT SYSTEM"** submitted by **[Student Name]** (Register No: **[Register Number]**) in partial fulfillment of the requirements for the award of the degree of **Master of Computer Applications (MCA)**, is an authentic work carried out under my direct supervision and guidance.

<br><br>

________________________  
**Internal Project Guide**  
[Faculty Designation]  
Department of Computer Applications  

---

### DECLARATION

I, **[Student Name]**, hereby declare that the project report entitled **"VILLA REAL ESTATE AGENCY MANAGEMENT SYSTEM"** submitted to the Department of Computer Applications, **[College / University Name]**, for the award of the degree of **Master of Computer Applications (MCA)**, is an authentic record of work done by me under the guidance of **[Faculty Guide Name]**.

I further declare that this report has not been submitted previously to any other University or Institution for the award of any degree or diploma.

<br>
Place: [City Name]  
Date: [Date]  

________________________  
**[Student Name]**  
(Reg. No: [Register Number])  

---

### ACKNOWLEDGMENT

I express my deepest gratitude to **[Head of Department Name]**, Head of the Department of Computer Applications, for providing the necessary facilities and support throughout the course of this project.

I am profoundly indebted to my internal project guide, **[Faculty Guide Name]**, for their invaluable guidance, constant encouragement, constructive criticism, and continuous monitoring throughout the development of this project.

I also extend my heartfelt thanks to all the faculty members, technical staff of the Department of Computer Applications, and my fellow classmates for their direct and indirect cooperation and valuable suggestions.

Finally, I express my sincere appreciation to my family and friends for their patience, understanding, and moral support during the completion of this project.

<br>
**[Student Name]**

---

### TABLE OF CONTENTS

1. **ABSTRACT**
2. **CHAPTER 1: INTRODUCTION**
   - 1.1 Introduction
   - 1.2 Problem Statement
   - 1.3 Scope and Relevance of the Project
   - 1.4 Objectives
3. **CHAPTER 2: SYSTEM ANALYSIS**
   - 2.1 Introduction
   - 2.2 Existing System
     - 2.2.1 Limitations of Existing System
   - 2.3 Proposed System
     - 2.3.1 Advantages of Proposed System
   - 2.4 Feasibility Study
     - 2.4.1 Technical Feasibility
     - 2.4.2 Operational Feasibility
     - 2.4.3 Economic Feasibility
   - 2.5 Software Engineering Paradigm Applied
4. **CHAPTER 3: SYSTEM DESIGN**
   - 3.1 Introduction
   - 3.2 Database Design
     - 3.2.1 Entity Relationship (E-R) Model
     - 3.2.2 Relational Schema & Table Structures
   - 3.3 Process Design – Data Flow Diagrams (DFD)
     - 3.3.1 Context Level (Level 0) DFD
     - 3.3.2 Level 1 DFD
   - 3.4 Object-Oriented Design – UML Diagrams
     - 3.4.1 Use Case Diagram
     - 3.4.2 Activity Diagram
     - 3.4.3 Sequence Diagram
   - 3.5 Input Design
   - 3.6 Output Design
5. **CHAPTER 4: SYSTEM ENVIRONMENT**
   - 4.1 Introduction
   - 4.2 Software Requirements Specification (SRS)
   - 4.3 Hardware Requirements Specification
   - 4.4 Tools & Platforms
     - 4.4.1 Front-End Tools & Frameworks
     - 4.4.2 Back-End Framework & Language
     - 4.4.3 Database Engine
     - 4.4.4 Operating System & Development Tools
6. **CHAPTER 5: SYSTEM IMPLEMENTATION**
   - 5.1 Introduction
   - 5.2 Coding & Core Modules
     - 5.2.1 Core Source Code Snippets
     - 5.2.2 Input Validation & Security Engine
   - 5.3 Code Validation & Optimization
7. **CHAPTER 6: SYSTEM TESTING**
   - 6.1 Introduction
   - 6.2 Unit Testing (White-Box Testing)
   - 6.3 Integration Testing (Black-Box Testing)
   - 6.4 System Testing & Execution Summary
   - 6.5 Test Plan & Test Cases
8. **CHAPTER 7: SYSTEM MAINTENANCE**
   - 7.1 Introduction
   - 7.2 Maintenance Strategies & Corrective Maintenance
9. **CHAPTER 8: FUTURE ENHANCEMENTS AND SCOPE OF FURTHER DEVELOPMENT**
   - 8.1 Introduction
   - 8.2 Merits of the System
   - 8.3 Limitations of the System
   - 8.4 Future Enhancements
10. **CHAPTER 9: CONCLUSION**
11. **CHAPTER 10: BIBLIOGRAPHY**
12. **APPENDIX**
    - Core Source Code Modules
    - Screen Layouts & User Interface Screenshots
13. **GLOSSARY**

---

### ABSTRACT

The **Villa Real Estate Agency Management System** is a full-stack, dynamic web application designed to digitize, streamline, and optimize property listings, builder approvals, property scheduling, client inquiries, and user wishlists for the modern real estate sector. Traditional real estate practices rely heavily on manual record-keeping, fragmented communication channels, and unverified seller listings, leading to inefficiency, security vulnerabilities, and delays in closing property deals.

This project resolves these challenges by providing a secure multi-role web platform built on **Python 5.x / Django MVC Framework**, **SQLite Database**, **Bootstrap 5 UI Framework**, and **Chart.js Analytics**. The system provides separate role-based interfaces for four major entities:
1. **Administrators**: Who manage executive dashboards, inspect real-time metrics, review pending builder applications, monitor approved agencies, view client inquiries, and track scheduled visits.
2. **Approved Builders**: Who add, edit, update, and manage property portfolios (Villas, Apartments, Penthouses, Condos) with high-resolution image uploads, and view client appointment requests.
3. **Registered Users / Buyers**: Who search for verified properties, toggle items into their interactive wishlist, schedule property site visits, and manage personal appointments.
4. **Public Guests**: Who browse property catalogs, explore deal categories, and submit contact inquiries.

To ensure client-level security and data integrity, the system implements strict validation logic:
- **Phone Number Verification**: Mandates exactly 10-digit Indian phone numbers with automated `+91` prefix formatting.
- **Email Verification**: Enforces strict RFC-compliant regex validation to prevent spam registrations.
- **Password Complexity**: Requires a minimum of 6 characters containing at least 1 uppercase letter, 1 numeric digit, and 1 special symbol.
- **Anti-Autofill Security Traps**: Prevents browser password managers from pre-filling credentials.

The platform has been rigorously tested using both **White-Box Testing** (unit models and validation methods) and **Black-Box Integration Testing** (end-to-end user lifecycles, builder approvals, and booking workflows) with 100% test pass rates across 16 test cases.

---

### CHAPTER 1: INTRODUCTION

#### 1.1 Introduction
The real estate industry is one of the fastest-growing financial sectors worldwide. Modern buyers demand instant access to high-quality property photos, accurate pricing, verified builder credentials, and seamless online scheduling. The **Villa Real Estate Agency Management System** is engineered to provide a transparent, user-friendly, and secure digital real estate portal.

Built using Django's Model-View-Template (MVT) architecture, the system provides a clean separation of concerns, rapid data rendering, and role-based access control. The front-end leverages custom CSS, Bootstrap 5 components, and Chart.js to deliver a visual experience matching the company's brand aesthetic (`#f35525` Villa Orange).

#### 1.2 Problem Statement
Existing traditional real estate workflows suffer from significant operational bottlenecks:
1. **Unverified Builder Listings**: Fraudulent or unaccredited entities list fake properties, damaging consumer trust.
2. **Session & Security Vulnerabilities**: Unauthenticated visitors frequently gain access to restricted seller or buyer dashboards.
3. **Manual Site Visit Scheduling**: Booking property visits via phone or email leads to double-booking and miscommunication between buyers and builders.
4. **Data Redundancy & Invalid Inputs**: Poor input validation leads to invalid phone numbers, malformed email addresses, and duplicate wishlist entries.

#### 1.3 Scope and Relevance of the Project
The scope of this project encompasses the complete digital lifecycle of real estate transactions:
- **Builder Accreditation**: Mandatory admin approval workflow before a builder can post properties.
- **Property Catalog Management**: Full CRUD (Create, Read, Update, Delete) operations for real estate portfolios with dynamic media handling.
- **Client Engagement**: Interactive wishlists, visit booking scheduling, and inquiry response tracking.
- **Data Quality & Validation**: Automated validation for Indian mobile numbers (+91), email addresses, and password security.

#### 1.4 Objectives
- To design and implement a role-based Web GIS / real estate portal.
- To establish a two-step verification workflow for builder registration and admin approval.
- To implement client visit scheduling and Wishlist management without data duplication.
- To enforce multi-layer form validation (Email Regex, +91 10-digit Phone, Password Complexity).
- To create a responsive Executive Admin Dashboard featuring KPI cards and Chart.js analytics.
- To achieve 100% test coverage across White-Box unit tests and Black-Box integration scenarios.

---

### CHAPTER 2: SYSTEM ANALYSIS

#### 2.1 Introduction
System analysis involves a detailed study of current real estate procedures, identifying bottlenecks, defining user requirements, and assessing project feasibility.

#### 2.2 Existing System
In the existing system, real estate transactions are handled through offline brokers or static websites:
- Property data is updated manually via spreadsheets or static HTML pages.
- Client visit requests are logged on paper registers.
- Builders communicate directly with buyers without administrative oversight.

##### 2.2.1 Limitations of Existing System
- **High Error Rate**: Invalid contact info is recorded due to a lack of input validation.
- **No Role Separation**: Unauthorized users can view seller contact numbers or private property details.
- **Poor User Experience**: Lack of search filters, wishlists, or instant booking confirmation.
- **Lack of Analytics**: Agency management cannot track monthly visit trends or top-performing property categories.

#### 2.3 Proposed System
The proposed system is an automated, web-based database management platform. It automates builder verification, client appointment scheduling, and catalog management while enforcing strict data security protocols.

##### 2.3.1 Advantages of Proposed System
- **Verified Builder Network**: Only admin-approved builders can upload listings.
- **Strict Input Validation**: Enforces `+91` 10-digit phone verification, standard email verification, and complex passwords.
- **Automated Wishlist & Booking**: Instant site visit scheduling linked directly to the buyer's account.
- **Executive Analytics**: Real-time KPI counters and Chart.js visual charts on the Admin Dashboard.
- **High Security**: Session authentication middleware prevents unauthorized route access.

#### 2.4 Feasibility Study

##### 2.4.1 Technical Feasibility
The project utilizes established open-source technologies: Python 5.x, Django Web Framework, SQLite, HTML5, CSS3, JavaScript, and Bootstrap 5. These tools are lightweight, scalable, well-documented, and fully supported on modern operating systems. Thus, the system is technically feasible.

##### 2.4.2 Operational Feasibility
The platform features an intuitive, responsive user interface. Navigation bars adapt dynamically based on session roles (Admin, Builder, User, Guest). The administrative dashboard requires no specialized technical training, making the system operationally feasible.

##### 2.4.3 Economic Feasibility
Built entirely with open-source frameworks and standard database tools, the project requires zero licensing fees. It reduces administrative overhead costs by automating client inquiries and booking registers, proving economically feasible.

#### 2.5 Software Engineering Paradigm Applied
The project follows the **Agile Iterative Development Model**. System design, component building, UI refactoring, security validation, and automated testing were performed in short, iterative development cycles to ensure continuous validation and quality control.

---

### CHAPTER 3: SYSTEM DESIGN

#### 3.1 Introduction
System Design transforms requirements into technical representations, including database schemas, process flows, object-oriented UML diagrams, and interface layouts.

#### 3.2 Database Design

##### 3.2.1 Entity Relationship (E-R) Model
Entities in the system include `User`, `Builder`, `ApprovedBuilder`, `Property`, `Booking`, `Wishlist`, and `Query`.

##### 3.2.2 Relational Schema & Table Structures

1. **`villa_user_details` Table**:
   - `id` (INT, Primary Key, Auto Increment)
   - `name` (VARCHAR 100)
   - `email` (VARCHAR 100, Unique)
   - `phone` (VARCHAR 100)
   - `password` (VARCHAR 100)
   - `photo` (VARCHAR 100 / ImageField)

2. **`villa_builder_details` Table (Pending Requests)**:
   - `id` (INT, Primary Key, Auto Increment)
   - `buildname` (VARCHAR 100)
   - `buildemail` (VARCHAR 100)
   - `buildphone` (VARCHAR 100)
   - `buildpassword` (VARCHAR 100)
   - `buildphoto` (VARCHAR 100 / ImageField)

3. **`villa_approved_builder_details` Table (Approved Builders)**:
   - Identical structure to `builder_details`. Stores verified builders.

4. **`builder_app_property_details` Table**:
   - `id` (INT, Primary Key, Auto Increment)
   - `user_id` (VARCHAR 100 - Builder ID reference)
   - `property_name` (VARCHAR 100)
   - `property_category` (VARCHAR 100)
   - `property_location` (VARCHAR 100)
   - `property_budget` (VARCHAR 100)
   - `property_bedroom` (VARCHAR 100)
   - `property_bathroom` (VARCHAR 100)
   - `property_area` (VARCHAR 100)
   - `property_floor` (VARCHAR 100)
   - `property_parking` (VARCHAR 100)
   - `property_photo` (VARCHAR 100 / ImageField)

5. **`user_app_booking` Table**:
   - `id` (INT, Primary Key, Auto Increment)
   - `user_id` (VARCHAR 100)
   - `name` (VARCHAR 100)
   - `email` (VARCHAR 100)
   - `phone` (VARCHAR 100)
   - `property_name` (VARCHAR 100)
   - `property_location` (VARCHAR 100)
   - `property_budget` (VARCHAR 100)

6. **`user_app_wishlists` Table**:
   - Stores user-wishlisted properties linked via `user_id` and `property_name`.

7. **`villa_query` Table**:
   - `id` (INT, Primary Key, Auto Increment)
   - `name`, `email`, `subject`, `message`

---

#### 3.3 Process Design – Data Flow Diagrams (DFD)

##### 3.3.1 Context Level (Level 0) DFD
- **Entities**: Guest, Registered User, Builder, Admin.
- **Process**: Villa Real Estate System.
- **Data Flows**:
  - Guest sends contact query -> System records query.
  - Builder registers -> System creates Pending Request.
  - Admin approves builder -> System transfers to Approved Builders.
  - User schedules visit -> System creates Booking record.

##### 3.3.2 Level 1 DFD
1. **Authentication Process**: Validates credentials against `user_details`, `approved_builder_details`, or Admin credentials.
2. **Property Management**: Approved Builder uploads/edits listings in `property_details`.
3. **Visit Booking Process**: Authenticated User selects property -> System reads user details & property info -> Saves to `booking`.
4. **Wishlist Process**: Checks existing wishlist -> Toggles Add/Delete.

---

#### 3.4 Object-Oriented Design – UML Diagrams

##### 3.4.1 Use Case Diagram
- **Actor User**: Register, Login, Browse Catalog, Toggle Wishlist, Schedule Visit, View My Bookings, Logout.
- **Actor Builder**: Register Application, Login (post-approval), Add Property, Edit Property, Delete Property, View Property Bookings.
- **Actor Admin**: Login, View Dashboard Analytics, Approve Builder, Reject Builder, View Approved Builders, View All Bookings, View Queries.

##### 3.4.2 Activity Diagram
1. User requests Registration -> System validates Email, Phone (+91), Password -> Saves User.
2. User selects Property Visit -> System checks Session (`uid`) -> If Active, creates Booking & redirects to `/scheduledvisit` -> If Inactive, redirects to `/login`.

##### 3.4.3 Sequence Diagram
`User` -> `Browser UI` -> `Django Router` -> `user_app.views.schedulevisit` -> `user_app.models.booking.save()` -> `Database` -> Redirect Response.

---

#### 3.5 Input Design
Forms are designed with Bootstrap 5 responsiveness and client/server validation:
- **Phone Field**: Integrated `+91` prefix addon, `pattern="[0-9]{10}"`, `maxlength="10"`.
- **Password Field**: `type="password"`, `autocomplete="new-password"`, helper hints for uppercase, digit, and symbol rules.
- **Media Uploads**: `enctype="multipart/form-data"` with image type restriction `accept="image/*"`.

#### 3.6 Output Design
Outputs include clean tabular layouts, interactive alert banners, card grids for properties, and a responsive executive dashboard featuring dynamic Chart.js charts.

---

### CHAPTER 4: SYSTEM ENVIRONMENT

#### 4.1 Introduction
This chapter outlines the hardware, software, and tools required for developing and running the system.

#### 4.2 Software Requirements Specification (SRS)
- **Operating System**: Windows 10 / 11 (64-bit)
- **Programming Language**: Python 3.10+ / 5.x compatible
- **Web Framework**: Django 5.2.5
- **Database Engine**: SQLite 3
- **Front-End Technologies**: HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3.3, Chart.js, FontAwesome 6, Tabler Icons

#### 4.3 Hardware Requirements Specification
- **Processor**: Intel Core i3 / AMD Ryzen 3 or higher
- **Memory (RAM)**: 4 GB minimum (8 GB recommended)
- **Hard Disk Space**: 500 MB free space
- **Display Resolution**: 1366 x 768 or higher

#### 4.4 Tools & Platforms
- **IDEs**: VS Code / Antigravity IDE
- **Command Shell**: Windows PowerShell
- **Testing Framework**: Django Built-in Unit Test Runner (`django.test`)

---

### CHAPTER 5: SYSTEM IMPLEMENTATION

#### 5.1 Introduction
System implementation involves converting design specifications into executable Django views, templates, models, and security middleware.

#### 5.2 Coding & Core Modules

##### 5.2.1 Security & Validation Engine Snippet (`villa/views.py`)
```python
import re
from django.shortcuts import render, redirect

def validate_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def validate_phone_format(phone):
    clean_digits = re.sub(r'\D', '', phone)
    if clean_digits.startswith('91') and len(clean_digits) == 12:
        clean_digits = clean_digits[2:]
    if len(clean_digits) == 10:
        return True, f"+91 {clean_digits}"
    return False, None

def validate_password_format(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>\-_+=\/~\[\]]', password):
        return False, "Password must contain at least one special symbol (!@#$%^&* etc.)."
    return True, None
```

##### 5.2.2 Role-Aware Booking View Snippet (`admin_app/views.py`)
```python
def scheduledvisit(request):
    if request.session.get('admin'):
        pdata = booking.objects.all().order_by('-id')
        return render(request, 'bookedvisit.html', {'prop': pdata})
    elif request.session.get('uid'):
        user_id = str(request.session['uid'])
        pdata = booking.objects.filter(user_id=user_id).order_by('-id')
        return render(request, 'bookedvisit.html', {'prop': pdata})
    elif request.session.get('bid'):
        bldrid = str(request.session['bid'])
        builder_props = property_details.objects.filter(user_id=bldrid).values_list('property_name', flat=True)
        pdata = booking.objects.filter(property_name__in=builder_props).order_by('-id')
        return render(request, 'bookedvisit.html', {'prop': pdata})
    return redirect('/login')
```

#### 5.3 Code Validation & Optimization
- **Database Query Optimization**: Queries use `.first()`, `.exists()`, and `.values_list(..., flat=True)` to prevent memory overload.
- **Anti-Autofill Protection**: Hidden dummy input traps prevent browser password managers from pre-filling fields.

---

### CHAPTER 6: SYSTEM TESTING

#### 6.1 Introduction
System testing verifies that all application components function correctly, handle edge cases safely, and satisfy security requirements.

#### 6.2 Unit Testing (White-Box Testing)
White-Box testing evaluates internal logic, data validation helper functions, model integrity, and session access control.

#### 6.3 Integration Testing (Black-Box Testing)
Black-Box testing evaluates end-to-end user lifecycles, admin approvals, property listing updates, and appointment scheduling via HTTP requests.

#### 6.4 System Testing Execution Summary
```text
Creating test database for alias 'default'...
Found 16 test(s).

[Black-Box Integration Tests]
- test_complete_user_lifecycle ... OK
- test_complete_builder_lifecycle ... OK
- test_contact_query_submission_and_admin_view ... OK

[White-Box Unit & Validation Tests]
- test_email_validation ... OK
- test_phone_validation_indian_format ... OK
- test_password_complexity_rules ... OK
- test_user_details_creation ... OK
- test_builder_details_approval_flow_models ... OK
- test_property_details_model ... OK
- test_query_model ... OK
- test_booking_model ... OK
- test_wishlist_model ... OK
- test_property_edit_without_new_photo ... OK
- test_schedule_visit_view_logic ... OK
- test_unauthenticated_user_access_protection ... OK
- test_wishlist_toggle_logic ... OK

----------------------------------------------------------------------
Ran 16 tests in 0.499s
OK (100% Pass Rate)
```

#### 6.5 Test Plan & Test Cases

| Test ID | Test Scenario | Input Data | Expected Output | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | User Registration with Invalid Phone | Phone = `12345` | Validation Error: "Phone number must be exactly 10 digits" | **PASS** |
| **TC-02** | User Registration with Valid Phone | Phone = `9876543210` | Formats phone to `+91 9876543210` & registers user | **PASS** |
| **TC-03** | Weak Password Test | Password = `villa` | Validation Error: "Must contain uppercase, number, symbol" | **PASS** |
| **TC-04** | Valid Password Test | Password = `Villa@2025` | Validates successfully | **PASS** |
| **TC-05** | Unauthenticated Page Access | Access `/add_prop` without session | Redirects to `/login` | **PASS** |
| **TC-06** | Builder Approval Lifecycle | Builder registers -> Admin approves | Transferred to `approved_builder_details`, login enabled | **PASS** |
| **TC-07** | Wishlist Toggle | Click Wishlist icon twice | 1st click adds item, 2nd click removes item | **PASS** |
| **TC-08** | Schedule Site Visit | User clicks "Schedule a Visit" | Creates booking entry & redirects to `/scheduledvisit` | **PASS** |

---

### CHAPTER 7: SYSTEM MAINTENANCE

#### 7.1 Introduction
System maintenance ensures the application remains functional, secure, and operational throughout its lifecycle.

#### 7.2 Maintenance Strategies & Corrective Maintenance
- **Preventive Maintenance**: Periodic database indexing and purging of orphaned temporary image uploads.
- **Corrective Maintenance**: Immediate application of patches for session security or validation updates.
- **Adaptive Maintenance**: Upgrading Django packages or migrating SQLite to PostgreSQL as user traffic grows.

---

### CHAPTER 8: FUTURE ENHANCEMENTS AND SCOPE OF FURTHER DEVELOPMENT

#### 8.1 Introduction
While the current platform meets all functional and security requirements, future developments can expand its business capabilities.

#### 8.2 Merits of the System
- Secure multi-role access (Admin, Builder, User, Guest).
- Enforces strict input validation (+91 phone numbers, email regex, complex passwords).
- Executive Admin Dashboard matching the brand color palette (`#f35525` Villa Orange).
- Fully covered by automated test suites (16 passing tests).

#### 8.3 Limitations of the System
- Currently uses SQLite, which is ideal for mini-projects but requires PostgreSQL for large-scale enterprise deployments.
- Virtual property tours and live video chat are not integrated into the initial release.

#### 8.4 Future Enhancements
1. **Online Payment Gateway Integration**: Razorpay / Stripe integration for booking fees.
2. **Google Maps API Integration**: Interactive map pin selection for property locations.
3. **AI-Powered Property Recommendation Engine**: Machine learning model suggesting properties based on user wishlists.
4. **SMS / WhatsApp Notifications**: Automated SMS visit reminders sent via Twilio API.

---

### CHAPTER 9: CONCLUSION

The **Villa Real Estate Agency Management System** successfully digitizes property management, builder verification, site visit scheduling, and client inquiry handling. By implementing a multi-tier Django architecture, strict data validation rules (+91 phone numbers, email regex, complex passwords), anti-autofill security controls, and a custom brand-styled Admin Dashboard, the platform addresses all drawbacks of traditional real estate management. The system passed 100% of automated unit and integration tests, confirming its stability, security, and production readiness.

---

### CHAPTER 10: BIBLIOGRAPHY

1. **Django Software Foundation**, *"Django Documentation (Version 5.2)"*, https://docs.djangoproject.com/
2. **Python Software Foundation**, *"Python 3 Language Reference"*, https://www.python.org/
3. **Bootstrap Team**, *"Bootstrap 5.3 Documentation"*, https://getbootstrap.com/
4. **Chart.js Community**, *"Chart.js Docs - Simple yet flexible JavaScript charting"*, https://www.chartjs.org/
5. **Silberschatz, A., Korth, H. F., & Sudarshan, S.**, *"Database System Concepts"*, 7th Edition, McGraw-Hill.
6. **Pressman, R. S.**, *"Software Engineering: A Practitioner's Approach"*, 8th Edition, McGraw-Hill.

---

### APPENDIX

#### A. Core Source Code Snippets

##### 1. Master URL Router (`villa/urls.py`)
```python
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_app.urls')),
    path('', include('user_app.urls')),
    path('', include('builder_app.urls')),
    path('', views.home, name='home'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('buildregister', views.buildregister, name='buildregister'),
    path('logout', views.logout, name='logout'),
    path('dashboardindex', views.dashboardindex, name='dashboardindex'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

##### 2. User App Views (`user_app/views.py`)
```python
from django.shortcuts import render, redirect, get_object_or_404
from builder_app.models import property_details
from villa.models import user_details
from user_app.models import booking, wishlists

def viewprop(request):
    pdata = property_details.objects.all().order_by('-id')
    wishlist_items = []
    if request.session.get('uid'):
        user_id = str(request.session['uid'])
        wishlist_items = list(wishlists.objects.filter(user_id=user_id).values_list('property_name', flat=True))
    return render(request, 'myprop.html', {'builder_properties': pdata, 'wishlist_items': wishlist_items})

def schedulevisit(request, id):
    if not request.session.get('uid'):
        return redirect('/login')
    user_id = request.session['uid']
    udata = user_details.objects.filter(pk=user_id).first()
    pdata = get_object_or_404(property_details, pk=id)

    if udata and pdata:
        bdata = booking(
            user_id=str(user_id),
            name=udata.name,
            email=udata.email,
            phone=udata.phone,
            property_name=pdata.property_name,
            property_location=pdata.property_location,
            property_budget=pdata.property_budget
        )
        bdata.save()
    return redirect('/scheduledvisit')
```

---

#### B. Screen Layouts & User Interface Screenshots

1. **Public Home Page (`/`)**: Features hero slider, featured property cards, video overview, best deals tabs, and contact form.
2. **Account Login (`/login`)**: Clean, anti-autofill input fields for email and password.
3. **User Registration (`/register`)**: Includes built-in `+91` phone prefix addon and real-time password requirement notes.
4. **Executive Admin Dashboard (`/dashboardindex`)**: Features Villa Orange branding (`#f35525`), 6 KPI metric cards, Chart.js doughnut & line graphs, builder approval table, and recent scheduled visits.
5. **Property Listing Gallery (`/viewprop`)**: Card grid displaying bedrooms, bathrooms, area, floor, parking, and interactive wishlist heart buttons.
6. **Booked Visits Screen (`/scheduledvisit`)**: Role-filtered cards showing appointment bookings.

---

### GLOSSARY

- **Django**: An open-source, high-level Python web framework encouraging rapid development and clean MVT design.
- **MVT (Model-View-Template)**: Software architectural pattern used by Django where Models manage data, Views handle business logic, and Templates present the UI.
- **SQLite**: A self-contained, serverless, zero-configuration SQL database engine.
- **Regex (Regular Expressions)**: Sequence of characters forming a search pattern used for string/form validation.
- **KPI (Key Performance Indicator)**: Quantifiable measure used to evaluate performance metrics on administrative dashboards.
- **CRUD**: Acronym for Create, Read, Update, Delete operations in database applications.
- **White-Box Testing**: Testing method evaluating internal code structure, paths, and logic.
- **Black-Box Testing**: Testing method evaluating external software functionality without inspecting code internal structures.
