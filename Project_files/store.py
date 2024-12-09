from dotenv import load_dotenv
load_dotenv(dotenv_path='.flaskenv')
from app import app

if __name__ == '__main__':
    app.run()