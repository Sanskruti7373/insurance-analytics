"""
Simple Sample Data Generator for Insurance Analytics
Creates realistic but simple test data

Save this as: data_generator.py
"""

import psycopg2
import random
from datetime import datetime, timedelta
from faker import Faker
import sys

# Initialize Faker for generating realistic data
fake = Faker('en_US')

class SimpleDataGenerator:
    """Generate simple sample data for insurance analytics"""
    
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.connect_to_database()
        
        # US states for realistic data
        self.states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI', 
                      'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']
        
        self.policy_types = ['auto', 'home', 'life', 'health']
        self.issue_types = ['billing', 'claims', 'technical', 'general']
        self.device_types = ['desktop', 'mobile', 'tablet']
        self.traffic_sources = ['google', 'facebook', 'direct', 'email', 'referral']
        self.page_names = ['home', 'quote', 'about', 'contact', 'login', 'dashboard']
    
    def connect_to_database(self):
        """Connect to database"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print("✅ Connected to database")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            sys.exit(1)
    
    def generate_users(self, count=500):
        """Generate sample users"""
        print(f"📊 Generating {count} users...")
        
        cursor = self.connection.cursor()
        
        for i in range(count):
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            state = random.choice(self.states)
            age = random.randint(18, 75)
            registration_date = fake.date_between(start_date='-2y', end_date='today')
            is_active = random.choice([True, True, True, False])  # 75% active
            
            cursor.execute("""
                INSERT INTO users (email, first_name, last_name, state, age, registration_date, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (email, first_name, last_name, state, age, registration_date, is_active))
            
            if (i + 1) % 100 == 0:
                print(f"  • Generated {i + 1} users")
        
        self.connection.commit()
        cursor.close()
        print(f"✅ Generated {count} users")
    
    def generate_policies(self, count=800):
        """Generate insurance policies"""
        print(f"📋 Generating {count} policies...")
        
        cursor = self.connection.cursor()
        
        # Get user IDs
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        for i in range(count):
            user_id = random.choice(user_ids)
            policy_type = random.choice(self.policy_types)
            
            # Set realistic premium ranges by policy type
            if policy_type == 'auto':
                premium = round(random.uniform(800, 2500), 2)
                coverage = round(premium * random.uniform(15, 40), 2)
            elif policy_type == 'home':
                premium = round(random.uniform(1000, 3500), 2)
                coverage = round(premium * random.uniform(50, 150), 2)
            elif policy_type == 'life':
                premium = round(random.uniform(300, 1500), 2)
                coverage = round(premium * random.uniform(50, 200), 2)
            else:  # health
                premium = round(random.uniform(2000, 6000), 2)
                coverage = round(premium * random.uniform(10, 30), 2)
            
            policy_status = random.choices(['active', 'cancelled', 'expired'], 
                                         weights=[85, 10, 5])[0]
            start_date = fake.date_between(start_date='-1y', end_date='today')
            
            cursor.execute("""
                INSERT INTO policies (user_id, policy_type, premium_amount, coverage_amount, 
                                    policy_status, start_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, policy_type, premium, coverage, policy_status, start_date))
            
            if (i + 1) % 200 == 0:
                print(f"  • Generated {i + 1} policies")
        
        self.connection.commit()
        cursor.close()
        print(f"✅ Generated {count} policies")
    
    def generate_page_visits(self, count=2000):
        """Generate website page visits"""
        print(f"🌐 Generating {count} page visits...")
        
        cursor = self.connection.cursor()
        
        # Get user IDs
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        for i in range(count):
            # 20% anonymous visits (no user_id)
            user_id = random.choice(user_ids) if random.random() > 0.2 else None
            page_name = random.choice(self.page_names)
            visit_date = fake.date_between(start_date='-90d', end_date='today')
            visit_time = fake.date_time_between(start_date='-90d', end_date='now')
            time_on_page = random.randint(30, 600)  # 30 seconds to 10 minutes
            device_type = random.choice(self.device_types)
            traffic_source = random.choice(self.traffic_sources)
            
            cursor.execute("""
                INSERT INTO page_visits (user_id, page_name, visit_date, visit_time, 
                                       time_on_page, device_type, traffic_source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, page_name, visit_date, visit_time, time_on_page, 
                  device_type, traffic_source))
            
            if (i + 1) % 500 == 0:
                print(f"  • Generated {i + 1} page visits")
        
        self.connection.commit()
        cursor.close()
        print(f"✅ Generated {count} page visits")
    
    def generate_quotes(self, count=600):
        """Generate quote requests"""
        print(f"💰 Generating {count} quotes...")
        
        cursor = self.connection.cursor()
        
        # Get user IDs
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        for i in range(count):
            user_id = random.choice(user_ids)
            policy_type = random.choice(self.policy_types)
            
            # Set realistic coverage and premium amounts
            if policy_type == 'auto':
                coverage = random.randint(25000, 100000)
                premium = round(coverage * random.uniform(0.015, 0.035), 2)
            elif policy_type == 'home':
                coverage = random.randint(200000, 800000)
                premium = round(coverage * random.uniform(0.003, 0.008), 2)
            elif policy_type == 'life':
                coverage = random.randint(50000, 500000)
                premium = round(coverage * random.uniform(0.005, 0.015), 2)
            else:  # health
                coverage = random.randint(50000, 200000)
                premium = round(coverage * random.uniform(0.02, 0.06), 2)
            
            quote_date = fake.date_between(start_date='-90d', end_date='today')
            
            # 20% conversion rate
            converted = random.random() < 0.20
            conversion_date = None
            if converted:
                conversion_date = quote_date + timedelta(days=random.randint(1, 30))
            
            cursor.execute("""
                INSERT INTO quotes (user_id, policy_type, requested_coverage, quoted_premium,
                                  quote_date, converted_to_policy, conversion_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, policy_type, coverage, premium, quote_date, converted, conversion_date))
            
            if (i + 1) % 150 == 0:
                print(f"  • Generated {i + 1} quotes")
        
        self.connection.commit()
        cursor.close()
        print(f"✅ Generated {count} quotes")
    
    def generate_support_tickets(self, count=200):
        """Generate customer support tickets"""
        print(f"🎧 Generating {count} support tickets...")
        
        cursor = self.connection.cursor()
        
        # Get user IDs
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        for i in range(count):
            user_id = random.choice(user_ids)
            issue_type = random.choice(self.issue_types)
            priority = random.choices(['low', 'medium', 'high'], weights=[50, 35, 15])[0]
            status = random.choices(['open', 'in_progress', 'resolved', 'closed'], 
                                  weights=[15, 25, 45, 15])[0]
            created_date = fake.date_between(start_date='-60d', end_date='today')
            
            resolved_date = None
            satisfaction_rating = None
            
            if status in ['resolved', 'closed']:
                resolved_date = created_date + timedelta(days=random.randint(1, 14))
                satisfaction_rating = random.randint(1, 5)
            
            cursor.execute("""
                INSERT INTO support_tickets (user_id, issue_type, priority, status, 
                                           created_date, resolved_date, satisfaction_rating)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, issue_type, priority, status, created_date, 
                  resolved_date, satisfaction_rating))
            
            if (i + 1) % 50 == 0:
                print(f"  • Generated {i + 1} support tickets")
        
        self.connection.commit()
        cursor.close()
        print(f"✅ Generated {count} support tickets")
    
    def generate_all_data(self):
        """Generate all sample data"""
        print("\n" + "="*50)
        print("  INSURANCE ANALYTICS - DATA GENERATION")
        print("="*50 + "\n")
        
        self.generate_users(500)
        self.generate_policies(800)
        self.generate_page_visits(2000)
        self.generate_quotes(600)
        self.generate_support_tickets(200)
        
        print("\n" + "="*50)
        print("  ✅ DATA GENERATION COMPLETE!")
        print("="*50)
        print("\n📊 Summary:")
        print("  • 500 users")
        print("  • 800 insurance policies")
        print("  • 2,000 page visits")
        print("  • 600 quote requests")
        print("  • 200 support tickets")
        print("\n🎉 Your database is now ready for analysis!")
    
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
    
    print("\n" + "="*50)
    print("  🚀 Starting Data Generation")
    print("="*50)
    print(f"\nConnecting to database: {DB_CONFIG['database']}")
    print(f"Host: {DB_CONFIG['host']}")
    print(f"User: {DB_CONFIG['user']}\n")
    
    try:
        generator = SimpleDataGenerator(DB_CONFIG)
        generator.generate_all_data()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your database password in DB_CONFIG")
        print("2. Make sure PostgreSQL is running")
        print("3. Verify database 'insurance_simple' exists")
        print("4. Run the schema.sql file first to create tables")
    
    finally:
        if 'generator' in locals():
            generator.close_connection()
    
    print("\n" + "="*50)
    print("  Script completed!")
    print("="*50 + "\n")