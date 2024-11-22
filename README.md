# trilpapi
Sample RESTful API with JWT using python and FastAPI, SQLAlchemy

## Development environment setup (MacBook)

1. git clone https://github.com/trilpai/trilpapi.git

2. cd trilpapi

3. git config --local user.name "your_github_username"

4. git config --local user.email "your_github_email"

5. python3 -m venv venv

6. source venv/bin/activate (macbook)
   - venv\Scripts\activate  (Windows cmd prompt)
   - .\venv\Scripts\Activate.ps1 (Windows powershell)

7. Command to come out of venv (you don't have to execute it now, it's just for knowledge)
    - deactivate

8. pip install --upgrade pip

9. pip install -r requirements.txt

Above 9 steps will create the development environment ready for dev/test.

## Run the Development environment

10. Create a MySQL DB by name trilpapi

11. Create a .env file and change the values of properties by copying the properties from trilpapi/envexample.txt into newly created .env

12. Create the DB tables and Seed Data
    - alembic upgrade head
    - alembic downgrade base (if you want to cleanup the DB fully)
    - alembic downgrade -1 (downgrade by 1 revision)
    - alembic downgrade 12345abcde (downgrade to a specific revision)

13. Run the development server
    - uvicorn src.main:app --reload

14. Test in Browser
    - http://localhost:8000/
    - you will see ->  {"message":"Welcome to Trilp API!"}

15. Opening Swagger UI
    - http://localhost:8000/docs

16. Opening Redoc Documentation
    - http://localhost:8000/redoc