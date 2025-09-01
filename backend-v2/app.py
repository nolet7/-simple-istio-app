from flask import Flask
import os

app = Flask(__name__)
version = os.getenv("VERSION", "v1")

@app.route("/")
def home():
    return {"message": f"Hello from Backend {version}"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
