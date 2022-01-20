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
# run the server targeting app in main.py
$ uvicorn main:app --reload

$ INFO:     Will watch for changes in these directories: ['./fast-api-serverless']
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

### Our folder structure looks something like this

```
├── venv
├── main.py
├── requirements.in
├── requirements.txt
```

4. Setup serverless for AWS deployment

```bash
# Init NPM
$ npm init
# Install the serverless framework
$ npm install serverless
$ npm install serverless-python-requirements --dev
```

Next we need to add an adaptor to the [ASGI](https://asgi.readthedocs.io/en/latest/) application to be deployed in an AWS Lambda function to handle API Gateway requests and responses we will use [Mangum](https://mangum.io/)

```bash
$ echo "mangum" >> requirements.in

# Update requirements.txt from requirements.in
$ pip-compile

# install dependencies
$ pip install -r requirements.txt
```

Now we need to modify main.py to use the adaptor

```python
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# routes...

# Wrap the app with the Adaptor
handler = Mangum(app)
```

```bash
# Create serverless.yml file
$ touch serverless.yml
```

```yaml
# serverless.yml
service: fast-api-serverless-demo

package:
  individually: true

provider:
  name: aws
  runtime: python3.8
  region: af-south-1
  stage: ${opt:stage, "dev"}

plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    dockerizePip: true
    layer:
      name: fast-api-serverless-demo-layer
      description: Requirements layer
      compatibleRuntimes:
        - python3.8

functions:
  app:
    package:
      include:
        - "main.py"
      exclude:
        - "requirements.txt"
        - "package.json"
        - "package-lock.json"
        - ".serverless/**"
        - ".venv/**"
        - "node_modules/**"

    # points to handler in main.py
    handler: main.handler
    environment:
      STAGE: ${self:provider.stage}
    layers:
      - { Ref: PythonRequirementsLambdaLayer }
    events:
      - http:
          method: any
          path: /{proxy+}
```

5. Deployment

```
AWS_PROFILE=<your profile> sls deploy -s dev
```
