import instana  # noqa: F401

import logging
import random
import threading
import time

import requests
from flask import Flask, jsonify

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8080"

SIMULATED_ERRORS = [
    (logging.ERROR,    "DatabaseConnectionError - failed to connect to db:5432"),
    (logging.ERROR,    "TimeoutError - upstream service did not respond within 5s"),
    (logging.CRITICAL, "NullPointerException in payment service"),
    (logging.WARNING,  "ServiceUnavailable - downstream timeout on /inventory"),
    (logging.ERROR,    "AuthenticationFailure - invalid token presented by client"),
    (logging.WARNING,  "HighMemoryUsage - heap usage above 85%"),
    (logging.ERROR,    "CircuitBreakerOpen - calls to recommendations-service blocked"),
]

# ---------------------------------------------------------------------------
# Background: real HTTP traffic to self (every 10–20 s)
# ---------------------------------------------------------------------------

def _traffic_loop():
    # give gunicorn a moment to fully start
    time.sleep(5)
    endpoints = [
        "/products",
        "/orders",
        "/orders",
        "/checkout",
        "/users/profile",
        "/inventory",
        "/recommendations",
        "/cart/item",
        "/payments",
    ]
    while True:
        path = random.choice(endpoints)
        try:
            requests.get(f"{BASE_URL}{path}", timeout=3)
        except Exception:
            pass
        time.sleep(random.uniform(10, 20))


# ---------------------------------------------------------------------------
# Background: simulated errors (every 30–70 s)
# ---------------------------------------------------------------------------

def _error_loop():
    while True:
        time.sleep(random.uniform(30, 70))
        level, message = random.choice(SIMULATED_ERRORS)
        logger.log(level, message)


# ---------------------------------------------------------------------------
# Start background threads (daemon=True so they die with the process)
# ---------------------------------------------------------------------------

threading.Thread(target=_traffic_loop, daemon=True).start()
threading.Thread(target=_error_loop, daemon=True).start()

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return jsonify({"status": "running"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/products")
def products():
    if random.random() < 0.1:
        return jsonify({"error": "not found"}), 404
    return jsonify({"products": ["item1", "item2", "item3"]}), 200


@app.route("/orders")
def orders():
    return jsonify({"orders": []}), 200


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    return jsonify({"status": "ok"}), 201


@app.route("/users/profile")
def users_profile():
    return jsonify({"user": "workshop"}), 200


@app.route("/inventory")
def inventory():
    return jsonify({"stock": random.randint(0, 100)}), 200


@app.route("/recommendations")
def recommendations():
    return jsonify({"items": []}), 200


@app.route("/cart/item", methods=["GET", "DELETE"])
def cart_item():
    return jsonify({"status": "removed"}), 204


@app.route("/payments", methods=["GET", "POST"])
def payments():
    if random.random() < 0.3:
        logger.error("DatabaseConnectionError - failed to connect to db:5432")
        return jsonify({"error": "DatabaseConnectionError"}), 500
    return jsonify({"status": "processed"}), 200


@app.route("/checkout/confirm", methods=["GET", "POST"])
def checkout_confirm():
    if random.random() < 0.2:
        logger.critical("NullPointerException in payment service")
        return jsonify({"error": "NullPointerException"}), 500
    return jsonify({"status": "confirmed"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
