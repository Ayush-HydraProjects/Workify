# Workify - User Profile Management System

Workify is a web-based platform that allows users to manage their profiles, update personal details, and change their avatars and bios. The system is designed with ease of use in mind and features a clean, modern interface that enhances user experience.

## Features

- **User Authentication**: Secure login and registration system.
- **Profile Management**: Users can update their profile details, including username, email, avatar, and bio.
- **Password Management**: Allows users to change their password securely.
- **Responsive Design**: Works on all devices with a mobile-first approach.
- **Error Handling**: Clear error messages and user feedback during form submission.
- **Interactive Avatar Update**: Users can upload a new avatar image and see a preview before saving.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript (Bootstrap 4 for responsive design)
- **Database**: SQLite (or PostgreSQL for production)
- **Authentication**: Django Authentication
- **Styling**: Custom CSS (with animations for better UX)
- **Version Control**: Git, GitHub

## Project Setup

Follow the steps below to get your development environment set up.

### Prerequisites

Ensure that the following are installed:

- Python 3.8 or higher
- pip (Python package installer)
- Git

### 1. Clone the repository

First, clone the project to your local machine:

```bash
git clone https://github.com/shivampatel1001/Workify.git
cd Workify
````

### 2\. Create a Virtual Environment

It is recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv myenv
```

Activate the virtual environment:

*   **On Windows**:
    
    ```bash
    myenv\Scripts\activate
    ```
    
*   **On macOS/Linux**:
    
    ```bash
    source myenv/bin/activate
    ```
    

### 3\. Install Dependencies

Once the virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 4\. Set Up the Database

Run the following commands to set up the database:

```bash
python manage.py migrate
```

This will set up the necessary database tables.

### 5\. Create a Superuser (Optional)

If you need admin access to the project:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the superuser.

### 6\. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You can now access the application at `http://127.0.0.1:8000/` in your browser.

### 7\. Accessing the Admin Panel

To access the admin panel, go to `http://127.0.0.1:8000/admin/` and log in using the superuser credentials you created earlier.

* * *

How It Works
------------

### 1\. User Registration

Users can register by providing their username, email, and password. The system will automatically authenticate them.

### 2\. User Profile Page

Once logged in, users can visit their profile page where they can:

*   **View and update their profile image (avatar)**.
*   **Edit their username and email**.
*   **Update their bio**.
*   **Change their password** via a separate password change page.

### 3\. Error Handling

In case of form errors (invalid inputs, empty fields), the system displays helpful error messages to guide the user to correct them.


Contributing
------------

1.  **Fork the repository** to your GitHub account.
2.  **Clone your fork** to your local machine.
3.  **Create a new branch** for your feature:
    
    ```bash
    git checkout -b feature-branch-name
    ```
    
4.  **Make changes** to the codebase.
5.  **Commit your changes**:
    
    ```bash
    git commit -m "Add feature"
    ```
    
6.  **Push your changes** to your remote branch:
    
    ```bash
    git push origin feature-branch-name
    ```
    
7.  **Create a pull request** from your fork to the main repository.
   

Acknowledgements
----------------

*   [Django](https://www.djangoproject.com/) - The web framework used for this project.
*   [Bootstrap](https://getbootstrap.com/) - Frontend framework for responsive design.
*   [Font Awesome](https://fontawesome.com/) - Icons used for UI.
