from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(basedir, '.flaskenv'))

from app import app

if __name__ == '__main__':
    app.run()
