# Bug Tracking Tool

A lightweight bug tracking application built with Python and Streamlit, designed for small project teams to effectively manage and track bugs.

## Features

- Create, assign, and track bugs with detailed information
- Categorize bugs by severity and priority
- Filter and search bugs
- Generate bug reports in PDF and Excel formats
- Interactive dashboard with bug analytics
- Modern, responsive user interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bug-tracker.git
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

- Python 3.8+
- Streamlit
- Pandas
- FPDF
- SQLite3 (for development)

All dependencies are listed in `requirements.txt`.

## Project Structure

```
bug_tracker/
├── src/                # Source code
│   ├── models/        # Data models
│   ├── services/      # Business logic
│   ├── database/      # Database operations
│   └── utils/         # Utility functions
├── tests/             # Unit tests
├── pages/             # Streamlit pages
├── app.py             # Main application
└── README.md
```

## Running the Application

1. Start the Streamlit server:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

## Running Tests

Execute the test suite:
```bash
python -m pytest tests/
```

## Usage

1. **Dashboard**: View bug statistics and analytics
2. **Create Bug**: Submit new bug reports with detailed information
3. **Bug List**: View and filter existing bugs
4. **Reports**: Generate Excel or PDF reports

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team.