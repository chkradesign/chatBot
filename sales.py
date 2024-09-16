import sqlite3

# Connect to sqlite
connection = sqlite3.connect("sales.db")

# Create a cursor object
cursor = connection.cursor()

# Drop existing tables if they exist
cursor.execute('DROP TABLE IF EXISTS COMMISSIONS')
cursor.execute('DROP TABLE IF EXISTS AGENTS')
cursor.execute('DROP TABLE IF EXISTS SALES')
cursor.execute('DROP TABLE IF EXISTS MONTHLY_TARGETS')
cursor.execute('DROP TABLE IF EXISTS CUSTOMER_FEEDBACK')

# Create COMMISSIONS table
cursor.execute('''CREATE TABLE COMMISSIONS (
    PRODUCT VARCHAR(20),
    POLICY_NUMBER INT PRIMARY KEY,
    COMM_AMOUNT DECIMAL(10,2)
);''')

# Create AGENTS table
cursor.execute('''CREATE TABLE AGENTS (
    AGENT_ID INT PRIMARY KEY,
    AGENT_NAME VARCHAR(255),
    POLICY_ISSUING_STATE VARCHAR(2)
   
);''')

# Create SALES table
cursor.execute('''CREATE TABLE SALES (
    SALE_ID VARCHAR(20),
    AGENT_ID INT,
    POLICY_NUMBER INT,
    BILLING_FREQUENCY VARCHAR(20),
    BILLING_OPTION VARCHAR(20),
    POLICY_ISSUE_DATE DATE,
    PRODUCT VARCHAR(50),
    PREMIUM_AMOUNT DECIMAL(10,2),
    FOREIGN KEY (POLICY_NUMBER) REFERENCES COMMISSIONS(POLICY_NUMBER)
);''')

#CREATE MONTHLY_TARGETS TABLE 
cursor.execute('''CREATE TABLE MONTHLY_TARGETS (
    AGENT_ID INT,
    MONTH VARCHAR(20),
    TARGET_AMOUNT DECIMAL(10,2),
    FOREIGN KEY (AGENT_ID) REFERENCES AGENTS(AGENT_ID)
);''')

#CREATE CUSTOMER_FEEDBACK TABLE 
cursor.execute('''CREATE TABLE CUSTOMER_FEEDBACK (
    AGENT_ID INT,
    CUSTOMER_ID INT,
    FEEDBACK VARCHAR(255),
    RATING INT,
    FOREIGN KEY (AGENT_ID) REFERENCES AGENTS(AGENT_ID)
);''')

# COMMISSIONS table details
Commissions_Details = [
    ("Universal Life Insurance", 1001, 500.00),
    ("Whole Life Insurance", 1002, 250.00),
    ("Term Life Insurance", 1003, 1000.00)
]

# Insert the rows into the COMMISSIONS table
cursor.executemany("INSERT INTO COMMISSIONS (PRODUCT, POLICY_NUMBER, COMM_AMOUNT) VALUES (?, ?, ?)", Commissions_Details)

# Define the Agent_Details to be inserted
Agent_Details = [
    (101, "John Doe", "CA"),
    (102, "Jane Smith", "NY"),
    (103, "Alex Brown", "TX"),
    (104, "Emily Davis", "FL"),
    (105, "Michael Johnson", "CA"),
    (106, "Sarah Miller", "NY"),
    (107, "David Wilson", "TX"),
    (108, "Olivia Carter", "FL"),
    (109, "William Anderson", "CA"),
    (110, "Jennifer Lopez", "NY"),
    (111, "Matthew Lee", "TX"),
    (112, "Ava Miller", "FL"),
    (113, "Christopher Evans", "CA"),
    (114, "Sophia Rodriguez", "NY"),
    (115, "Daniel Brown", "TX"),
    (116, "Isabella Johnson", "FL"),
    (117, "Ethan Davis", "CA"),
    (118, "Mia Miller", "NY"),
    (119, "Jacob Wilson", "TX"),
    (120, "Charlotte Carter", "FL")
]

# Insert the rows into the AGENTS table
cursor.executemany("INSERT INTO AGENTS (AGENT_ID, AGENT_NAME, POLICY_ISSUING_STATE) VALUES (?, ?, ?)", Agent_Details)

# Define the Sales_Details to be inserted
Sales_Details = [
    ( "S001", 101, 1003, "Annual", "Credit Card", "2024-01-01", 10000.00),
    ( "S002", 102, 1002, "Monthly", "Credit Card", "2024-01-01", 30000.00),
    ( "S003", 103, 1001, "Quarterly", "Credit Card", "2024-01-01", 50000),
    ( "S004", 104, 1002, "Annual", "Bank Draft", "2024-03-15", 20000),
    ( "S005", 105, 1002, "Monthly", "Credit Card", "2024-01-01",  10000),
    ( "S006", 106, 1003, "Monthly", "Credit Card", "2024-01-01", 51000),
    ( "S007", 107, 1002, "Annual", "Bank Draft", "2024-03-15",  20000),
    ( "S008", 108, 1003, "Quarterly", "Credit Card", "2024-01-01", 10000),
    ( "S009", 109, 1002, "Annual", "Bank Draft", "2024-03-15",  24000),
    ( "S010", 111, 1003, "Annual", "Credit Card", "2024-01-01",  10000),
    ( "S011", 112, 1002, "Monthly", "Credit Card", "2024-01-01",  30000),
    ( "S012", 113, 1003, "Quarterly", "Credit Card", "2024-01-01",  50000),
    ( "S013", 114, 1002, "Annual", "Bank Draft", "2024-03-15",  20000),
    ( "S014", 115, 1002, "Monthly", "Credit Card", "2024-01-01",  10000),
    ( "S015", 116, 1003, "Monthly", "Credit Card", "2024-01-01", 51000),
    ( "S016", 101, 1002, "Annual", "Bank Draft", "2024-03-15",  20000),
    ( "S017", 101, 1003, "Quarterly", "Credit Card", "2024-01-01",  10000),
    ( "S018", 101, 1002, "Annual", "Bank Draft", "2024-03-15", 24000),  
    ( "S019", 101, 1003, "Annual", "Credit Card", "2024-01-01",  10000),
    ( "S020", 102, 1002, "Monthly", "Credit Card", "2024-01-01", 30000),
    ( "S021", 103, 1003, "Quarterly", "Credit Card", "2024-01-01", 50000),
    ( "S022", 104, 1002, "Annual", "Bank Draft", "2024-03-15",  20000),
    ( "S023", 105, 1002, "Monthly", "Credit Card", "2024-01-01", 10000),
    ( "S024", 106, 1003, "Monthly", "Credit Card", "2024-01-01",  51000),
    ( "S025", 107, 1002, "Annual", "Bank Draft", "2024-03-15",  20000),
    ( "S026", 108, 1003, "Quarterly", "Credit Card", "2024-01-01",  10000),
    ( "S027", 108, 1002, "Annual", "Bank Draft", "2024-03-15", 24000),
    ( "S028", 111, 1003, "Annual", "Credit Card", "2024-01-01",  10000),
    ( "S029", 114, 1002, "Monthly", "Credit Card", "2024-01-01", 30000),
    ( "S030", 117, 1003, "Quarterly", "Credit Card", "2024-01-01",  50000),
    ( "S031", 116, 1002, "Annual", "Bank Draft", "2024-03-15",  20000),
    ( "S032", 115, 1002, "Monthly", "Credit Card", "2024-01-01",  10000),
    ( "S033", 116, 1003, "Monthly", "Credit Card", "2024-01-01", 51000),
    ( "S034", 105, 1002, "Annual", "Bank Draft", "2024-03-15", 20000),
    ( "S035", 105, 1003, "Quarterly", "Credit Card", "2024-01-01", 10000),
    ( "S036", 101, 1002, "Annual", "Bank Draft", "2024-03-15",  24000),
    ( "S037", 101, 1003, "Annual", "Credit Card", "2024-01-01", 10000),
    ( "S038", 102, 1002, "Monthly", "Credit Card", "2024-01-01",30000),
    ( "S039", 103, 1003, "Quarterly", "Credit Card", "2024-01-01", 5000),
    ( "S040", 104, 1002, "Annual", "Bank Draft", "2024-03-15", 20000),
    ( "S041", 109, 1002, "Monthly", "Credit Card", "2024-01-01", 10000),
    ( "S042", 106, 1003, "Monthly", "Credit Card", "2024-01-01",  51000),
    ( "S043", 107, 1002, "Annual", "Bank Draft", "2024-03-15", 20000),
    ( "S044", 108, 1003, "Quarterly", "Credit Card", "2024-01-01", 10000),
    ( "S045", 109, 1002, "Annual", "Bank Draft", "2024-03-15",  240000),
    ( "S046", 111, 1003, "Annual", "Credit Card", "2024-01-01",  10000),
    ( "S047", 120, 1002, "Monthly", "Credit Card", "2024-01-01", 30000),
    ( "S048", 115, 1003, "Quarterly", "Credit Card", "2024-01-01",50000),
    ( "S049", 103, 1002, "Annual", "Bank Draft", "2024-03-15", 20000),
    ( "S050", 115, 1002, "Monthly", "Credit Card", "2024-01-01", 10000),
    ( "S051", 106, 1003, "Monthly", "Credit Card", "2024-01-01",  51000),
    ( "S052", 120, 1002, "Annual", "Bank Draft", "2024-03-15", 20000),
    ( "S053", 101, 1003, "Quarterly", "Credit Card", "2024-01-01",  10000),
    ( "S054", 120, 1002, "Annual", "Bank Draft", "2024-03-15",  24000),  
]

# Insert the rows into the SALES table
cursor.executemany("INSERT INTO SALES (SALE_ID,AGENT_ID,POLICY_NUMBER, BILLING_FREQUENCY, BILLING_OPTION, POLICY_ISSUE_DATE, PREMIUM_AMOUNT) VALUES (?, ?, ?, ?, ?, ?, ?)", Sales_Details)

Monthly_Targets_Details = [
    (101, 'January', 100000.00),
    (102, 'February', 100000.00),
    (103, 'March', 100000.00),
    (104, 'January', 90000.00),
    (105, 'February', 90000.00),
    (106, 'March', 90000.00),
    (107, 'January', 80000.00),
    (108, 'February', 80000.00),
    (109, 'March', 80000.00),
    (110, 'January', 110000.00),
    (111, 'February', 110000.00),
    (112, 'March', 110000.00)
]

cursor.executemany("INSERT INTO MONTHLY_TARGETS (AGENT_ID, MONTH, TARGET_AMOUNT) VALUES (?, ?, ?)", Monthly_Targets_Details)

Customer_Feedback_Details = [
    (101, 10011, 'Very helpful and knowledgeable. Helped me choose the best policy.', 5),
    (102, 10012, 'Good service but response time could be improved.', 4),
    (103, 10013, 'Friendly and professional. Explained all details clearly.', 5),
    (104, 10014, 'Satisfactory service but faced some delays in processing.', 3),
    (105, 10015, 'Excellent service. Very patient and answered all my questions.', 5),
    (106, 10016, 'Good experience overall. Would recommend to others.', 4),
    (107, 10017, 'Average service. Could improve on communication.', 3),
    (108, 10018, 'Very efficient and quick. Made the process very easy for me.', 5),
    (109, 10011, 'Very helpful and knowledgeable. Helped me choose the best policy.', 5),
    (110, 10012, 'Good service but response time could be improved.', 4),
    (111, 10013, 'Friendly and professional. Explained all details clearly.', 5),
    (112, 10014, 'Satisfactory service but faced some delays in processing.', 3),
    (113, 10015, 'Excellent service. Very patient and answered all my questions.', 5),
    (114, 10016, 'Good experience overall. Would recommend to others.', 4),
    (115, 10017, 'Average service. Could improve on communication.', 3),
    (116, 10018, 'Very efficient and quick. Made the process very easy for me.', 5),
    (117, 10011, 'Very helpful and knowledgeable. Helped me choose the best policy.', 5),
    (118, 10012, 'Good service but response time could be improved.', 4),
    (119, 10013, 'Friendly and professional. Explained all details clearly.', 5),
    (120, 10041, 'Satisfactory service but faced some delays in processing.', 3),
]

cursor.executemany("INSERT INTO CUSTOMER_FEEDBACK (AGENT_ID, CUSTOMER_ID, FEEDBACK, RATING) VALUES (?, ?, ?, ?)", Customer_Feedback_Details)

print("Database schema created successfully!")

# # Save changes and close connection
connection.commit()
connection.close()
