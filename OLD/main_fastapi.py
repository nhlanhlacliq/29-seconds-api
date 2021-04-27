from fastapi import FastAPI
import hypercorn

app = FastAPI()

db = []

@app.get('/')
def index():
    return db

app.run()
