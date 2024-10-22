# Employee Clock-In System

## Table of Contents

- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [UX Design Process](#ux-design-process)
  - [User Personas](#user-personas)
  - [User Stories](#user-stories)
  - [Design Goals](#design-goals)
  - [Wireframes and Mockups](#wireframes-and-mockups)
    - [Home Page](#home-page)
    - [Login Page](#login-page)
    - [Dashboard](#dashboard)
    - [Clock-In Page](#clock-in-page)
    - [Clock-In History Page](#clock-in-history-page)
    - [Profile Creation and Editing](#profile-creation-and-editing)
- [Implementation](#implementation)
  - [Home Page](#home-page-1)
  - [Login and Registration](#login-and-registration)
  - [Dashboard](#dashboard-1)
  - [Clock-In Functionality](#clock-in-functionality)
  - [Clock-In History](#clock-in-history)
  - [Profile Management](#profile-management)
- [Conclusion](#conclusion)
- [Appendix](#appendix)
  - [Diagrams and Screenshots](#diagrams-and-screenshots)

---

## Introduction

This document outlines the UX design work undertaken for the Employee Clock-In System project. It details the design process, including wireframes, mockups, and diagrams created to visualize the user interface and experience. The reasoning behind design decisions is explained, and the implementation of these designs is demonstrated.

## Project Overview

The Employee Clock-In System is a web application built using Django. It allows employees to:

- Register and log in to their accounts.
- Create and manage their profiles.
- Clock in and clock out of work.
- View their clock-in history for the current month.
- Manage job records (e.g., jobs done, hours worked).

## UX Design Process

### User Personas

1. **Regular Employee**

   - **Goals:**
     - Easily clock in and out.
     - View clock-in history.
     - Manage personal profile.

2. **Administrator/Superuser**

   - **Goals:**
     - Oversee employee clock-ins.
     - Manage employee profiles.
     - Access administrative functions.

### User Stories

- **As a regular employee, I want to:**

  - Register and log in securely.
  - Create and edit my profile.
  - Clock in when I start work and clock out when I finish.
  - View my clock-in history for the current month.

- **As an administrator, I want to:**

  - Access an administrative dashboard.
  - View all employee clock-in records.
  - Manage employee profiles.

### Design Goals

- **Simplicity:** Ensure the interface is clean and easy to navigate.
- **Clarity:** Provide clear instructions and feedback to the user.
- **Responsiveness:** Design the UI to be responsive across devices.
- **Accessibility:** Use accessible design practices for all users.

### Wireframes and Mockups

#### Home Page

- **Description:** The landing page introduces the application and provides navigation links to register or log in.
- **Design Elements:**
  - Application title and brief description.
  - Prominent buttons for "Register" and "Login".
  - A navigation bar with links to other pages (once logged in).


#### Login Page

- **Description:** Allows users to log in using their credentials.
- **Design Elements:**
  - Username and password fields.
  - "Remember Me" checkbox (optional).
  - "Forgot Password" link.
  - Submit button.


#### Dashboard

- **Description:** The main hub for logged-in users, providing access to all functionalities.
- **Design Elements:**
  - Welcome message with the user's name.
  - Navigation links or buttons to:
    - Clock In/Out.
    - View Clock-In History.
    - Manage Profile.
    - Log Out.


#### Clock-In Page

- **Description:** Allows users to clock in or out.
- **Design Elements When Not Clocked In:**
  - Message indicating the user is not clocked in.
  - "Clock In" button.

- **Design Elements When Clocked In:**
  - Message displaying the clock-in time.
  - "Clock Out" button.


#### Clock-In History Page

- **Description:** Displays a list of the user's clock-in records for the current month.
- **Design Elements:**
  - Table listing:
    - Clock-In Time.
    - Clock-Out Time.
    - Duration.
  - Option to navigate to previous months (optional feature).


#### Profile Creation and Editing

- **Description:** Allows users to create or edit their profiles.
- **Design Elements:**
  - Form fields for:
    - First Name
    - Last Name
    - Date of Birth
    - Address
    - Phone Number
    - Email Address
  - Submit button.

---

## Implementation

The designs created during the UX process were implemented using Django templates, views, and models. The following sections demonstrate how each design was realized in the application.

### Home Page

- **Implementation Details:**
  - Used a simple template extending a base layout.
  - Included navigation links to "Register" and "Login".
  - Displayed a brief introduction to the application.

- **Result:**
  - The home page matches the wireframe, providing a clear entry point for users.

### Login and Registration

- **Implementation Details:**
  - Created custom forms for user authentication.
  - Styled forms using Bootstrap for consistency.
  - Included helpful error messages and validation.

- **Result:**
  - The login and registration pages align with the mockups, offering a user-friendly experience.

### Dashboard

- **Implementation Details:**
  - Displayed a welcome message with the user's name.
  - Provided buttons for key actions: Clock In/Out, View History, Manage Profile.
  - Ensured the dashboard is responsive and accessible.

- **Result:**
  - The dashboard serves as a central hub, reflecting the design goals of simplicity and clarity.

### Clock-In Functionality

- **Implementation Details:**
  - Implemented clock-in and clock-out logic in views.
  - Displayed appropriate messages based on the user's clock-in status.
  - Ensured that time fields are handled automatically without user input.

- **Result:**
  - The clock-in page functions as designed, with messages and buttons updating based on status.

### Clock-In History

- **Implementation Details:**
  - Created a view to retrieve clock-in records for the current month.
  - Designed a template to display records in a table format.
  - Included duration calculations and formatted dates.

- **Result:**
  - Users can view their clock-in history, matching the wireframe and fulfilling user stories.

### Profile Management

- **Implementation Details:**
  - Developed forms for creating and editing profiles.
  - Applied validation rules (e.g., age verification).
  - Provided feedback messages upon successful updates or errors.

- **Result:**
  - The profile pages adhere to the design, allowing users to manage their information effectively.

---

## Conclusion

The UX design process guided the development of the Employee Clock-In System. By creating wireframes and mockups, we established a clear vision for the application's interface and user experience. These designs were faithfully implemented, resulting in an application that meets the needs of its users through intuitive navigation, responsive design, and essential functionality.

---


**Please replace the placeholder image paths (`./diagrams/...` and `./screenshots/...`) with the actual paths to your wireframes and screenshots in your project repository.**


## Screenshots
### Large screen view:
![clockin-history](README-images/clockin-history.png)
![create-record](README-images/create-record.png)
![job-history](README-images/job-history.png)
![login](README-images/login.png)
![update-record](README-images/update-record.png)
![view-record](README-images/view-record.png)
![welcome-page](README-images/welcome-page.png)

### mobile view:
![create-record-mobile-navbar-open](README-images/create-record-mobile-navbar-open.png) ![create-record-mobile](README-images/create-record-mobile.png)

## Directory Structure

- `employeeapp/`: Contains the main application code.
- `manage.py`: The command-line utility for administrative tasks.
- `db.sqlite3`: The SQLite database file.
- `requirements.txt`: Lists the dependencies required for the project.
- `Procfile`: Configuration for deploying the app to Heroku or similar platforms.
- `clockin/`: Directory for clock-in related features and templates.

## Testing
UI has been tested manually, no unittesting involved.
During manual testing there was no bug found.
### CSS Checker:
![css-validator](README-images/css-validator.png)
### PEP8 Checker:
#### forms.py:
![forms-pep8](README-images/forms-pep8.png)
#### urls.py:
![url-pep8](README-images/url-pep8.png)
#### views.py:
![views-pep8](README-images/views-pep8.png)

## Sources
- [Icon Converter](https://www.icoconverter.com/):Great to make favicons
- [Font Awesome](https://fontawesome.com/account/general):Great for free icons
- [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/):Bootstrap source
- [Bootstrap](https://startbootstrap.com/):Bootstrap source
- [Image Color Picker](https://imagecolorpicker.com/): Used for selecting a harmonious color palette. 
- [GPT-4](https://chat.openai.com/?model=gpt-4): Utilized for generating images, texts, and providing explanations of elements.
- [Google](www.google.com): Employed for image research.
- [YouTube](www.youtube.com):multiple tutorials




## Setup Instructions

### Prerequisites

- Python 3.x
- Django
- SQLite (or another database if you prefer)
- Virtualenv (recommended)

### Installation

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd employeeapp-ver6-main
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply the migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7. **Access the application:**
    Open a web browser and go to `http://127.0.0.1:8000/`.

## Deployment

### Using Heroku

1. **Install the Heroku CLI:**
    Follow the instructions at https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku:**
    ```bash
    heroku login
    ```

3. **Create a new Heroku app:**
    ```bash
    heroku create
    ```

4. **Deploy the app:**
    ```bash
    git push heroku main
    ```

5. **Run database migrations on Heroku:**
    ```bash
    heroku run python manage.py migrate
    ```

6. **Create a superuser on Heroku:**
    ```bash
    heroku run python manage.py createsuperuser
    ```

## Usage

- **Admin Interface:** Access the admin interface at `http://127.0.0.1:8000/admin` to manage employee data.
- **Clock-in Interface:** Employees can clock in and out using the interface at the root URL `http://127.0.0.1:8000/`.

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Open a pull request.

## Contact Information
For further inquiries or feedback, please contact:

Peter Rimaszecsi
Email: rim.peter@hotmail.com
