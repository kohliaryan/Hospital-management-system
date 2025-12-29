from flask import current_app as app

@app.get('/')
def hello():
    return "Server is running!"