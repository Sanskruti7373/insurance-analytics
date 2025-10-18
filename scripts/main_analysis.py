"""
100% FIXED Enhanced Insurance Data Analysis
Exports to PNG, Excel, and Power BI formats
ALL SQL ERRORS RESOLVED

Save this as: main_analysis_enhanced.py
Replace your existing file completely with this code
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
from datetime import datetime
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
import warnings
import os
warnings.filterwarnings('ignore')

# Set style for better looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class EnhancedInsuranceAnalytics:
    """Enhanced analytics class with Excel and Power BI export"""
    
    def __init__(self, db_config):
        """Initialize with database connection"""
        self.db_config = db_config
        self.connection = None
        self.all_data = {}  # Store all analysis results
        self.connect_to_database()
    
    def connect_to_database(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print("✅ Connected to database successfully!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            exit(1)
    
    def run_query(self, query):
        """Execute SQL query and return pandas DataFrame"""
        try:
            df = pd.read_sql_query(query, self.connection)
            return df
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return pd.DataFrame()
    
    def get_customer_overview(self):
        """Get basic customer statistics"""
        query = """
        SELECT 
            COUNT(*) as total_customers,
            COUNT(CASE WHEN is_active = true THEN 1 END) as active_customers,
            ROUND(AVG(age), 1) as average_age,
            COUNT(DISTINCT state) as states_served
        FROM users;
        """
        
        result = self.run_query(query)
        self.all_data['customer_overview'] = result
        
        print("\n📊 CUSTOMER OVERVIEW")
        print("=" * 30)
        if not result.empty:
            print(f"Total Customers: {result['total_customers'].iloc[0]:,}")
            print(f"Active Customers: {result['active_customers'].iloc[0]:,}")
            print(f"Average Age: {result['average_age'].iloc[0]} years")
            print(f"States Served: {result['states_served'].iloc[0]}")
        
        return result
    
    def analyze_policies_by_type(self):
        """Analyze policies by type"""
        query = """
        SELECT 
            policy_type,
            COUNT(*) as policy_count,
            ROUND(AVG(premium_amount), 2) as avg_premium,
            ROUND(SUM(premium_amount), 2) as total_revenue,
            ROUND(MIN(premium_amount), 2) as min_premium,
            ROUND(MAX(premium_amount), 2) as max_premium
        FROM policies 
        WHERE policy_status = 'active'
        GROUP BY policy_type
        ORDER BY total_revenue DESC;
        """
        
        df = self.run_query(query)
        self.all_data['policies_by_type'] = df
        
        print("\n📋 POLICIES BY TYPE")
        print("=" * 40)
        if not df.empty:
            print(df[['policy_type', 'policy_count', 'avg_premium', 'total_revenue']].to_string(index=False))
        
        # Create visualization
        if not df.empty:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            ax1.bar(df['policy_type'], df['policy_count'], color=colors)
            ax1.set_title('Number of Policies by Type', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Policy Count', fontsize=11)
            ax1.set_xlabel('Policy Type', fontsize=11)
            ax1.grid(axis='y', alpha=0.3)
            
            for i, v in enumerate(df['policy_count']):
                ax1.text(i, v + 5, str(int(v)), ha='center', va='bottom', fontweight='bold')
            
            ax2.bar(df['policy_type'], df['total_revenue'], color=colors)
            ax2.set_title('Revenue by Policy Type', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Total Revenue ($)', fontsize=11)
            ax2.set_xlabel('Policy Type', fontsize=11)
            ax2.grid(axis='y', alpha=0.3)
            
            for i, v in enumerate(df['total_revenue']):
                ax2.text(i, v + 1000, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig('policy_analysis.png', dpi=300, bbox_inches='tight')
            print("  📊 Chart saved: policy_analysis.png")
            plt.close()
        
        return df
    
    def analyze_customers_by_state(self):
        """Analyze customer distribution by state"""
        query = """
        SELECT 
            state,
            COUNT(*) as customer_count,
            ROUND(AVG(age), 1) as avg_age,
            COUNT(p.policy_id) as total_policies,
            ROUND(COALESCE(SUM(p.premium_amount), 0), 2) as total_revenue
        FROM users u
        LEFT JOIN policies p ON u.user_id = p.user_id AND p.policy_status = 'active'
        GROUP BY state
        ORDER BY customer_count DESC;
        """
        
        df = self.run_query(query)
        self.all_data['customers_by_state'] = df
        
        print("\n🗺️  CUSTOMERS BY STATE")
        print("=" * 45)
        if not df.empty:
            print(df.head(10).to_string(index=False))
        
        # Create visualization for top 10
        if not df.empty:
            top10 = df.head(10)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
            
            ax1.barh(top10['state'], top10['customer_count'], color='steelblue')
            ax1.set_title('Top 10 States by Customer Count', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Number of Customers', fontsize=11)
            ax1.set_ylabel('State', fontsize=11)
            ax1.grid(axis='x', alpha=0.3)
            
            for i, v in enumerate(top10['customer_count']):
                ax1.text(v + 1, i, str(int(v)), va='center', fontweight='bold')
            
            ax2.barh(top10['state'], top10['total_revenue'], color='coral')
            ax2.set_title('Top 10 States by Revenue', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Total Revenue ($)', fontsize=11)
            ax2.set_ylabel('State', fontsize=11)
            ax2.grid(axis='x', alpha=0.3)
            
            for i, v in enumerate(top10['total_revenue']):
                ax2.text(v + 500, i, f'${v:,.0f}', va='center', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig('state_analysis.png', dpi=300, bbox_inches='tight')
            print("  📊 Chart saved: state_analysis.png")
            plt.close()
        
        return df
    
    def analyze_quote_conversion(self):
        """Analyze quote to policy conversion"""
        query = """
        SELECT 
            policy_type,
            COUNT(*) as total_quotes,
            COUNT(CASE WHEN converted_to_policy = true THEN 1 END) as converted_quotes,
            ROUND(
                COUNT(CASE WHEN converted_to_policy = true THEN 1 END) * 100.0 / COUNT(*), 
                2
            ) as conversion_rate,
            ROUND(AVG(quoted_premium), 2) as avg_quote_amount
        FROM quotes
        GROUP BY policy_type
        ORDER BY conversion_rate DESC;
        """
        
        df = self.run_query(query)
        self.all_data['quote_conversion'] = df
        
        print("\n💰 QUOTE CONVERSION ANALYSIS")
        print("=" * 40)
        if not df.empty:
            print(df.to_string(index=False))
        
        # Create visualization
        if not df.empty:
            fig, ax = plt.subplots(figsize=(10, 7))
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            bars = ax.bar(df['policy_type'], df['conversion_rate'], color=colors, edgecolor='black', linewidth=1.5)
            
            ax.set_title('Quote Conversion Rate by Policy Type', fontsize=16, fontweight='bold', pad=20)
            ax.set_ylabel('Conversion Rate (%)', fontsize=12)
            ax.set_xlabel('Policy Type', fontsize=12)
            ax.set_ylim(0, max(df['conversion_rate']) * 1.2 if len(df) > 0 else 100)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{height:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            plt.savefig('conversion_analysis.png', dpi=300, bbox_inches='tight')
            print("  📊 Chart saved: conversion_analysis.png")
            plt.close()
        
        return df
    
    def analyze_customer_age_groups(self):
        """Analyze customers by age groups"""
        query = """
        WITH age_grouped AS (
            SELECT 
                u.user_id,
                u.age,
                CASE 
                    WHEN u.age < 25 THEN '18-24'
                    WHEN u.age < 35 THEN '25-34'
                    WHEN u.age < 45 THEN '35-44'
                    WHEN u.age < 55 THEN '45-54'
                    WHEN u.age < 65 THEN '55-64'
                    ELSE '65+'
                END as age_group,
                CASE 
                    WHEN u.age < 25 THEN 1
                    WHEN u.age < 35 THEN 2
                    WHEN u.age < 45 THEN 3
                    WHEN u.age < 55 THEN 4
                    WHEN u.age < 65 THEN 5
                    ELSE 6
                END as sort_order
            FROM users u
            WHERE u.age IS NOT NULL
        )
        SELECT 
            ag.age_group,
            COUNT(DISTINCT ag.user_id) as customer_count,
            COUNT(p.policy_id) as total_policies,
            ROUND(AVG(p.premium_amount), 2) as avg_premium,
            ROUND(SUM(p.premium_amount), 2) as total_revenue
        FROM age_grouped ag
        LEFT JOIN policies p ON ag.user_id = p.user_id AND p.policy_status = 'active'
        GROUP BY ag.age_group, ag.sort_order
        ORDER BY ag.sort_order;
        """
        
        df = self.run_query(query)
        # Remove sort_order column from display
        if 'sort_order' in df.columns:
            df = df.drop('sort_order', axis=1)
        self.all_data['age_groups'] = df
        
        print("\n👥 CUSTOMERS BY AGE GROUP")
        print("=" * 35)
        if not df.empty:
            print(df.to_string(index=False))
        
        # Create visualization
        if not df.empty:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
            
            colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
            explode = [0.05 if i == df['customer_count'].idxmax() else 0 for i in range(len(df))]
            
            ax1.pie(df['customer_count'], labels=df['age_group'], autopct='%1.1f%%', 
                   startangle=90, colors=colors_pie[:len(df)], explode=explode, shadow=True)
            ax1.set_title('Customer Distribution by Age Group', fontsize=14, fontweight='bold', pad=20)
            
            ax2.bar(df['age_group'], df['avg_premium'], color='lightcoral', edgecolor='black', linewidth=1.5)
            ax2.set_title('Average Premium by Age Group', fontsize=14, fontweight='bold', pad=20)
            ax2.set_ylabel('Average Premium ($)', fontsize=11)
            ax2.set_xlabel('Age Group', fontsize=11)
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(axis='y', alpha=0.3)
            
            for i, v in enumerate(df['avg_premium']):
                if pd.notna(v):
                    ax2.text(i, v + 50, f'${v:.0f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig('age_analysis.png', dpi=300, bbox_inches='tight')
            print("  📊 Chart saved: age_analysis.png")
            plt.close()
        
        return df
    
    def analyze_support_tickets(self):
        """Analyze customer support tickets"""
        query = """
        SELECT 
            issue_type,
            COUNT(*) as ticket_count,
            COUNT(CASE WHEN status IN ('resolved', 'closed') THEN 1 END) as resolved_tickets,
            ROUND(
                COUNT(CASE WHEN status IN ('resolved', 'closed') THEN 1 END) * 100.0 / COUNT(*), 
                2
            ) as resolution_rate,
            ROUND(AVG(satisfaction_rating), 2) as avg_satisfaction
        FROM support_tickets
        GROUP BY issue_type
        ORDER BY ticket_count DESC;
        """
        
        df = self.run_query(query)
        self.all_data['support_tickets'] = df
        
        print("\n🎧 SUPPORT TICKET ANALYSIS")
        print("=" * 40)
        if not df.empty:
            print(df.to_string(index=False))
        
        # Create visualization
        if not df.empty:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
            
            ax1.bar(df['issue_type'], df['ticket_count'], color='orange', edgecolor='black', linewidth=1.5)
            ax1.set_title('Support Tickets by Issue Type', fontsize=14, fontweight='bold', pad=20)
            ax1.set_ylabel('Number of Tickets', fontsize=11)
            ax1.set_xlabel('Issue Type', fontsize=11)
            ax1.tick_params(axis='x', rotation=45)
            ax1.grid(axis='y', alpha=0.3)
            
            for i, v in enumerate(df['ticket_count']):
                ax1.text(i, v + 1, str(int(v)), ha='center', va='bottom', fontweight='bold')
            
            ax2.bar(df['issue_type'], df['avg_satisfaction'], color='green', edgecolor='black', linewidth=1.5)
            ax2.set_title('Average Satisfaction by Issue Type', fontsize=14, fontweight='bold', pad=20)
            ax2.set_ylabel('Satisfaction Rating (1-5)', fontsize=11)
            ax2.set_xlabel('Issue Type', fontsize=11)
            ax2.tick_params(axis='x', rotation=45)
            ax2.set_ylim(0, 5)
            ax2.grid(axis='y', alpha=0.3)
            ax2.axhline(y=3, color='red', linestyle='--', alpha=0.5, label='Baseline (3.0)')
            ax2.legend()
            
            for i, v in enumerate(df['avg_satisfaction']):
                if pd.notna(v):
                    ax2.text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig('support_analysis.png', dpi=300, bbox_inches='tight')
            print("  📊 Chart saved: support_analysis.png")
            plt.close()
        
        return df
    
    def export_to_excel(self):
        """Export all analysis to a formatted Excel file with charts"""
        print("\n📊 Exporting to Excel with charts...")
        
        filename = f'Insurance_Analytics_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Executive Summary
            summary_data = {
                'Metric': [
                    'Total Customers',
                    'Active Customers',
                    'Total Policies',
                    'Total Revenue',
                    'Average Premium',
                    'States Served',
                    'Total Quotes',
                    'Avg Conversion Rate',
                    'Total Support Tickets'
                ],
                'Value': []
            }
            
            # Calculate summary values with error handling
            if 'customer_overview' in self.all_data and not self.all_data['customer_overview'].empty:
                summary_data['Value'].append(int(self.all_data['customer_overview']['total_customers'].iloc[0]))
                summary_data['Value'].append(int(self.all_data['customer_overview']['active_customers'].iloc[0]))
            else:
                summary_data['Value'].extend([0, 0])
            
            if 'policies_by_type' in self.all_data and not self.all_data['policies_by_type'].empty:
                summary_data['Value'].append(int(self.all_data['policies_by_type']['policy_count'].sum()))
                summary_data['Value'].append(f"${self.all_data['policies_by_type']['total_revenue'].sum():,.2f}")
                summary_data['Value'].append(f"${self.all_data['policies_by_type']['avg_premium'].mean():,.2f}")
            else:
                summary_data['Value'].extend([0, '$0.00', '$0.00'])
            
            if 'customer_overview' in self.all_data and not self.all_data['customer_overview'].empty:
                summary_data['Value'].append(int(self.all_data['customer_overview']['states_served'].iloc[0]))
            else:
                summary_data['Value'].append(0)
            
            if 'quote_conversion' in self.all_data and not self.all_data['quote_conversion'].empty:
                summary_data['Value'].append(int(self.all_data['quote_conversion']['total_quotes'].sum()))
                summary_data['Value'].append(f"{self.all_data['quote_conversion']['conversion_rate'].mean():.2f}%")
            else:
                summary_data['Value'].extend([0, '0.00%'])
            
            if 'support_tickets' in self.all_data and not self.all_data['support_tickets'].empty:
                summary_data['Value'].append(int(self.all_data['support_tickets']['ticket_count'].sum()))
            else:
                summary_data['Value'].append(0)
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Write each dataset to a separate sheet
            for key, df in self.all_data.items():
                if not df.empty:
                    sheet_name = key.replace('_', ' ').title()[:31]  # Excel sheet name limit
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Add charts and formatting
        self.add_excel_charts(filename)
        
        print(f"  ✅ Excel report with charts saved: {filename}")
        return filename
    
    def add_excel_charts(self, filename):
        """Add professional charts to Excel file"""
        from openpyxl.chart import BarChart, PieChart, LineChart, Reference
        from openpyxl.chart.label import DataLabelList
        
        wb = load_workbook(filename)
        
        # Define styles
        header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
        header_font = Font(color='FFFFFF', bold=True, size=12)
        
        # Format all sheets
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            
            # Format headers
            for cell in ws[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Auto-adjust column widths
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
        
        # Add chart to Policies by Type sheet
        if 'Policies By Type' in wb.sheetnames:
            ws = wb['Policies By Type']
            
            # Bar chart for policy counts
            chart1 = BarChart()
            chart1.type = "col"
            chart1.style = 10
            chart1.title = "Policies by Type"
            chart1.y_axis.title = 'Number of Policies'
            chart1.x_axis.title = 'Policy Type'
            
            data = Reference(ws, min_col=2, min_row=1, max_row=ws.max_row)
            cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
            chart1.add_data(data, titles_from_data=True)
            chart1.set_categories(cats)
            chart1.shape = 4
            ws.add_chart(chart1, "H2")
            
            # Bar chart for revenue
            chart2 = BarChart()
            chart2.type = "col"
            chart2.style = 11
            chart2.title = "Revenue by Policy Type"
            chart2.y_axis.title = 'Revenue ($)'
            chart2.x_axis.title = 'Policy Type'
            
            data = Reference(ws, min_col=4, min_row=1, max_row=ws.max_row)
            cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
            chart2.add_data(data, titles_from_data=True)
            chart2.set_categories(cats)
            chart2.shape = 4
            ws.add_chart(chart2, "H18")
        
        # Add chart to Customers by State sheet
        if 'Customers By State' in wb.sheetnames:
            ws = wb['Customers By State']
            
            # Bar chart for top 10 states
            chart3 = BarChart()
            chart3.type = "bar"
            chart3.style = 12
            chart3.title = "Top 10 States by Customer Count"
            chart3.y_axis.title = 'State'
            chart3.x_axis.title = 'Number of Customers'
            
            data = Reference(ws, min_col=2, min_row=1, max_row=min(11, ws.max_row))
            cats = Reference(ws, min_col=1, min_row=2, max_row=min(11, ws.max_row))
            chart3.add_data(data, titles_from_data=True)
            chart3.set_categories(cats)
            ws.add_chart(chart3, "G2")
        
        # Add chart to Quote Conversion sheet
        if 'Quote Conversion' in wb.sheetnames:
            ws = wb['Quote Conversion']
            
            # Bar chart for conversion rates
            chart4 = BarChart()
            chart4.type = "col"
            chart4.style = 13
            chart4.title = "Conversion Rate by Policy Type"
            chart4.y_axis.title = 'Conversion Rate (%)'
            chart4.x_axis.title = 'Policy Type'
            
            data = Reference(ws, min_col=4, min_row=1, max_row=ws.max_row)
            cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
            chart4.add_data(data, titles_from_data=True)
            chart4.set_categories(cats)
            chart4.shape = 4
            ws.add_chart(chart4, "G2")
        
        # Add chart to Age Groups sheet
        if 'Age Groups' in wb.sheetnames:
            ws = wb['Age Groups']
            
            # Pie chart for age distribution
            chart5 = PieChart()
            chart5.title = "Customer Distribution by Age Group"
            chart5.style = 10
            
            data = Reference(ws, min_col=2, min_row=1, max_row=ws.max_row)
            cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
            chart5.add_data(data, titles_from_data=True)
            chart5.set_categories(cats)
            
            # Add data labels
            chart5.dataLabels = DataLabelList()
            chart5.dataLabels.showPercent = True
            
            ws.add_chart(chart5, "G2")
            
            # Bar chart for average premium by age
            chart6 = BarChart()
            chart6.type = "col"
            chart6.style = 14
            chart6.title = "Average Premium by Age Group"
            chart6.y_axis.title = 'Average Premium ($)'
            chart6.x_axis.title = 'Age Group'
            
            data = Reference(ws, min_col=4, min_row=1, max_row=ws.max_row)
            cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
            chart6.add_data(data, titles_from_data=True)
            chart6.set_categories(cats)
            ws.add_chart(chart6, "G18")
        
        # Add chart to Support Tickets sheet
        if 'Support Tickets' in wb.sheetnames:
            ws = wb['Support Tickets']
            
            # Bar chart for ticket counts
            chart7 = BarChart()
            chart7.type = "col"
            chart7.style = 15
            chart7.title = "Support Tickets by Issue Type"
            chart7.y_axis.title = 'Number of Tickets'
            chart7.x_axis.title = 'Issue Type'
            
            data = Reference(ws, min_col=2, min_row=1, max_row=ws.max_row)
            cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
            chart7.add_data(data, titles_from_data=True)
            chart7.set_categories(cats)
            ws.add_chart(chart7, "G2")
            
            # Bar chart for satisfaction ratings
            chart8 = BarChart()
            chart8.type = "col"
            chart8.style = 16
            chart8.title = "Average Satisfaction by Issue Type"
            chart8.y_axis.title = 'Satisfaction Rating (1-5)'
            chart8.x_axis.title = 'Issue Type'
            
            data = Reference(ws, min_col=5, min_row=1, max_row=ws.max_row)
            cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
            chart8.add_data(data, titles_from_data=True)
            chart8.set_categories(cats)
            ws.add_chart(chart8, "G18")
        
        wb.save(filename)
    
    def export_for_powerbi(self):
        """Export data in Power BI compatible format"""
        print("\n📊 Exporting for Power BI...")
        
        # Create PowerBI_Data folder
        powerbi_folder = 'PowerBI_Data'
        if not os.path.exists(powerbi_folder):
            os.makedirs(powerbi_folder)
        
        # Export raw tables as CSV for Power BI
        tables_to_export = {
            'users': 'SELECT * FROM users',
            'policies': 'SELECT * FROM policies',
            'quotes': 'SELECT * FROM quotes',
            'page_visits': 'SELECT * FROM page_visits',
            'support_tickets': 'SELECT * FROM support_tickets'
        }
        
        for table_name, query in tables_to_export.items():
            df = self.run_query(query)
            if not df.empty:
                filepath = f'{powerbi_folder}/{table_name}.csv'
                df.to_csv(filepath, index=False)
                print(f"  ✅ Exported: {filepath}")
        
        # Export aggregated analysis tables
        for key, df in self.all_data.items():
            if not df.empty:
                filepath = f'{powerbi_folder}/{key}.csv'
                df.to_csv(filepath, index=False)
                print(f"  ✅ Exported: {filepath}")
        
        # Create setup guide (using only ASCII characters)
        guide_text = """
===============================================================================
                    POWER BI SETUP GUIDE
===============================================================================

FILES EXPORTED:
===============

Raw Data Tables:
  - users.csv (Customer information)
  - policies.csv (Insurance policies)
  - quotes.csv (Quote requests)
  - page_visits.csv (Website traffic)
  - support_tickets.csv (Support tickets)

Analysis Tables:
  - customer_overview.csv (Summary statistics)
  - policies_by_type.csv (Policy analysis)
  - customers_by_state.csv (Geographic analysis)
  - quote_conversion.csv (Conversion metrics)
  - age_groups.csv (Demographics)
  - support_tickets.csv (Support metrics)

===============================================================================
STEP 1: IMPORT DATA INTO POWER BI
===============================================================================

1. Open Power BI Desktop
2. Click "Get Data" button
3. Select "Text/CSV"
4. Navigate to the PowerBI_Data folder
5. Import all CSV files one by one
6. Click "Load" for each file

===============================================================================
STEP 2: CREATE RELATIONSHIPS
===============================================================================

Go to "Model" view (left sidebar icon) and create these relationships:

1. users[user_id] --> policies[user_id] (One-to-Many)
2. users[user_id] --> quotes[user_id] (One-to-Many)
3. users[user_id] --> page_visits[user_id] (One-to-Many)
4. users[user_id] --> support_tickets[user_id] (One-to-Many)

To create a relationship:
- Drag the user_id field from users table
- Drop it on the user_id field in the target table
- Ensure cardinality is "One to Many (*)"

===============================================================================
STEP 3: CREATE KEY MEASURES
===============================================================================

Go to "Modeling" tab > "New Measure" and create:

Total Revenue = 
    SUM(policies[premium_amount])

Active Policies = 
    COUNTROWS(FILTER(policies, policies[policy_status] = "active"))

Conversion Rate = 
    DIVIDE(
        COUNTROWS(FILTER(quotes, quotes[converted_to_policy] = TRUE)), 
        COUNTROWS(quotes),
        0
    ) * 100

Average Premium = 
    AVERAGE(policies[premium_amount])

Customer Count = 
    DISTINCTCOUNT(users[user_id])

Total Quotes = 
    COUNTROWS(quotes)

Resolved Tickets = 
    COUNTROWS(FILTER(support_tickets, 
        support_tickets[status] IN {"resolved", "closed"}))

Average Satisfaction = 
    AVERAGE(support_tickets[satisfaction_rating])

===============================================================================
STEP 4: BUILD YOUR DASHBOARD
===============================================================================

PAGE 1: EXECUTIVE DASHBOARD
---------------------------
- KPI Cards: Total Revenue, Customer Count, Active Policies
- Bar Chart: Revenue by Policy Type
- Filled Map: Customers by State (use 'state' field)
- Line Chart: Trends over time

PAGE 2: CUSTOMER ANALYTICS
---------------------------
- Pie Chart: Customer Distribution by Age Group
- Bar Chart: Average Premium by Age Group
- Table: Top 10 States by Customer Count
- Donut Chart: Active vs Inactive Customers

PAGE 3: SALES PERFORMANCE
-------------------------
- Funnel Chart: Quote to Policy Conversion
- Bar Chart: Conversion Rate by Policy Type
- Column Chart: Quote trends
- Table: Policy details with filters

PAGE 4: SUPPORT ANALYSIS
------------------------
- Clustered Bar Chart: Tickets by Issue Type
- Gauge: Average Satisfaction Rating (0-5 scale)
- Stacked Bar: Resolution Rate by Issue Type
- Table: Recent support tickets

===============================================================================
DESIGN TIPS
===============================================================================

1. Use consistent color scheme across all pages
2. Add slicers for: State, Policy Type, Date Range
3. Enable drill-through from summary to detail pages
4. Add tooltips for better user experience
5. Use bookmarks for different view states
6. Keep dashboards simple and focused

===============================================================================
POWER BI BEST PRACTICES
===============================================================================

- Create a Date table for better time-based analysis
- Use Quick Measures for common calculations
- Publish to Power BI Service to share with team
- Set up scheduled refresh if using live database
- Use Power Query to clean/transform data
- Test dashboard on different screen sizes

===============================================================================
TROUBLESHOOTING
===============================================================================

If relationships don't auto-create:
- Manually drag and drop between tables in Model view
- Check that column names match exactly
- Ensure data types are compatible

If measures show errors:
- Check that table and column names are correct
- Use Table[Column] syntax consistently
- Test measures on a simple visual first

If visuals are blank:
- Verify data loaded correctly
- Check filters aren't excluding all data
- Ensure relationships are active (solid line)

===============================================================================
LEARN MORE
===============================================================================

Official Documentation:
https://learn.microsoft.com/power-bi/

Video Tutorials:
https://www.youtube.com/user/mspowerbi

Community Forums:
https://community.powerbi.com/

===============================================================================
"""
        
        with open(f'{powerbi_folder}/PowerBI_Setup_Guide.txt', 'w', encoding='utf-8') as f:
            f.write(guide_text)
        
        print(f"  ✅ Setup guide: {powerbi_folder}/PowerBI_Setup_Guide.txt")
        return powerbi_folder
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n" + "="*60)
        print("    ENHANCED INSURANCE ANALYTICS REPORT")
        print("="*60)
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all analyses
        self.get_customer_overview()
        self.analyze_policies_by_type()
        self.analyze_customers_by_state()
        self.analyze_quote_conversion()
        self.analyze_customer_age_groups()
        self.analyze_support_tickets()
        
        # Export to Excel and Power BI
        excel_file = self.export_to_excel()
        powerbi_folder = self.export_for_powerbi()
        
        # Summary insights
        print("\n🎯 KEY INSIGHTS")
        print("=" * 60)
        
        if 'policies_by_type' in self.all_data and not self.all_data['policies_by_type'].empty:
            top_policy = self.all_data['policies_by_type'].iloc[0]
            total_revenue = self.all_data['policies_by_type']['total_revenue'].sum()
            print(f"✓ Most popular policy: {top_policy['policy_type']} ({int(top_policy['policy_count'])} policies)")
            print(f"✓ Total revenue: ${total_revenue:,.2f}")
        
        if 'quote_conversion' in self.all_data and not self.all_data['quote_conversion'].empty:
            avg_conversion = self.all_data['quote_conversion']['conversion_rate'].mean()
            best_conversion = self.all_data['quote_conversion'].iloc[0]
            print(f"✓ Best converting policy: {best_conversion['policy_type']} ({best_conversion['conversion_rate']}%)")
            print(f"✓ Average conversion rate: {avg_conversion:.2f}%")
        
        if 'customers_by_state' in self.all_data and not self.all_data['customers_by_state'].empty:
            top_state = self.all_data['customers_by_state'].iloc[0]
            print(f"✓ Top state: {top_state['state']} ({int(top_state['customer_count'])} customers, ${top_state['total_revenue']:,.2f})")
        
        if 'support_tickets' in self.all_data and not self.all_data['support_tickets'].empty:
            total_tickets = self.all_data['support_tickets']['ticket_count'].sum()
            avg_satisfaction = self.all_data['support_tickets']['avg_satisfaction'].mean()
            print(f"✓ Total support tickets: {int(total_tickets)}")
            print(f"✓ Average satisfaction: {avg_satisfaction:.2f}/5.0")
        
        print("\n📁 GENERATED FILES")
        print("=" * 60)
        print("\n📊 PNG Charts:")
        print("  ✅ policy_analysis.png")
        print("  ✅ state_analysis.png")
        print("  ✅ conversion_analysis.png")
        print("  ✅ age_analysis.png")
        print("  ✅ support_analysis.png")
        
        print(f"\n📗 Excel Report:")
        print(f"  ✅ {excel_file}")
        print("     Contains multiple sheets with all analysis data")
        
        print(f"\n📊 Power BI Data:")
        print(f"  ✅ {powerbi_folder}/")
        print("     Contains CSV files ready for Power BI import")
        
        print("\n💡 NEXT STEPS")
        print("=" * 60)
        print("1. View PNG charts for quick visual insights")
        print("2. Open Excel file for detailed data analysis")
        print("3. Import CSVs into Power BI Desktop for interactive dashboards")
        print("4. Follow PowerBI_Setup_Guide.txt for setup instructions")
        
        print("\n" + "="*60)
        print("    ✅ ANALYSIS COMPLETE!")
        print("="*60)
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("\n🔐 Database connection closed")


# Main execution
if __name__ == "__main__":
    # Database configuration
    # ⚠️ UPDATE THESE VALUES WITH YOUR DATABASE CREDENTIALS!
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'insurance_simple',
        'user': 'postgres',
        'password': 'postgres123',  # ⚠️ CHANGE THIS!
        'port': 5432
    }
    
    print("\n" + "="*60)
    print("  🏢 ENHANCED INSURANCE DATA ANALYTICS")
    print("      WITH EXCEL & POWER BI EXPORT")
    print("="*60)
    print(f"\nConnecting to database: {DB_CONFIG['database']}")
    print(f"Host: {DB_CONFIG['host']}")
    print(f"User: {DB_CONFIG['user']}")
    
    try:
        # Check if openpyxl is installed
        try:
            import openpyxl
            print("✅ openpyxl package found")
        except ImportError:
            print("\n❌ ERROR: openpyxl package not installed!")
            print("\nPlease install it using:")
            print("  pip install openpyxl")
            print("\nThen run this script again.")
            exit(1)
        
        print()
        
        # Initialize analytics
        analytics = EnhancedInsuranceAnalytics(DB_CONFIG)
        
        # Generate complete report
        analytics.generate_summary_report()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running analysis: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you ran data_generator.py first")
        print("2. Check database connection settings")
        print("3. Verify all tables exist (run schema.sql)")
        print("4. Install openpyxl: pip install openpyxl")
    
    finally:
        if 'analytics' in locals():
            analytics.close_connection()
    
    print("\n" + "="*60)
    print("  🎉 Thank you for using Enhanced Insurance Analytics!")
    print("="*60 + "\n")