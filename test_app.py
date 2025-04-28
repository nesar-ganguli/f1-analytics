from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Flask is working! 🎉"

@app.route("/api/test")
def test():
    return {"message": "Test API works ✅"}

if __name__ == "__main__":
    app.run(debug=True, port=5099)

