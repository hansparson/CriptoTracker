Cripto Tracker
OS : Ubuntu 21
Python : 3.8+
Database : SQLite3

Setup Virtual environtment (Ubuntu Terminal)
1. Create Virtual Environtment `python3 -m venv env`
2. Activate environtment  `source env/bin/activate`

Install Requirement
1. `pip install -r requirements.txt`

Setup Table for SQLite3
1. run the file revision 
    `alembic revision --autogenerate -m "message"`
2. run the migration file
    `alembic upgrade head`

Run App 
1. run `sh ./start-app.sh`
2. or `uvicorn main:app --reload`

Postman Collection for testing
`CriptoTracker.postman_collection`

Several problems were found in this development
1. I dont get any free API for convert value USD to IDR, so i use harcode on calculation
2. I always deploy with railways, google cloud vps, but my git account trial is expired. sorry i can't deploy the system.