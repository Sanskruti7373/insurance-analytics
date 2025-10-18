-- Drop tables if they exist (for clean reinstall)
DROP TABLE IF EXISTS support_tickets CASCADE;
DROP TABLE IF EXISTS quotes CASCADE;
DROP TABLE IF EXISTS page_visits CASCADE;
DROP TABLE IF EXISTS policies CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    state VARCHAR(2) NOT NULL,
    age INTEGER,
    registration_date DATE DEFAULT CURRENT_DATE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Policies table
CREATE TABLE policies (
    policy_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    policy_type VARCHAR(20) NOT NULL,
    premium_amount DECIMAL(8,2),
    coverage_amount DECIMAL(10,2),
    policy_status VARCHAR(20) DEFAULT 'active',
    start_date DATE,
    created_date DATE DEFAULT CURRENT_DATE
);

-- Page visits table
CREATE TABLE page_visits (
    visit_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    page_name VARCHAR(50) NOT NULL,
    visit_date DATE DEFAULT CURRENT_DATE,
    visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_on_page INTEGER,
    device_type VARCHAR(20),
    traffic_source VARCHAR(30)
);

-- Quotes table
CREATE TABLE quotes (
    quote_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    policy_type VARCHAR(20) NOT NULL,
    requested_coverage DECIMAL(10,2),
    quoted_premium DECIMAL(8,2),
    quote_date DATE DEFAULT CURRENT_DATE,
    converted_to_policy BOOLEAN DEFAULT FALSE,
    conversion_date DATE
);

-- Support tickets table
CREATE TABLE support_tickets (
    ticket_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    issue_type VARCHAR(30),
    priority VARCHAR(10),
    status VARCHAR(20) DEFAULT 'open',
    created_date DATE DEFAULT CURRENT_DATE,
    resolved_date DATE,
    satisfaction_rating INTEGER
);

-- Create indexes for better query performance
CREATE INDEX idx_users_state ON users(state);
CREATE INDEX idx_policies_type ON policies(policy_type);
CREATE INDEX idx_policies_user ON policies(user_id);
CREATE INDEX idx_page_visits_date ON page_visits(visit_date);
CREATE INDEX idx_quotes_date ON quotes(quote_date);
CREATE INDEX idx_quotes_user ON quotes(user_id);

-- Create useful views
CREATE VIEW customer_summary AS
SELECT 
    u.user_id,
    u.first_name || ' ' || u.last_name as full_name,
    u.state,
    u.age,
    COUNT(p.policy_id) as total_policies,
    COALESCE(SUM(p.premium_amount), 0) as total_premium,
    u.registration_date
FROM users u
LEFT JOIN policies p ON u.user_id = p.user_id
GROUP BY u.user_id, u.first_name, u.last_name, u.state, u.age, u.registration_date;

COMMENT ON TABLE users IS 'Customer information table';
COMMENT ON TABLE policies IS 'Insurance policies table';
COMMENT ON TABLE page_visits IS 'Website traffic tracking';
COMMENT ON TABLE quotes IS 'Insurance quote requests';
COMMENT ON TABLE support_tickets IS 'Customer support tickets';

-- Success message
SELECT 'Database schema created successfully!' as status;