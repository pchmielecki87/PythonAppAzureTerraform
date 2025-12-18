import logging
from flask import Flask, request, redirect, url_for, render_template_string

# ----------------------------
# Application Insights (OpenTelemetry)
# ----------------------------
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# Enable Azure Monitor exporter
configure_azure_monitor()

# Enable logging + Flask instrumentation
LoggingInstrumentor().instrument(set_logging_format=True)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# In-memory list
# ----------------------------
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

# ----------------------------
# Routes
# ----------------------------
@app.route("/")
def index():
    logger.info("GET / called", extra={"items_count": len(items)})
    return render_template_string(HTML, items=items)

@app.route("/add", methods=["POST"])
def add():
    item = request.form.get("item", "").strip()

    if item:
        items.append(item)
        logger.info(
            "Item added",
            extra={
                "item": item,
                "total_items": len(items)
            },
        )
    else:
        logger.warning("Empty item submitted")

    return redirect(url_for("index"))

# ----------------------------
# Local execution
# ----------------------------
if __name__ == "__main__":
    logger.info("Starting Flask app")
    app.run(host="0.0.0.0", port=8000)
