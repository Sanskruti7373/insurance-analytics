# 📊 Insurance Analytics System

A comprehensive data analytics platform for insurance companies, providing insights into customer behavior, policy performance, and business metrics.

![Project Banner](https://img.shields.io/badge/Python-3.8+-blue.svg)
![SQL](https://img.shields.io/badge/PostgreSQL-12+-316192.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 🎯 Project Overview

This project analyzes insurance application data to provide actionable business insights through automated reporting, interactive dashboards, and comprehensive data analysis.

### Key Features

- 📊 **Automated Analytics** - Python scripts for data analysis
- 📈 **Visual Reports** - PNG charts, Excel reports with graphs
- 🔄 **Power BI Integration** - Ready-to-import datasets
- 💾 **PostgreSQL Database** - Normalized schema with 5 core tables
- 🎨 **Professional Visualizations** - Publication-ready charts

## 📸 Screenshots

### Executive Dashboard
![Dashboard](screenshots/dashboard.png)

### Sample Analysis Charts
![Charts](screenshots/charts.png)

## 🛠️ Technologies Used

- **Database:** PostgreSQL 15
- **Programming:** Python 3.11
- **Data Analysis:** pandas, numpy
- **Visualization:** matplotlib, seaborn
- **Reporting:** openpyxl, Power BI
- **Data Generation:** Faker

## 📊 Database Schema
users (500+ records)
├── user_id (PK)
├── email, name, state, age
└── registration_date
policies (800+ records)
├── policy_id (PK)
├── user_id (FK)
├── policy_type, premium_amount
└── policy_status
quotes (600+ records)
├── quote_id (PK)
├── user_id (FK)
├── conversion_status
└── quoted_premium
page_visits (2000+ records)
├── visit_id (PK)
├── user_id (FK)
├── page_name, device_type
└── visit_date
support_tickets (200+ records)
├── ticket_id (PK)
├── user_id (FK)
├── issue_type, status
└── satisfaction_rating


## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- 8GB RAM recommended

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/insurance-analytics.git
cd insurance-analytics
```

### Step 2: Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Database Setup
```bash
# Create database
createdb insurance_simple

# Run schema
psql -U postgres -d insurance_simple -f sql/schema.sql
```

### Step 4: Configure Database Connection

Update `scripts/main_analysis_enhanced.py` with your database credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'insurance_simple',
    'user': 'your_username',
    'password': 'your_password',
    'port': 5432
}
```

### Step 5: Generate Sample Data
```bash
cd scripts
python data_generator.py
```

### Step 6: Run Analysis
```bash
python main_analysis_enhanced.py
```

## 📊 Output Files

After running the analysis, you'll get:

- **5 PNG Charts** - Visual analysis charts
- **Excel Report** - Multi-sheet workbook with embedded charts
- **Power BI Data** - Folder with CSV files ready for import

## 💡 Key Insights Generated

- Customer demographics and geographic distribution
- Policy performance by type (Auto, Home, Life, Health)
- Quote-to-policy conversion rates (20% average)
- Support ticket analysis and satisfaction scores
- Revenue analysis and trending

## 🔍 Sample Queries

### Top 5 Customers by Revenue
```sql
SELECT 
    u.first_name || ' ' || u.last_name as customer_name,
    SUM(p.premium_amount) as total_revenue
FROM users u
JOIN policies p ON u.user_id = p.user_id
WHERE p.policy_status = 'active'
GROUP BY u.user_id, customer_name
ORDER BY total_revenue DESC
LIMIT 5;
```

### Conversion Rate by Policy Type
```sql
SELECT 
    policy_type,
    COUNT(*) as total_quotes,
    COUNT(CASE WHEN converted_to_policy = true THEN 1 END) * 100.0 / COUNT(*) as conversion_rate
FROM quotes
GROUP BY policy_type
ORDER BY conversion_rate DESC;
```

## 📈 Future Enhancements

- [ ] Add machine learning for churn prediction
- [ ] Real-time dashboard with WebSockets
- [ ] RESTful API for data access
- [ ] Docker containerization
- [ ] Automated testing suite
- [ ] CI/CD pipeline

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your Name](https://linkedin.com/in/your-profile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Project developed as part of data analytics portfolio
- Sample data generated using Faker library
- Inspired by real-world insurance analytics needs

---

⭐ If you find this project useful, please consider giving it a star!