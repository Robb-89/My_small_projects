from flask import Flask, request

app = Flask(__name__)

# Route to handle incoming XSS callbacks
@app.route("/xss", methods=["GET", "POST"])
def handle_xss():
    # Log incoming data from the request
    data = request.args.get("data", "No data received")
    print(f"[!] XSS Callback Received: {data}")

    # Respond to the request
    return "Callback received!", 200

if __name__ == "__main__":
    # Start the server on localhost:5000
    app.run(host="0.0.0.0", port=5000)
