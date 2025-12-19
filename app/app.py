import logging
import os
from flask import Flask, request, redirect, url_for, render_template_string, session

# Azure OpenCensus imports
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler

app = Flask(__name__)
app.secret_key = 'super-secret-key' # Change this in production

# 1. SETUP AZURE MONITORING
# Replace with your actual Connection String from Azure Portal
APPLICATION_INSIGHTS_CONNECTION_STRING = "InstrumentationKey=00000000-0000-0000-0000-000000000000"

# Middleware to automatically track requests
middleware = FlaskMiddleware(
    app,
    exporter=AzureExporter(connection_string=APPLICATION_INSIGHTS_CONNECTION_STRING),
    sampler=ProbabilitySampler(rate=1.0),
)

# Configure standard Python logging to send traces to Azure
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=APPLICATION_INSIGHTS_CONNECTION_STRING))
logger.setLevel(logging.INFO)

# In-memory storage
items = []

HTML_TEMPLATE = """
<!doctype html>
<title>Shopping List</title>
{% if session.get('user') %}
    <p>Logged in as: <strong>{{ session['user'] }}</strong> | <a href="/logout">Logout</a></p>
    <h1>Shopping List</h1>
    <form method="post" action="/add">
      <input name="item" placeholder="Add item" required>
      <button type="submit">Add</button>
    </form>
    <ul>
      {% for i in items %}
        <li>{{i}}</li>
      {% endfor %}
    </ul>
{% else %}
    <h1>Login Required</h1>
    <form method="post" action="/login">
      <input name="username" placeholder="Username" required>
      <button type="submit">Login</button>
    </form>
{% endif %}
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, items=items)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    if username:
        session['user'] = username
        logger.info(f"User '{username}' logged in successfully.")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    user = session.pop('user', None)
    if user:
        logger.info(f"User '{user}' logged out.")
    return redirect(url_for("index"))

@app.route("/add", methods=["POST"])
def add():
    if 'user' not in session:
        logger.warning("Unauthorized attempt to add item.")
        return redirect(url_for("index"))

    item = request.form.get("item", "").strip()
    if item:
        items.append(item)
        # Log the action to Azure Log Analytics
        logger.info(f"Item added: {item}", extra={'custom_dimensions': {'user': session.get('user')}})
        
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)