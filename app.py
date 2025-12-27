from flask import Flask, jsonify
from cost_dashboard import fetch_cost_dashboard

app = Flask(__name__)

@app.route("/api/cost-dashboard", methods=["GET"])
def cost_dashboard():
    data = fetch_cost_dashboard()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
