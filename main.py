from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """
    Hi World
    """
    return {"message": "Hello World"}


@app.get("/users")
def get_users():
    """
    Get a single users

    """
    return {"message": "Get Users!"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Get a single user

    """
    return {"user": user_id}
