# 🏭 Factory Management System
A comprehensive web-based application designed to streamline and manage factory operations efficiently. This system encompasses modules for employee management, production tracking, inventory control, and more.​


## 🚀 Features  
- Employee Management: Add, update, and manage employee records seamlessly.

- Production Tracking: Monitor production lines, track outputs, and manage schedules.

- Inventory Control: Keep tabs on raw materials and finished goods inventory.

- Reporting: Generate insightful reports to aid in decision-making.

- User Authentication: Secure login system to protect sensitive data.  

## 🛠️ Tech Stack  
- Backend: Python, Flask

- Frontend: HTML, CSS, JavaScript

- Database: MySQL

- Containerization: Docker, Docker Compose

## 📁 Project Structure
```
DB_Project/
├── app/                   # Core application files
│   ├── static/            # Static assets (CSS, JS, images)
│   ├── templates/         # HTML templates
│   ├── __init__.py        # Application factory
│   └── routes.py          # Route definitions
├── test/                  # Test cases
├── .github/workflows/     # GitHub Actions workflows
├── .idea/                 # IDE configurations
├── factory_db.sql         # Database schema
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose setup
└── run.py                 # Application entry point
```

## 🐳 Getting Started with Docker  
**Clone the Repository:**

```bash
git clone https://github.com/abdulahad1015/DB_Project.git
cd DB_Project  
```

**Build and Run with Docker Compose:**

```bash
docker-compose up --build
```

**Access the Application**: Navigate to ```http://localhost:5000``` in your web browser.

## 🧪 Running Tests
To execute the test suite:​

```bash
python -m unittest discover -s test
```

## 🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.​