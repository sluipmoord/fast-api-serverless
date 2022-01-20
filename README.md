## Serverless demo with fast API

1 - Setup Virtual Environment and [pip tools](https://github.com/jazzband/pip-tools)

```bash
# Create virtual environment
$ python -m venv venv

# Activate virtual environment
$ . venv/bin/activate

# Install pip-tools for requirements management
$ python -m pip install pip-tools

# create requirements.in file in the root folder
$ touch requirements.in
```

2 - Install FAST API

```bash
# Add dependencies
$ echo "fastapi" >> requirements.in
$ echo "uvicorn[standard]" >> requirements.in

# Create requirements.txt from requirements.in
$ pip-compile

# install dependencies
$ pip install -r requirements.txt
```

3 - Write a Fast API

```bash
# Create main.py file in the root folder
$ touch main.py
```

```python
# main.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
  return {"message": "Hello World"}
```

```bash
# run the server
$ uvicorn main:app --reload

$ INFO:     Will watch for changes in these directories: ['/Users/sluipmoord/Development/Teamgeek/demoday/fast-api-serverless']
$ INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
$ INFO:     Started reloader process [60133] using watchgod

# Test the server
$ curl http://127.0.0.1:8000
$ {"message":"Hello World"}

# Docs should be visible here http://localhost:8000/docs or http://127.0.0.1:8000/redoc
```

```python
# Add a new route to main.py
@app.get("/users")
def get_users():
    return {"message": "Get Users!"}
```

```bash
# Test to see it working
$  curl http://127.0.0.1:8000/users
$ {"message":"Get Users!"}
```

```python
# Add a new route to main.py
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user": user_id}
```

Our folder sturcuture looks something like this

```
├── venv
├── main.py
├── requirements.in
├── requirements.txt
```
