import logging
from flask import Flask, request, redirect, url_for, render_template_string

# Azure OpenCensus imports
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware

app = Flask(__name__)

# --- AZURE CONFIGURATION ---
# Replace with your actual Connection String from the Azure Portal
CONNECTION_STRING = "InstrumentationKey=00000000-0000-0000-0000-000000000000"

# 1. Automatic Request Tracking (Application Insights)
middleware = FlaskMiddleware(
    app,
    exporter=AzureExporter(connection_string=CONNECTION_STRING),
    sampler=ProbabilitySampler(rate=1.0),
)

# 2. Custom Logging (Log Analytics)
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=CONNECTION_STRING))
logger.setLevel(logging.INFO)
# ---------------------------

items = []

HTML = """
<!doctype html>
<title>Shopping List</title>
<h1>Shopping List</h1>
<form method=post action="/add">
  <input name=item placeholder="Add item" required>
  <button type=submit>Add</button>
</form>

<ul>
  {% for i in items %}
    <li>{{i}}</li>
  {% endfor %}
</ul>
"""

@app.route("/")
def index():
    # Log when the list is viewed
    logger.info(f"Shopping list viewed. Current item count: {len(items)}")
    return render_template_string(HTML, items=items)

@app.route("/add", methods=["POST"])
def add():
    item = request.form.get("item", "").strip()
    if item:
        items.append(item)
        # Log when a new item is added
        logger.info(f"New item added to list: {item}")
    else:
        logger.warning("Attempted to add an empty item.")
        
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)