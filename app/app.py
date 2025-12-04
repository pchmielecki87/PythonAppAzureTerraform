from flask import Flask, render_template_string, request, redirect
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

# ----------------------------
# Key Vault configuration
# ----------------------------
KEY_VAULT_NAME = "keyvaulttest1"
KV_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=KV_URL, credential=credential)

# ----------------------------
# In-memory shopping list
# ----------------------------
shopping_list = []

# ----------------------------
# Template with dropdown + secrets
# ----------------------------
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Shopping List + Secrets</title>
</head>
<body>
    <h1>Shopping List</h1>

    <form method="POST" action="/add">
        <input type="text" name="item" placeholder="Add item" required>
        <button type="submit">Add</button>
    </form>

    <ul>
        {% for item in shopping_list %}
            <li>{{ item }}</li>
        {% endfor %}
    </ul>

    <hr>

    <h2>Read secret from Azure Key Vault</h2>

    <form method="GET" action="/">
        <label for="secret">Select secret:</label>
        <select name="secret">
            <option value="secret1" {% if selected_secret == "secret1" %}selected{% endif %}>secret1</option>
            <option value="secret2" {% if selected_secret == "secret2" %}selected{% endif %}>secret2</option>
        </select>
        <button type="submit">Read Secret</button>
    </form>

    {% if secret_value %}
        <p><strong>Value from Key Vault:</strong> {{ secret_value }}</p>
    {% endif %}
</body>
</html>
"""


# ----------------------------
# Helper function for secrets
# ----------------------------
def get_secret_value(secret_name):
    try:
        secret = secret_client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        return f"Error: {str(e)}"


# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET"])
def index():
    selected_secret = request.args.get("secret")

    if selected_secret:
        secret_value = get_secret_value(selected_secret)
    else:
        secret_value = None

    return render_template_string(
        TEMPLATE,
        shopping_list=shopping_list,
        selected_secret=selected_secret,
        secret_value=secret_value,
    )


@app.route("/add", methods=["POST"])
def add_item():
    item = request.form.get("item")
    if item:
        shopping_list.append(item)
    return redirect("/")


if __name__ == "__main__":
    # For local debugging only
    app.run(host="0.0.0.0", port=5000, debug=True)
