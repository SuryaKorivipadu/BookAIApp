# BookAIApp
An AI backend app to manage book details, generate summaries and book recommendations
This application uses FASTAPI backend, Ollama Llama3.2 model and PostgreSQL


Steps to run the application:
1. Install PostgreSQL server in your machine.

2. Clone the repository using below command:
git clone https://github.com/SuryaKorivipadu/BookAIApp.git
 
3. Create a file named '.env' and place it in the project folder

4. Write the following details in .env file
Database_user=<Database username>
Database_password=<Database password>
Database_name=<Database name>
Database_host=<Database host>
Database_port=<Database port number>

5. Install the packages using below command:
pip install -r requirements.txt

6. Run the code using following command:
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8002

7. Open the API documentation swagger URL using below link and try the APIs:
http://localhost:8002/docs