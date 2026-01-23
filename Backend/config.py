import os
from dotenv import load_dotenv
load_dotenv()
# from groq import Groq


db_user = os.getenv("db_user")
db_pswd = os.getenv("db_pswd")
db_port = os.getenv("db_port", "5432") #Default port : 5432
db_name = os.getenv("db_name")
db_host = os.getenv("db_host","localhost")

base_url = f"postgresql://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_name}"

