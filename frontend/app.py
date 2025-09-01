from flask import Flask, render_template_string
app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
    <h1>Simple Frontend</h1>
    <p>This is the frontend. Visit <a href="/api">/api</a> to test the backend (canary traffic in Istio).</p>
    """)

@app.route("/api")
def api():
    return {"message": "Frontend calls backend at /backend"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
