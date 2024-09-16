import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Content, Part
from typing import List
import sqlite3
import pandas as pd

# Function to check login credentials
def verify_credentials(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Login page
def login():
    # Create the users table with default credentials
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if verify_credentials(username, password):
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid username or password")

def home():
    # Setup the navbar
    st.set_page_config(layout="wide")
    navbar = st.container()
    # Place the logout button in the navbar
    with navbar:
        col1, col2 = st.columns([9, 1])
        with col1:
            st.title("SQL Bot")
        with col2:
            if st.button("Logout"):
                st.session_state["logged_in"] = False
                st.session_state.messages = []
                st.rerun()

    # initialise chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["parts"])

    # Connect to sales database and show output
    def read_sql_query(sql, database):
        conn = sqlite3.connect(database)
        data = pd.read_sql_query(sql, conn)
        conn.close()
        return data


    # Description of the database
    description = """The SQL database has the name sales and represents the company information system for a insurance company.
    It uses five interconnected tables to manage agents(employees), their sales, monthly target, customer feedback and commissions.
    The AGENTS table stores information about the agents in the company, including a unique identifier (AGENT_ID),
    agent name (AGENT_NAME), state where the policy was issued which is a two letter code for the state name (POLICY_ISSUING_STATE), and the policy number (POLICY_NUMBER).
    It uses foreign key: POLICY_NUMBER referencing the COMMISSIONS table.
    The SALES table stores information such as SalesId (SALES_ID), (AGENT_ID),
    policy number (POLICY_NUMBER) and the billing frequency (BILLING_FREQUENCY), the type of billing it was (BILLING_OPTION),
    the date the policy was issued (POLICY_ISSUE_DATE), Amount the product has been sold by the agent (PREMIUM_AMOUNT).
    It also uses foreign key: POLICY_NUMBER referencing the COMMISSIONS table.
    The COMMISSIONS table has information about the commissions for the agents with the type of policy it was (PRODUCT), policy number (POLICY_NUMBER),
    and the commission amount (COMM_AMOUNT).
    The MONTHLY_TARGETS table has information about the monthy tagets to be acheived by the agents this table contains agentId (AGENT_ID) , month (MONTH), target to be acheived (TARGET_AMOUNT),
    It uses foreign key: AGENT_ID referencing the AGENTS table.
    The CUSTOMER_FEEDBACK table stores information about agents performance  such as Agentid (AGENT_ID),
    CUSTOMER Id (CUSTOMER_ID) and the feedback provided by the customer for an agent (FEEDBACK), also the rating provided by customer based on the service  (RATING).
    AGENTS and SALES tables are related to the COMMISSIONS table through the POLICY_NUMBER foreign key.
    This structure indicates that one policy (identified by POLICY_NUMBER) can have  multiple sales details, and is associated with an agent."""

    history: List[Content] = [
        Content(role=message["role"], parts=[Part.from_text(message["parts"])])
        for message in st.session_state.messages
    ]

    vertexai.init(project="cog01j3qdy6xns3g9fzvsjz14by1v", location="asia-south1")
    model = GenerativeModel("gemini-1.5-pro-001")
    chat=model.start_chat(history=history)

    prompt = st.chat_input("Enter prompt here")
    if prompt:
        # display user message
        with st.chat_message(name="user"):
            st.markdown(prompt)
        # add user message to chat history
        st.session_state.messages.append({"role":"user", "parts":prompt})

        # Instructions for AI to check database connectivty required or not
        instructions=f"""You are an expert in converting English questions to 'True' or 'False' answers being 
        part of a chatbot capable of providing information on a wide range of topics, enhanced by direct access to a specific SQL database.
        {description}
        \n\nFor example, \nExample 1 - Hello there! 
        The output will be 'False'
        \n Example 2 - Can you help in figuring out which employee made the highest in commisions this year?,
        the output will be 'True'
        \n Example 3 Calculate the average commission percentage for each product type, 
        the output will be 'True'
        Provide only sinlge word outputs 'True' if connection to the database is needed and 'False' if it is not needed.
        Make sure the output does not have ``` or ' in beginning or end.
        """

        # checking to see if database will be needed or not
        # if yes then extract necessary data from database and attaching it as part of the question
        check=model.generate_content([instructions, prompt]).text
        print(check)
        if eval(check):
            instructions=f"""You are an expert in converting English questions to SQL query.
            {description}
            \n\nFor example, \nExample 1 - Find the total commission earned by each agent. 
            The SQL command will be something like this SELECT a.AGENT_NAME, SUM(c.COMM_AMOUNT) AS TOTAL_COMMISSION
            FROM AGENTS a
            INNER JOIN COMMISSIONS c ON a.POLICY_NUMBER = c.POLICY_NUMBER
            GROUP BY a.AGENT_NAME;
            \n Example 2 - List all policies issued in California with an expected premium greater than $1000,
            the SQL command will be something like this SELECT s.POLICY_NUMBER, s.PRODUCT, s.EXPECTED_PREMIUM_AMOUNT
            FROM SALES s
            INNER JOIN AGENTS a ON s.POLICY_NUMBER = a.POLICY_NUMBER
            WHERE a.POLICY_ISSUING_STATE = 'CA' AND s.EXPECTED_PREMIUM_AMOUNT > 1000;
            \n Example 3 Calculate the average commission percentage for each product type, 
            the SQL command will be something like this SELECT s.PRODUCT, AVG(c.COMM_PERCENT) AS AVERAGE_COMMISSION_PERCENT
            FROM SALES s
            INNER JOIN COMMISSIONS c ON s.POLICY_NUMBER = c.POLICY_NUMBER
            GROUP BY s.PRODUCT;
            \n Example 4 Find the top 5 agents by total commission earned, the SQL command will be something like this
            SELECT a.AGENT_NAME, SUM(c.COMM_AMOUNT) AS TOTAL_COMMISSION
            FROM AGENTS a
            INNER JOIN COMMISSIONS c ON a.POLICY_NUMBER = c.POLICY_NUMBER
            GROUP BY a.AGENT_NAME
            ORDER BY TOTAL_COMMISSION DESC
            LIMIT 5;
            \n Example 5 List all policies with a chargeback and the corresponding agent, the SQL command will be something like this
            SELECT c.POLICY_NUMBER, a.AGENT_NAME, c.CHARGEBACK_CODE
            FROM COMMISSIONS c
            INNER JOIN AGENTS a ON c.POLICY_NUMBER = a.POLICY_NUMBER
            WHERE c.CHARGEBACK_CODE IS NOT NULL;
            \n Example 7 - Where does a agent does his business or which location he is from. 
            SELECT AGENT_ID, AGENT_NAME, POLICY_ISSUING_STATE
            FROM AGENTS;
            \n Example 8 - Find the top performing agents based on targets acheived.
            SELECT a.agent_id,a.agent_name,t.TARGET_AMOUNT,SUM(s.PREMIUM_AMOUNT) AS total_sales_amount,(SUM(s.PREMIUM_AMOUNT) / t.TARGET_AMOUNT) * 100 AS achieved amount
            FROM agents a
            JOIN MONTHLY_TARGETS t ON a.agent_id = t.agent_id
            JOIN sales s ON a.agent_id = s.agent_id
            WHERE a.agent_name = 'agent_name'
            GROUP BY a.agent_id, a.agent_name, t.TARGET_AMOUNT;
            \n Example 9 - How good is the agent relationship with customer.
            SELECT AVG(RATING) AS average_rating
            FROM Customer_Feedback_Details
            WHERE AGENT_ID = '101';
            The SQL code should not have ``` or the word sql in beginning or end of sql in output also no further explanation of the code"""

            print("Needed connection")
            # creating the query
            code=model.generate_content([instructions, prompt]).text
            print(code)
            query=code.strip("`sql")
            print(query)
            # running the query
            db_path="sales.db"
            data = read_sql_query(query, db_path)

            # final prompt generated to send chatbot
            data=data.to_csv()
            explainer="""\nAttaching the necessary data from the company SQL database.
            More data does exist and the user can see it if they want and they just need to ask.
            Make additional comments if applicable. Do not ask for any context or additional data, answer with whatever knowledge you have.
            There is more data and you do not have access to it for security reasons.
            Although if there is no data with what I'm providing it means there is no data with reference to the question asked by the user.
            Do not make up data\n"""
            prompt=prompt+explainer+data
            print(prompt)
            response=chat.send_message(prompt).text

        # otherwise no changes are made and the question is answered as is
        else:
            print("Not needed")
            response=chat.send_message(prompt).text

        # display bot messages
        with st.chat_message(name="Bot"):
            st.markdown(response)
        # add bot response to chat history
        st.session_state.messages.append({"role":"model", "parts":response})
        print(st.session_state.messages)

# Main function
def main():
    home()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        home()
    else:
        login()

if __name__ == '__main__':
    main()
