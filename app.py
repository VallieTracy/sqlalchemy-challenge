from flask import Flask, jsonify

app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"




if __name__ == "__main__":
    app.run(debug=True)