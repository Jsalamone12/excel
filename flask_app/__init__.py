import pandas as pd
from sqlalchemy import create_engine
from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
BCRYPT = Bcrypt(app)

app.secret_key = "rootroot"

DATABASE = "excel_db"