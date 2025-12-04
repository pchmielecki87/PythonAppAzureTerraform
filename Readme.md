# 🛒 Azure Python Web App + Terraform + Azure DevOps

**Fully automated deployment of a Python Flask web app with Azure App Service, Key Vault integration, Application Insights, and Azure DevOps multi-stage pipeline.**

---

# 📦 What’s inside this repository?

```
/
├── app/
│   ├── app.py                # Flask application with shopping list + Key Vault secrets
│   └── requirements.txt      # Python dependencies
│
├── terraform/
│   ├── main.tf               # Core resources (App Service, Plan, App Insights)
│   ├── keyvault.tf           # Key Vault data source (existing KV)
│   ├── outputs.tf            # Useful Terraform outputs
│   ├── variables.tf          # Variables for prefix, location, misc
│   └── backend.tf            # Remote state (Azure Storage)
│
└── azure-pipelines.yaml      # Azure DevOps pipeline (build + terraform + deploy)
```

---

# 🗺️ Architecture Overview

```
                     ┌─────────────────────────────┐
                     │        Developers           │
                     │    (push to main branch)    │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                         ┌────────────────────┐
                         │ Azure DevOps CI/CD │
                         │  Multi-stage YAML  │
                         └───────┬────────────┘
   ┌─────────────────────────────┼─────────────────────────────────────────┐
   │                             │                                         │
   ▼                             ▼                                         ▼
┌──────────┐           ┌──────────────────┐                    ┌────────────────────┐
│ Build    │  builds   │   Terraform      │ deploys infra:     │ Deploy to App      │
│ Python   │──────────▶│ (init/plan/apply)│ App Service Plan,  │ Service (Linux)    │
│ Flask    │           │                  │ App Service,       │ with Managed ID    │
└──────────┘           └──────────────────┘ App Insights, KV   └────────────────────┘
                                                ▲
                                                │ data source (existing KV)
                                                ▼
                                  ┌────────────────────────────┐
                                  │ Azure Key Vault (existing) │
                                  │ secrets: secret1, secret2  │
                                  └────────────────────────────┘
```

---

# 🧩 Components

### 🐍 **Python Web App**

* Built with **Flask**
* Simple shopping list UI (+ item add)
* Dropdown to choose **secret1 / secret2**
* Secrets dynamically loaded from **Azure Key Vault**
* On refresh → updated secret value is displayed instantly
* Uses `DefaultAzureCredential` (MSI-ready)

---

### ☁️ **Azure Infrastructure (Terraform)**

All Azure resources are **Free tier**:

| Resource                     | Azure Tier | Description                |
| ---------------------------- | ---------- | -------------------------- |
| **App Service Plan**         | F1 (Free)  | Linux hosting plan         |
| **App Service**              | Free       | Hosts Flask application    |
| **Application Insights**     | Free       | Telemetry & monitoring     |
| **Log Analytics (optional)** | Low-cost   | Diagnostics workspace      |
| **Key Vault (data source)**  | existing   | Reads `secret1`, `secret2` |

---

## 🔐 Key Vault Integration Diagram

```
╔══════════════════╗       managed identity       ╔══════════════════════════╗
║  Flask Web App   ║ ───────────────────────────▶ ║ Azure Key Vault          ║
║ /app/app.py      ║   DefaultAzureCredential     ║ - secret1                ║
║                  ║                              ║ - secret2                ║
╚══════════════════╝                              ╚══════════════════════════╝
```

---

# 🛠️ Azure DevOps Pipeline (3 Stages)

```
┌─────────────────────────────────────────────────────────────────┐
│       Azure DevOps Multi-Stage YAML Pipeline                    │
└─────────────────────────────────────────────────────────────────┘

1️⃣ **Build Stage**
   - Install Python
   - Install dependencies
   - Package the Flask app (zip)

2️⃣ **Terraform Stage**
   - terraform init
   - terraform plan (always runs)
   - terraform apply (manual “run or skip”)
   - terraform destroy (optional manual flag)
   - unlock state if needed

3️⃣ **Deployment Stage**
   - Retrieve outputs from Terraform
   - Deploy Flask build artifact into Azure App Service
```

---

# 🚀 Deployment Flow Summary

```
git push ➜ Pipeline triggers ➜ Build App ➜ Terraform infra ➜ Deploy App
```

After deployment:

* App Service runs Flask app
* App connects to existing Key Vault
* On UI page load → secrets are fetched live

---

# 🧰 Technologies Used

| Area          | Technology                         |
| ------------- | ---------------------------------- |
| Web App       | Python 3.x, Flask                  |
| Secrets       | Azure Key Vault + Managed Identity |
| Infra as Code | Terraform (azurerm provider)       |
| Hosting       | Azure App Service (Linux F1)       |
| Monitoring    | Application Insights               |
| CI/CD         | Azure DevOps YAML Pipelines        |
| State Backend | Azure Storage (remote tfstate)     |
