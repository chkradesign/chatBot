## Streamlit Chatbot with SQL Database Access (using Gemini by Google)

**Introduction:**

This project provides a user-friendly chatbot interface built with Streamlit and leverages the power of Gemini, a large language model by Google, for natural language interactions. It allows users to connect and interact with a specified SQL database, empowering them to retrieve and potentially manipulate information.

**Features:**

- **Chatbot Interface:** Engage in interactive conversations with the chatbot using text input.
- **SQL Database Integration:** Connect to a specified SQL database to access and manage data.
- **User Login:** Added login functionality to restrict access to authorized users. (New)

**Getting Started:**

Before you begin, ensure you have Python and Git installed on your system.

1. **Clone the Repository:**
   Open a terminal or command prompt and navigate to your desired project directory. Then, run the following command to clone this repository from GitHub:

   ```bash
   git clone https://github.com/<your-username>/<your-repository-name>.git
   ```

   Replace `<your-username>` with your GitHub username and `<your-repository-name>` with the actual name of your repository.

2. **Create a Virtual Environment (Recommended):**
   - **Using `venv` (Python 3.3+):**
     ```bash
     cd <your-repository-name>
     python -m venv venv
     source venv/bin/activate  # Linux/macOS
     venv\Scripts\activate.bat  # Windows
     ```
   - **Using `conda` (if available):**
     ```bash
     conda create -p venv python=x.y.z  # Replace x.y.z with your desired Python version
     conda activate venv
     ```

3. **Install Dependencies:**
   Activate your virtual environment (if created). Then, install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database Connection (Optional):**
   - If you have a pre-existing SQL database:
     1. Modify the connection details in the variable `db_path` with your database path.
     2. Make sure your database server is accessible from your machine.
   - If you want to use the `sales.py` script for a sample database:
     Run `python sales.py` to create an example database within your project directory.

5. **Configure Google Cloud Project (New):**
   - Create a new Google Cloud project or use an existing one.
   - Enable the Vertex AI API for your project.
   - Set up authentication using Application Default Credentials:
     1. Install the Google Cloud SDK: `pip install google-cloud-sdk`
     2. Initialize the SDK: `gcloud init`
     3. Log in using Application Default Credentials: `gcloud auth application-default login`

6. **Run the Chatbot:**
   Start the Streamlit application:

   ```bash
   streamlit run app.py
   ```

   A browser window will open automatically, displaying the login page. (Changed from showing the chatbot interface directly)

**Using the Chatbot:**

1. Login using your registered username and password.
2. Interact with the chatbot by typing your questions or commands. The chatbot will leverage Gemini's capabilities to understand your intent and potentially access data from the connected database, if configured.

**Additional Notes:**

- For first-time users of Python, virtual environments are highly recommended to isolate project dependencies and avoid conflicts with other applications on your system.
- The `users.py` file contains sample credentials for testing purposes. You can modify it to add or remove users as needed.
- Refer to the Google Cloud documentation for more information on configuring Vertex AI and using Application Default Credentials.
