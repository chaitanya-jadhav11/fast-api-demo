from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def greeting():
    print("Welcome to home page")
    return {"message": "Welcome to home page"}

