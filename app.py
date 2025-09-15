from flask import Flask

print("🚀 app.py started")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask is running!"

if __name__ == "_main_":
    print("⚡ About to start Flask server on http://127.0.0.1:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=True)