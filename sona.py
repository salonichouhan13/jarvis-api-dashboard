
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template_string, request, jsonify
import requests
import os
import re

app = Flask(__name__)

# =========================================================
# CONFIG
# =========================================================

BASE_URL = "https://cybersameer-jarvis-apis1.onrender.com"

# Termux/Linux:
# export JARVIS_API_KEY="DEVELOPERCYBERSAMEER"
API_KEY = os.getenv("JARVIS_API_KEY", "DEVELOPERCYBERSAMEER")


# =========================================================
# SAFE API TOOLS
# =========================================================

API_TOOLS = {
    "ifsc": {
        "name": "IFSC Lookup",
        "icon": "🏦",
        "endpoint": "/ifsc",
        "method": "GET",
        "fields": {
            "code": "IFSC Code"
        }
    },

    "pincode": {
        "name": "Pincode Lookup",
        "icon": "📍",
        "endpoint": "/pincode",
        "method": "GET",
        "fields": {
            "pin": "Pincode"
        }
    },

    "imei": {
        "name": "IMEI / TAC Information",
        "icon": "📱",
        "endpoint": "/imei",
        "method": "GET",
        "fields": {
            "imei": "IMEI"
        }
    },

    "github": {
        "name": "GitHub User",
        "icon": "🐙",
        "endpoint": "/github",
        "method": "GET",
        "fields": {
            "username": "GitHub Username"
        }
    },

    "gitrepo": {
        "name": "GitHub Repository",
        "icon": "📦",
        "endpoint": "/gitrepo",
        "method": "GET",
        "fields": {
            "repo": "Repository (owner/name)"
        }
    },

    "gittrending": {
        "name": "GitHub Trending",
        "icon": "🔥",
        "endpoint": "/gittrending",
        "method": "GET",
        "fields": {
            "language": "Language",
            "period": "Period (daily/weekly/monthly)"
        }
    },

    "ipinfo": {
        "name": "IP Information",
        "icon": "🌐",
        "endpoint": "/ipinfo",
        "method": "GET",
        "fields": {
            "ip": "IP Address"
        }
    },

    "domaininfo": {
        "name": "Domain Information",
        "icon": "🔎",
        "endpoint": "/domaininfo",
        "method": "GET",
        "fields": {
            "domain": "Domain"
        }
    },

    "dns": {
        "name": "DNS Lookup",
        "icon": "🛰️",
        "endpoint": "/dns",
        "method": "GET",
        "fields": {
            "domain": "Domain",
            "type": "DNS Type (A/AAAA/MX/TXT)"
        }
    },

    "webinfo": {
        "name": "Website / DNS Info",
        "icon": "🌍",
        "endpoint": "/webinfo",
        "method": "GET",
        "fields": {
            "domain": "Domain",
            "type": "Type"
        }
    },

    "weather": {
        "name": "Weather",
        "icon": "🌤️",
        "endpoint": "/weather",
        "method": "GET",
        "fields": {
            "city": "City"
        }
    },

    "crypto": {
        "name": "Crypto Information",
        "icon": "₿",
        "endpoint": "/crypto",
        "method": "GET",
        "fields": {
            "coin": "Coin / Symbol"
        }
    },

    "emi": {
        "name": "EMI Calculator",
        "icon": "💰",
        "endpoint": "/emi",
        "method": "GET",
        "fields": {
            "principal": "Principal",
            "rate": "Interest Rate",
            "tenure": "Tenure (months)"
        }
    },

    "grade": {
        "name": "Grade Calculator",
        "icon": "🎓",
        "endpoint": "/grade",
        "method": "GET",
        "fields": {
            "marks": "Marks",
            "max_marks": "Maximum Marks"
        }
    },

    "element": {
        "name": "Periodic Element",
        "icon": "⚛️",
        "endpoint": "/element",
        "method": "GET",
        "fields": {
            "symbol": "Element Symbol"
        }
    },

    "qr": {
        "name": "QR Generator",
        "icon": "▦",
        "endpoint": "/qr",
        "method": "GET",
        "fields": {
            "text": "Text",
            "size": "Size",
            "color": "Color",
            "bgcolor": "Background Color"
        }
    },

    "github_repo": {
        "name": "GitHub Repository Info",
        "icon": "💻",
        "endpoint": "/gitrepo",
        "method": "GET",
        "fields": {
            "repo": "owner/repository"
        }
    },

    # ---------- NEW TOOLS ----------
    "aadhaar": {
        "name": "Aadhaar Verification",
        "icon": "🪪",
        "endpoint": "/aadhaar",
        "method": "GET",
        "fields": {
            "aadhaar": "Aadhaar Number"
        }
    },

    "pan": {
        "name": "PAN Verification",
        "icon": "📄",
        "endpoint": "/pan",
        "method": "GET",
        "fields": {
            "pan": "PAN Number"
        }
    },

    "phone": {
        "name": "Phone Number Lookup",
        "icon": "📞",
        "endpoint": "/phone",
        "method": "GET",
        "fields": {
            "number": "Phone Number"
        }
    },

    "calltracer": {
        "name": "Call Tracer",
        "icon": "🔍",
        "endpoint": "/calltracer",
        "method": "GET",
        "fields": {
            "number": "Phone Number"
        }
    },

    "truecaller": {
        "name": "Truecaller Lookup",
        "icon": "📇",
        "endpoint": "/truecaller",
        "method": "GET",
        "fields": {
            "number": "Phone Number"
        }
    },

    "vehicle": {
        "name": "Vehicle Info",
        "icon": "🚗",
        "endpoint": "/vehicle",
        "method": "GET",
        "fields": {
            "registration": "Registration Number"
        }
    }
}


# =========================================================
# HTML
# =========================================================

HTML = r'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width,initial-scale=1.0">

<title>J.A.R.V.I.S API TOOLS</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    background:
        radial-gradient(circle at top,#182848,#050914 55%);
    min-height: 100vh;
    color: white;
}

.header {
    padding: 25px 18px;
    text-align: center;
    border-bottom: 1px solid #273452;
    background: rgba(0,0,0,.35);
    backdrop-filter: blur(12px);
}

.header h1 {
    font-size: 28px;
    letter-spacing: 2px;
}

.header h1 span {
    color: #00d9ff;
}

.header p {
    margin-top: 8px;
    color: #8795b5;
    font-size: 13px;
}

.container {
    max-width: 1100px;
    margin: auto;
    padding: 25px 16px;
}

.layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 20px;
}

.panel {
    background: rgba(10,18,35,.86);
    border: 1px solid #263657;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 15px 45px rgba(0,0,0,.25);
}

.panel-title {
    font-size: 13px;
    color: #7181a2;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.tools {
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-height: 650px;
    overflow-y: auto;
}

.tool {
    border: 1px solid transparent;
    background: #111c32;
    color: #dce5ff;
    padding: 12px;
    border-radius: 11px;
    cursor: pointer;
    text-align: left;
    transition: .2s;
}

.tool:hover,
.tool.active {
    border-color: #00d9ff;
    background: #132840;
}

.tool-icon {
    margin-right: 8px;
}

.tool-count {
    float: right;
    color: #617292;
    font-size: 11px;
}

.tool-name {
    font-size: 13px;
    font-weight: bold;
}

.search-box {
    margin-bottom: 20px;
}

.search-box input {
    width: 100%;
    padding: 13px;
    border-radius: 10px;
    border: 1px solid #2b3b5c;
    background: #0a1222;
    color: white;
    outline: none;
}

.search-box input:focus {
    border-color: #00d9ff;
}

.selected {
    color: #00d9ff;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 18px;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    color: #8795b5;
    font-size: 12px;
    margin-bottom: 7px;
}

.form-group input {
    width: 100%;
    padding: 13px;
    border-radius: 10px;
    border: 1px solid #293a5b;
    background: #091121;
    color: white;
    outline: none;
}

.form-group input:focus {
    border-color: #00d9ff;
}

button.run {
    width: 100%;
    padding: 14px;
    border: 0;
    border-radius: 11px;
    background: linear-gradient(135deg,#00d9ff,#0077ff);
    color: white;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
}

button.run:disabled {
    opacity: .5;
}

.status {
    margin-top: 15px;
    font-size: 12px;
    color: #7e8eae;
}

.result {
    margin-top: 20px;
    display: none;
}

.result.show {
    display: block;
}

.result-card {
    background: #0a1427;
    border: 1px solid #263857;
    border-radius: 14px;
    overflow: hidden;
}

.result-header {
    padding: 13px 15px;
    background: #111e35;
    border-bottom: 1px solid #263857;
    display: flex;
    justify-content: space-between;
}

.badge {
    background: #123b32;
    color: #4dffbf;
    border-radius: 20px;
    padding: 5px 10px;
    font-size: 10px;
}

.result-body {
    padding: 15px;
}

.row {
    display: flex;
    justify-content: space-between;
    gap: 15px;
    padding: 12px 0;
    border-bottom: 1px solid #1d2b44;
}

.row:last-child {
    border-bottom: 0;
}

.key {
    color: #7181a2;
    font-size: 12px;
}

.value {
    color: #e8efff;
    font-size: 13px;
    text-align: right;
    word-break: break-word;
}

.json-toggle {
    margin-top: 12px;
    width: 100%;
    padding: 11px;
    border-radius: 9px;
    border: 1px solid #293b5d;
    background: #101c31;
    color: #9eacc7;
    cursor: pointer;
}

.json {
    display: none;
    margin-top: 10px;
    padding: 15px;
    background: #03070d;
    border-radius: 10px;
    color: #55ff99;
    font-family: monospace;
    font-size: 11px;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 400px;
    overflow: auto;
}

.json.show {
    display: block;
}

.error {
    margin-top: 15px;
    color: #ff6875;
    font-size: 13px;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #53617b;
    font-size: 11px;
}

@media(max-width:750px) {

    .layout {
        grid-template-columns: 1fr;
    }

    .tools {
        max-height: 300px;
    }

    .header h1 {
        font-size: 21px;
    }

}

</style>
</head>

<body>

<header class="header">
    <h1>🤖 <span>J.A.R.V.I.S</span> API TOOLS</h1>
    <p>Public Utility & Developer API Dashboard</p>
</header>

<div class="container">

<div class="layout">

<!-- TOOL MENU -->

<div class="panel">

<div class="panel-title">
    API TOOLS
</div>

<div class="search-box">
    <input
        id="toolSearch"
        placeholder="Search API tools..."
        oninput="filterTools()">
</div>

<div class="tools" id="tools">

{% for key, tool in tools.items() %}

<button
    class="tool"
    data-name="{{ tool.name|lower }}"
    onclick="selectTool('{{ key }}')">

<span class="tool-icon">{{ tool.icon }}</span>

<span class="tool-name">
{{ tool.name }}
</span>

</button>

{% endfor %}

</div>

</div>


<!-- MAIN -->

<div class="panel">

<div class="selected" id="selectedTool">
    Select an API Tool
</div>

<div id="formArea">
    <p style="color:#697895;font-size:13px">
        Left side se koi API tool select karo.
    </p>
</div>

<div class="status" id="status"></div>

<div class="result" id="result">

<div class="result-card">

<div class="result-header">
    <strong>API RESULT</strong>
    <span class="badge">SUCCESS</span>
</div>

<div class="result-body" id="resultBody"></div>

</div>

<button
    class="json-toggle"
    onclick="toggleJSON()">
    { } View Raw JSON
</button>

<pre class="json" id="json"></pre>

</div>

<div class="error" id="error"></div>

</div>

</div>

</div>

<footer class="footer">
    J.A.R.V.I.S API Dashboard · Use APIs responsibly
</footer>


<script>

const tools = {{ tools|tojson }};

let selected = null;


function selectTool(key) {

    selected = key;

    const tool = tools[key];

    document.getElementById("selectedTool").innerText =
        tool.icon + " " + tool.name;

    let html = "";

    for (const field in tool.fields) {

        html += `
        <div class="form-group">

            <label>${tool.fields[field]}</label>

            <input
                id="field_${field}"
                placeholder="${tool.fields[field]}">

        </div>
        `;

    }

    html += `
        <button
            class="run"
            id="runButton"
            onclick="runAPI()">
            ⚡ RUN API
        </button>
    `;

    document.getElementById("formArea").innerHTML = html;

    document.getElementById("result").classList.remove("show");

    document.getElementById("error").innerText = "";

    document.getElementById("status").innerText =
        "Ready — " + tool.endpoint;
}


function filterTools() {

    const query =
        document.getElementById("toolSearch")
        .value.toLowerCase();

    document.querySelectorAll(".tool").forEach(btn => {

        const name = btn.dataset.name;

        btn.style.display =
            name.includes(query) ? "block" : "none";

    });
}


async function runAPI() {

    if (!selected) return;

    const tool = tools[selected];

    const params = {};

    for (const field in tool.fields) {

        const input =
            document.getElementById("field_" + field);

        if (input) {
            params[field] = input.value.trim();
        }

    }

    document.getElementById("error").innerText = "";

    const button =
        document.getElementById("runButton");

    button.disabled = true;
    button.innerText = "⏳ PROCESSING...";

    document.getElementById("status").innerText =
        "Connecting to API...";

    try {

        const response = await fetch("/api/run", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                tool: selected,
                params: params
            })

        });

        const data = await response.json();

        if (!response.ok || data.status === "error") {

            throw new Error(
                data.message || "API request failed"
            );

        }

        showResult(data.data);

        document.getElementById("status").innerText =
            "✓ Request completed";

    }

    catch (error) {

        document.getElementById("error").innerText =
            "❌ " + error.message;

        document.getElementById("status").innerText =
            "Request failed";

    }

    finally {

        button.disabled = false;
        button.innerText = "⚡ RUN API";

    }
}


function showResult(data) {

    const result =
        document.getElementById("result");

    const body =
        document.getElementById("resultBody");

    const json =
        document.getElementById("json");

    body.innerHTML = "";

    function addRows(obj, prefix="") {

        if (
            typeof obj !== "object" ||
            obj === null
        ) {

            body.innerHTML += `
            <div class="row">
                <span class="key">${prefix}</span>
                <span class="value">
                    ${escapeHTML(String(obj))}
                </span>
            </div>`;

            return;
        }

        for (const key in obj) {

            const value = obj[key];

            if (
                typeof value === "object" &&
                value !== null
            ) {

                addRows(
                    value,
                    prefix ? prefix + "." + key : key
                );

            } else {

                body.innerHTML += `
                <div class="row">
                    <span class="key">
                        ${escapeHTML(
                            prefix ? prefix + "." + key : key
                        )}
                    </span>

                    <span class="value">
                        ${escapeHTML(String(value))}
                    </span>
                </div>`;

            }

        }

    }

    addRows(data);

    json.innerText =
        JSON.stringify(data, null, 2);

    result.classList.add("show");

}


function toggleJSON() {

    document
        .getElementById("json")
        .classList.toggle("show");

}


function escapeHTML(value) {

    return value
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}

</script>

</body>
</html>
'''


# =========================================================
# RESPONSE CLEANER – removes developer/user and adds team
# =========================================================

def clean_api_response(data):
    """
    Remove 'developer' and 'user' keys from the API response
    and add a 'team' field with value 'TEAM WALHALLA'.
    Works recursively on dictionaries.
    """
    if isinstance(data, dict):
        # Remove top-level developer and user
        data.pop("developer", None)
        data.pop("user", None)
        # Add team
        data["team"] = "TEAM WALHALLA"
        # Clean any nested dicts (though we only need top-level for QR)
        for key, value in data.items():
            if isinstance(value, dict):
                clean_api_response(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        clean_api_response(item)
    return data


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template_string(
        HTML,
        tools=API_TOOLS
    )


# =========================================================
# API PROXY
# =========================================================

@app.route("/api/run", methods=["POST"])
def run_api():

    try:

        body = request.get_json(silent=True) or {}

        tool_key = body.get("tool")
        params = body.get("params") or {}

        if tool_key not in API_TOOLS:
            return jsonify({
                "status": "error",
                "message": "Invalid API tool"
            }), 400

        tool = API_TOOLS[tool_key]

        # Basic input cleanup
        clean_params = {}

        for key, value in params.items():

            if not isinstance(value, str):
                value = str(value)

            value = value.strip()

            if len(value) > 500:
                return jsonify({
                    "status": "error",
                    "message": f"Input too long: {key}"
                }), 400

            clean_params[key] = value

        # Add API key server-side
        clean_params["key"] = API_KEY

        url = BASE_URL.rstrip("/") + tool["endpoint"]

        response = requests.get(
            url,
            params=clean_params,
            timeout=30
        )

        content_type = response.headers.get(
            "content-type",
            ""
        ).lower()

        if "application/json" in content_type:

            data = response.json()

            # ---- CLEAN THE RESPONSE ----
            clean_api_response(data)

        else:

            data = {
                "response": response.text
            }

        if response.status_code >= 400:

            return jsonify({
                "status": "error",
                "message": f"Remote API returned HTTP {response.status_code}",
                "data": data
            }), response.status_code

        return jsonify({
            "status": "success",
            "data": data
        })

    except requests.exceptions.Timeout:

        return jsonify({
            "status": "error",
            "message": "API timeout"
        }), 504

    except requests.exceptions.RequestException as e:

        return jsonify({
            "status": "error",
            "message": "Could not connect to API"
        }), 502

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5001)
    )

    print("=" * 55)
    print("🤖 J.A.R.V.I.S API DASHBOARD")
    print("=" * 55)
    print(f"BASE URL : {BASE_URL}")
    print(f"SERVER   : http://127.0.0.1:{port}")
    print("=" * 55)

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        threaded=True
    )