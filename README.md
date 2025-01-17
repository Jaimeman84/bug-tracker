# Bug Tracking Tool

A lightweight bug tracking application built with Python and Streamlit, designed for small project teams to effectively manage and track bugs.

## Features

### Dashboard
- Overview of total bugs, open bugs, and resolved bugs
- Interactive pie chart showing bug distribution by status with custom colors
- Bar chart displaying bugs by severity levels
- Recent bugs list with the latest reported issues
- Quick navigation to create bugs or view all bugs

### Bug Management
- Create detailed bug reports with:
  - Title and description
  - Severity and priority levels
  - Assignment information
  - Steps to reproduce
  - Expected and actual results
- Filter bugs by multiple criteria:
  - Status (Open, In Progress, Resolved, Closed)
  - Severity (Low, Medium, High, Critical)
  - Priority (Low, Medium, High)

### Analytics
- Interactive visualizations:
  - Status distribution (donut chart)
  - Severity breakdown (bar chart)
  - Bug creation trends over time
  - Priority vs Severity analysis
- Performance metrics:
  - Resolution rate
  - Average resolution time
  - Bug distribution statistics

### Reporting
- Generate reports in multiple formats:
  - Excel reports with detailed bug information
  - PDF reports with bug summaries
- Filter reports by date range
- Download generated reports

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jaimeman84/bug-tracker.git
cd bug-tracker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Requirements

```
streamlit==1.22.0
numpy==1.24.3
pandas==1.5.3
plotly==5.13.1
fpdf==1.7.2
SQLAlchemy==2.0.15
pytest==7.3.1
pytest-cov==4.0.0
python-dotenv==1.0.0
openpyxl==3.1.2
```

## Project Structure

```
bug_tracker/
├── src/
│   ├── models/
│   │   ├── bug.py          # Bug data model
│   │   └── user.py         # User data model
│   ├── services/
│   │   ├── bug_service.py      # Bug management logic
│   │   ├── report_service.py   # Report generation
│   │   └── analytics_service.py # Analytics calculations
│   ├── database/
│   │   └── db_manager.py   # Database operations
│   └── utils/
│       └── constants.py     # Application constants
├── tests/
│   ├── test_bug_service.py
│   ├── test_report_service.py
│   └── test_analytics_service.py
├── app.py                   # Main application
├── config.py               # Configuration settings
├── requirements.txt
└── README.md
```

## Running the Application

1. Start the application:
```bash
streamlit run app.py
```

2. Access via browser at `http://localhost:8501`

## Using the Application

1. **Dashboard**
   - View overall bug statistics
   - See recent bugs
   - Access quick actions

2. **Creating Bugs**
   - Click "Create Bug" in the navigation
   - Fill in all required fields
   - Submit to create a new bug

3. **Viewing Bugs**
   - Use the "Bug List" page
   - Apply filters as needed
   - Click on bugs to view details

4. **Analytics**
   - Access the "Analytics" page
   - View different charts and metrics
   - Use interactive features to explore data

5. **Generating Reports**
   - Go to the "Reports" page
   - Select report format (Excel/PDF)
   - Apply date filters if needed
   - Generate and download reports

## Running Tests

Execute the test suite:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=src tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## Development Guidelines

- Follow SOLID principles
- Write unit tests for new features
- Use type hints
- Follow PEP 8 style guide
- Document new functions and classes

## Troubleshooting

If you encounter version compatibility issues:
1. Uninstall conflicting packages:
```bash
pip uninstall numpy pandas
```

2. Reinstall with specific versions:
```bash
pip install numpy==1.24.3 pandas==1.5.3
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support:
1. Check the issues page for known problems
2. Create a new issue if needed
3. Contact the development team

## Acknowledgments

- Streamlit for the web framework
- SQLAlchemy for database operations
- Plotly for interactive visualizations