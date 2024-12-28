from dotenv import load_dotenv
import os
from app import app

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(basedir, '.flaskenv'))

if __name__ == '__main__':
    app.run()
