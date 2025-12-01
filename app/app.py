from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
# in-memory list
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
    return render_template_string(HTML, items=items)

@app.route("/add", methods=["POST"])
def add():
    item = request.form.get("item", "").strip()
    if item:
        items.append(item)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
