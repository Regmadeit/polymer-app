from flask import Flask, request, redirect, url_for, render_template_string, session, send_from_directory
import os
from werkzeug.utils import secure_filename
import pandas as pd

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

submitted_forms = []

### ---------- STATIC FILE SERVING ---------- ###
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

### ---------- LOGIN ROUTE ---------- ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session['user'] = email  # Store the user's email in session
        return redirect(url_for('home'))  # Redirect to the homepage

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Login | Republic Services</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5; /* Republic Services Blue */
                color: white;
                text-align: center;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
                font-family: Arial, sans-serif;
            }
            .login-box {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 0 15px rgba(255, 205, 0, 0.8);
                animation: fadeIn 1s ease-in-out;
            }
            .login-box h2 {
                color: #003DA5;
            }
            .form-control {
                margin-bottom: 10px;
            }
            .btn-login {
                background-color: #FFCD00;
                border: none;
                width: 100%;
                font-weight: bold;
                padding: 10px;
                color: black;
            }
            .btn-login:hover {
                background-color: #FFD700;
            }
            .logo {
                width: 120px;
                margin-bottom: 20px;
                animation: bounce 1.5s infinite;
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <img src="{{ url_for('static', filename='logo.png') }}" alt="Republic Services Logo" class="logo">
        <div class="login-box">
            <h2>Sign in with Outlook</h2>
            <form method="POST">
                <input type="email" class="form-control" id="email" name="email" placeholder="Email address" required>
                <input type="password" class="form-control" id="password" name="password" placeholder="Password" required>
                <button type="submit" class="btn btn-login">Login</button>
            </form>
        </div>
    </body>
    </html>
    ''')
@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Republic Services Polymer Center</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding-top: 50px;
                padding-bottom: 20px;
            }
            .logo {
                width: 120px;
                margin: 0 auto 20px;
                display: block;
            }
            .nav-button {
                background-color: #FFC72C;
                color: #004289;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                margin: 15px auto;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                width: 90%;
                max-width: 400px;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .nav-button:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
            .container {
                padding: 0 15px;
            }
            footer {
                margin-top: 40px;
                font-size: 13px;
                color: rgba(255,255,255,0.7);
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Republic Services Logo" class="logo">
            <div class="d-flex flex-column align-items-center">
                <a href="/checklist" class="nav-button">Operator Checklists</a>
                <a href="/supervisor" class="nav-button">Supervisor Review</a>
                <a href="https://accumatica.com" target="_blank" class="nav-button">Accumatica</a>
                <a href="/login" class="nav-button">Login with Outlook</a>
                <a href="/logistics" class="nav-button">Logistics Dashboard</a>
                <a href="/maintenance" class="nav-button">Maintenance Dashboard</a>
            </div> 
            <footer>
                <p class="mt-4">A work in progress by Reginald Turner</p>
            </footer>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    ''')

@app.route('/checklist')
def checklist_home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Operator Checklists</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding-top: 40px;
                padding-bottom: 20px;
            }
            .logo {
                width: 120px;
                margin: 0 auto 20px;
                display: block;
            }
            .nav-button {
                background-color: #FFC72C;
                color: #003DA5;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                margin: 15px auto;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .nav-button:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
            .container {
                padding: 0 15px;
            }
            footer {
                margin-top: 40px;
                font-size: 13px;
                color: rgba(255,255,255,0.7);
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Republic Services Logo" class="logo">
            <h2 class="mb-4">Operator Checklists</h2>
            <a href="/checklist/washline" class="btn nav-button">Washline Checklist</a>
            <a href="/checklist/crosswrap" class="btn nav-button">Crosswrap Checklist</a>
            <a href="/checklist/baler" class="btn nav-button">Baler Checklist</a>
            <a href="/checklist/forklift" class="btn nav-button">Forklift Checklist</a>
            
            <a href="/" class="btn nav-button" style="background-color:#fff; color:#003DA5;">Back to Dashboard</a>
            
            <footer>
                <p class="mt-4">A work in progress by Reginald Turner</p>
            </footer>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    ''')

@app.route('/checklist/forklift', methods=['GET', 'POST'])
def forklift_checklist():
    checklist_items = [
        "Steps/handrails functional & in place",
        "Ensure all caps are secure and locked",
        "Inspect hoses, fittings, cylinders for wear and leaks",
        "Inspect for any equipment damage",
        "Check horn",
        "Inspect fire extinguisher (Green light on)",
        "Check mirrors",
        "Check all exterior lights",
        "Check battery disconnect is OFF",
        "Check engine/crankcase oil level",
        "Check hydraulic oil level",
        "Check coolant level (when engine is cold)",
        "Check air filter (replace/clean as needed)",
        "Check back-up alarm camera",
        "Perform field brake test (before starting work)",
        "Strobe light working",
        "Check tires & wheels",
        "Test 2-way radio for proper functioning",
        "Check pivot shaft oil site gauge",
        "Seat and belt in good condition",
        "Clean windows and cab",
        "MAIN DISCONNECT MUST BE TURNED OFF AT END OF SHIFT OR WHEN MACHINE IS NOT IN SERVICE.",
        "Describe any necessary repairs or problems for the technician to address."
    ]

    if request.method == 'POST':
        operator_name = request.form.get('operator')
        date = request.form.get('date')
        notes = request.form.get('notes')
        checklist_responses = {item: request.form.get(item, 'No') for item in checklist_items}

        # Save responses to Excel file
        df = pd.DataFrame([{
            'Operator': operator_name,
            'Date': date,
            'Notes': notes,
            **checklist_responses
        }])

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'forklift_checklist.xlsx')
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(file_path, index=False)

        return redirect(url_for('home'))

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Forklift Checklist</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                padding: 20px;
            }
            .logo {
                width: 100px;
                margin: 20px auto;
                cursor: pointer;
            }
            .form-check-label {
                text-align: left;
                display: block;
            }
        </style>
    </head>
    <body>
        <img src="{{ url_for('static', filename='logo.png') }}" class="logo" onclick="window.location.href='/'">
        <h2 class="text-center">Forklift Operator Checklist</h2>
        <form method="POST">
            <div class="mb-3">
                <label>Operator Name:</label>
                <input type="text" name="operator" class="form-control" required>
            </div>
            <div class="mb-3">
                <label>Date:</label>
                <input type="date" name="date" class="form-control" required>
            </div>
            
            {% for item in checklist_items %}
                <div class="form-check">
                    <input type="checkbox" class="form-check-input" name="{{item}}" id="{{item}}" value="Yes">
                    <label class="form-check-label" for="{{item}}">{{item}}</label>
                </div>
            {% endfor %}

            <div class="mb-3 mt-3">
                <label>Additional Notes:</label>
                <textarea name="notes" class="form-control"></textarea>
            </div>
            <button class="btn btn-warning mt-2">Submit Checklist</button>
        </form>
        <a href="/checklist" class="btn btn-secondary mt-3">Back to Checklists</a>
    </body>
    </html>
    ''', checklist_items=checklist_items)


@app.route('/checklist/washline', methods=['GET', 'POST'])
def washline_checklist():
    checklist_tasks = [
        "Inspect all filters and clean if needed",
        "Verify water levels and temperature",
        "Ensure conveyor belts are properly aligned",
        "Check all valves for proper function",
        "Inspect spray nozzles for clogs",
        "Verify the chemical feed system is operational",
        "Document any issues or maintenance needs"
    ]

    if request.method == 'POST':
        operator = request.form['operator']
        date = request.form['date']
        notes = request.form.get('notes', '')

        task_results = {task: ('Completed' if request.form.get(task) else 'Not Completed') for task in checklist_tasks}

        submission = {
            'Operator': operator,
            'Date': date,
            'Notes': notes,
            **task_results
        }

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'washline_checklist.xlsx')
        df = pd.DataFrame([submission])

        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(file_path, index=False)

        return redirect(url_for('home'))

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Washline Checklist</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                padding: 15px;
            }
            .form-check-label {
                font-size: 14px;
            }
            .logo {
                width: 100px;
                margin: 15px auto;
                display: block;
                cursor: pointer;
            }
            .submit-btn {
                background-color: #FFCD00;
                color: black;
            }
        </style>
    </head>
    <body>
        <img src="{{ url_for('static', filename='logo.png') }}" class="logo" onclick="window.location.href='/'">
        <h3 class="text-center mb-3">Washline Checklist</h3>
        <form method="POST">
            {% for task in checklist_tasks %}
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="{{task}}" name="{{task}}">
                <label class="form-check-label" for="{{task}}">{{task}}</label>
            </div>
            {% endfor %}
            <div class="mb-2 mt-3">
                <input class="form-control" type="text" name="operator" placeholder="Operator Name" required>
            </div>
            <div class="mb-2">
                <input class="form-control" type="date" name="date" required>
            </div>
            <div class="mb-2">
                <textarea class="form-control" name="notes" placeholder="Notes (optional)"></textarea>
            </div>
            <button type="submit" class="btn submit-btn w-100">Submit Checklist</button>
        </form>
        <a href="/" class="btn btn-secondary w-100 mt-2">Home</a>
    </body>
    </html>
    ''', checklist_tasks=checklist_tasks)

@app.route('/checklist/baler', methods=['GET', 'POST'])
def baler_checklist():
    checklist_tasks = [
        "Inspect hydraulic fluid levels",
        "Check for debris in the baler chamber",
        "Test the ejection system",
        "Inspect belts and pulleys for wear",
        "Ensure all safety guards are in place",
        "Check sensors for proper operation",
        "Document any issues or maintenance needs"
    ]

    if request.method == 'POST':
        operator = request.form['operator']
        date = request.form['date']
        notes = request.form.get('notes', '')

        task_results = {task: ('Completed' if request.form.get(task) else 'Not Completed') for task in checklist_tasks}

        submission = {
            'Operator': operator,
            'Date': date,
            'Notes': notes,
            **task_results
        }

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'baler_checklist.xlsx')
        df = pd.DataFrame([submission])

        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(file_path, index=False)

        return redirect(url_for('home'))

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Baler Checklist</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                padding: 15px;
            }
            .form-check-label {
                font-size: 14px;
            }
            .logo {
                width: 100px;
                margin: 15px auto;
                display: block;
                cursor: pointer;
            }
            .submit-btn {
                background-color: #FFCD00;
                color: black;
            }
        </style>
    </head>
    <body>
        <img src="{{ url_for('static', filename='logo.png') }}" class="logo" onclick="window.location.href='/'">
        <h3 class="text-center mb-3">Baler Checklist</h3>
        <form method="POST">
            {% for task in checklist_tasks %}
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="{{task}}" name="{{task}}">
                <label class="form-check-label" for="{{task}}">{{task}}</label>
            </div>
            {% endfor %}
            <div class="mb-2 mt-3">
                <input class="form-control" type="text" name="operator" placeholder="Operator Name" required>
            </div>
            <div class="mb-2">
                <input class="form-control" type="date" name="date" required>
            </div>
            <div class="mb-2">
                <textarea class="form-control" name="notes" placeholder="Notes (optional)"></textarea>
            </div>
            <button type="submit" class="btn submit-btn w-100">Submit Checklist</button>
        </form>
        <a href="/" class="btn btn-secondary w-100 mt-2">Home</a>
    </body>
    </html>
    ''', checklist_tasks=checklist_tasks)

@app.route('/checklist/crosswrap', methods=['GET', 'POST'])
def crosswrap_checklist():
    checklist_tasks = [
        "Inspect wrapper alignment",
        "Check for loose straps",
        "Ensure wrapping material is loaded",
        "Inspect safety guards and emergency stops",
        "Clean rollers and sensors",
        "Verify operational readiness",
        "Document any issues or maintenance needs"
    ]

    if request.method == 'POST':
        operator = request.form['operator']
        date = request.form['date']
        notes = request.form.get('notes', '')

        task_results = {task: ('Completed' if request.form.get(task) else 'Not Completed') for task in checklist_tasks}

        submission = {
            'Operator': operator,
            'Date': date,
            'Notes': notes,
            **task_results
        }

        # Excel file storage
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'crosswrap_checklist.xlsx')
        df = pd.DataFrame([submission])

        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(file_path, index=False)

        return redirect(url_for('home'))

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Crosswrap Checklist</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                padding: 15px;
            }
            .form-check-label {
                font-size: 14px;
            }
            .logo {
                width: 100px;
                margin: 15px auto;
                display: block;
                cursor: pointer;
            }
            .submit-btn {
                background-color: #FFCD00;
                color: black;
            }
        </style>
    </head>
    <body>
        <img src="{{ url_for('static', filename='logo.png') }}" class="logo" onclick="window.location.href='/'">
        <h3 class="text-center mb-3">Crosswrap Checklist</h3>
        <form method="POST">
            {% for task in checklist_tasks %}
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="{{task}}" name="{{task}}">
                <label class="form-check-label" for="{{task}}">{{task}}</label>
            </div>
            {% endfor %}
            <div class="mb-2 mt-3">
                <input class="form-control" type="text" name="operator" placeholder="Operator Name" required>
            </div>
            <div class="mb-2">
                <input class="form-control" type="date" name="date" required>
            </div>
            <div class="mb-2">
                <textarea class="form-control" name="notes" placeholder="Notes (optional)"></textarea>
            </div>
            <button type="submit" class="btn submit-btn w-100">Submit Checklist</button>
        </form>
        <a href="/" class="btn btn-secondary w-100 mt-2">Home</a>
    </body>
    </html>
    ''', checklist_tasks=checklist_tasks)

@app.route('/logistics')
def logistics_dashboard():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Logistics Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {
                background-color: #003DA5;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding-top: 30px;
            }
            .container {
                max-width: 1200px;
                margin: auto;
                padding: 20px;
            }
            .btn-custom {
                background-color: #FFC72C;
                color: #004289;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                margin-top: 15px;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .btn-custom:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
            .card {
                background-color: #004A7C;
                border-radius: 12px;
                padding: 20px;
                margin: 20px auto;
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                color: white;
            }
            .btn-back {
                background-color: #FFFFFF;
                color: #004289;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                margin-top: 15px;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            .btn-back:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Republic Services Logo" class="logo" width="120">
            <h1 class="my-3">Logistics Dashboard</h1>

            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <h4>Inbound & Outbound Distribution</h4>
                        <canvas id="loadChart"></canvas>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <h4>Trailer Status Overview</h4>
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
            </div>

            <a href="/" class="btn btn-back">Back to Dashboard</a>
        </div>

        <script>
            // Load Distribution Chart
            const ctx1 = document.getElementById('loadChart').getContext('2d');
            new Chart(ctx1, {
                type: 'pie',
                data: {
                    labels: ['Inbound Loads', 'Outbound Loads'],
                    datasets: [{
                        data: [60, 40],
                        backgroundColor: ['#FFC72C', '#004289'],
                    }]
                },
                options: {
                    responsive: true,
                }
            });

            // Trailer Status Chart
            const ctx2 = document.getElementById('statusChart').getContext('2d');
            new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: ['Available', 'Loaded', 'Out of Service', 'Awaiting Pickup'],
                    datasets: [{
                        data: [45, 30, 10, 15],
                        backgroundColor: ['#28a745', '#ffc107', '#dc3545', '#17a2b8'],
                    }]
                },
                options: {
                    responsive: true,
                }
            });
        </script>
    </body>
    </html>
    ''')


@app.route('/inbound_trailers', methods=['GET', 'POST'])
def inbound_trailers():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'inbound_trailers.xlsx')

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=['Trailer ID', 'Carrier', 'ETA', 'Status'])

    if request.method == 'POST':
        trailer_id = request.form['trailer_id']
        carrier = request.form['carrier']
        eta = request.form['eta']
        status = request.form['status']

        new_entry = {'Trailer ID': trailer_id, 'Carrier': carrier, 'ETA': eta, 'Status': status}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(file_path, index=False)

        return redirect(url_for('inbound_trailers'))

    table_html = df.to_html(classes='table table-bordered table-striped', index=False)

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Inbound Trailers</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="container mt-5">
        <h1 class="text-center">Inbound Trailers</h1>
        <form method="POST" class="mt-4 mb-3">
            <div class="mb-3">
                <input type="text" name="trailer_id" class="form-control" placeholder="Trailer ID" required>
            </div>
            <div class="mb-3">
                <input type="text" name="carrier" class="form-control" placeholder="Carrier Name" required>
            </div>
            <div class="mb-3">
                <input type="datetime-local" name="eta" class="form-control" required>
            </div>
            <div class="mb-3">
                <select name="status" class="form-control">
                    <option value="En Route">En Route</option>
                    <option value="Arrived">Arrived</option>
                    <option value="Delayed">Delayed</option>
                </select>
            </div>
            <button type="submit" class="btn btn-success">Add Inbound Trailer</button>
        </form>

        <h3 class="mt-5">Inbound Trailers</h3>
        {{ table_html|safe }}

        <a href="/logistics" class="btn btn-primary mt-3">Back to Logistics</a>
    </body>
    </html>
    ''', table_html=table_html)

@app.route('/outbound_trailers', methods=['GET', 'POST'])
def outbound_trailers():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'outbound_trailers.xlsx')

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=['Trailer ID', 'Destination', 'Departure Time', 'Status'])

    if request.method == 'POST':
        trailer_id = request.form['trailer_id']
        destination = request.form['destination']
        departure_time = request.form['departure_time']
        status = request.form['status']

        new_entry = {'Trailer ID': trailer_id, 'Destination': destination, 'Departure Time': departure_time, 'Status': status}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(file_path, index=False)

        return redirect(url_for('outbound_trailers'))

    table_html = df.to_html(classes='table table-bordered table-striped', index=False)

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Outbound Trailers</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="container mt-5">
        <h1 class="text-center">Outbound Trailers</h1>
        <form method="POST" class="mt-4 mb-3">
            <div class="mb-3">
                <input type="text" name="trailer_id" class="form-control" placeholder="Trailer ID" required>
            </div>
            <div class="mb-3">
                <input type="text" name="destination" class="form-control" placeholder="Destination" required>
            </div>
            <div class="mb-3">
                <input type="datetime-local" name="departure_time" class="form-control" required>
            </div>
            <div class="mb-3">
                <select name="status" class="form-control">
                    <option value="Departed">Departed</option>
                    <option value="In Transit">In Transit</option>
                    <option value="Delivered">Delivered</option>
                </select>
            </div>
            <button type="submit" class="btn btn-success">Add Outbound Trailer</button>
        </form>

        <h3 class="mt-5">Outbound Trailers</h3>
        {{ table_html|safe }}

        <a href="/logistics" class="btn btn-primary mt-3">Back to Logistics</a>
    </body>
    </html>
    ''', table_html=table_html)

@app.route('/trailer_inventory', methods=['GET', 'POST'])
def trailer_inventory():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'trailer_inventory.xlsx')

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=['Trailer ID', 'Type', 'Status', 'Location'])

    if request.method == 'POST':
        trailer_id = request.form['trailer_id']
        trailer_type = request.form['trailer_type']
        status = request.form['status']
        location = request.form['location']

        new_trailer = {'Trailer ID': trailer_id, 'Type': trailer_type, 'Status': status, 'Location': location}
        df = pd.concat([df, pd.DataFrame([new_trailer])], ignore_index=True)
        df.to_excel(file_path, index=False)

        return redirect(url_for('trailer_inventory'))

    table_html = df.to_html(classes='table table-bordered table-striped', index=False)

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trailer Inventory</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="container mt-5">
        <h1 class="text-center">Trailer Inventory</h1>
        <form method="POST" class="mt-4 mb-3">
            <div class="mb-3">
                <input type="text" name="trailer_id" class="form-control" placeholder="Trailer ID" required>
            </div>
            <div class="mb-3">
                <input type="text" name="trailer_type" class="form-control" placeholder="Trailer Type" required>
            </div>
            <div class="mb-3">
                <select name="status" class="form-control">
                    <option value="Available">Available</option>
                    <option value="In Use">In Use</option>
                </select>
            </div>
            <div class="mb-3">
                <input type="text" name="location" class="form-control" placeholder="Location" required>
            </div>
            <button type="submit" class="btn btn-success">Add Trailer</button>
        </form>

        <h3 class="mt-5">Current Trailer Inventory</h3>
        {{ table_html|safe }}

        <a href="/logistics" class="btn btn-primary mt-3">Back to Logistics</a>
    </body>
    </html>
    ''', table_html=table_html)

@app.route('/shipment_schedule', methods=['GET', 'POST'])
def shipment_schedule():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'shipment_schedule.xlsx')

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=['Shipment ID', 'Destination', 'Departure Date', 'Status'])

    if request.method == 'POST':
        shipment_id = request.form['shipment_id']
        destination = request.form['destination']
        departure_date = request.form['departure_date']
        status = request.form['status']

        new_shipment = {'Shipment ID': shipment_id, 'Destination': destination, 'Departure Date': departure_date, 'Status': status}
        df = pd.concat([df, pd.DataFrame([new_shipment])], ignore_index=True)
        df.to_excel(file_path, index=False)

        return redirect(url_for('shipment_schedule'))

    table_html = df.to_html(classes='table table-bordered table-striped', index=False)

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shipment Schedule</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="container mt-5">
        <h1 class="text-center">Shipment Schedule</h1>
        <form method="POST" class="mt-4 mb-3">
            <div class="mb-3">
                <input type="text" name="shipment_id" class="form-control" placeholder="Shipment ID" required>
            </div>
            <div class="mb-3">
                <input type="text" name="destination" class="form-control" placeholder="Destination" required>
            </div>
            <div class="mb-3">
                <input type="date" name="departure_date" class="form-control" required>
            </div>
            <div class="mb-3">
                <select name="status" class="form-control">
                    <option value="Scheduled">Scheduled</option>
                    <option value="In Transit">In Transit</option>
                    <option value="Delivered">Delivered</option>
                </select>
            </div>
            <button type="submit" class="btn btn-success">Add Shipment</button>
        </form>

        <h3 class="mt-5">Shipment Schedule</h3>
        {{ table_html|safe }}

        <a href="/logistics" class="btn btn-primary mt-3">Back to Logistics</a>
    </body>
    </html>
    ''', table_html=table_html)


@app.route('/supervisor', methods=['GET', 'POST'])
def supervisor_review():
    checklist_files = {
        "Forklift": "forklift_checklist.xlsx",
        "Washline": "washline_checklist.xlsx",
        "Crosswrap": "crosswrap_checklist.xlsx",
        "Baler": "baler_checklist.xlsx"
    }

    checklists = {}
    for name, filename in checklist_files.items():
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(path):
            df = pd.read_excel(path)
            checklists[name] = df.to_dict(orient='records')
        else:
            checklists[name] = []

    if request.method == 'POST':
        action = request.form.get('action')
        checklist_name = request.form.get('checklist_name')
        operator = request.form.get('operator')
        date = request.form.get('date')

        # Logging actions (approval/rejection) - you can enhance this later
        print(f"{action.capitalize()} - Checklist: {checklist_name}, Operator: {operator}, Date: {date}")

        # Redirect to refresh the page after action
        return redirect(url_for('supervisor_review'))

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Supervisor Review</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                padding: 20px;
            }
            .logo {
                width: 100px;
                margin: 20px auto;
                cursor: pointer;
            }
            table {
                background-color: white;
                color: black;
            }
            .approve-btn {
                background-color: #28a745;
                color: white;
            }
            .reject-btn {
                background-color: #dc3545;
                color: white;
            }
        </style>
    </head>
    <body>
        <img src="{{ url_for('static', filename='logo.png') }}" class="logo" onclick="window.location.href='/'">
        <h2 class="text-center mb-4">Supervisor Review</h2>

        {% for checklist, entries in checklists.items() %}
            <h4 class="mt-4">{{ checklist }} Submissions</h4>
            {% if entries %}
                <div class="table-responsive">
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Operator</th>
                                <th>Date</th>
                                <th>Notes</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for entry in entries %}
                            <tr>
                                <td>{{ entry['Operator'] }}</td>
                                <td>{{ entry['Date'] }}</td>
                                <td>{{ entry.get('Notes', '') }}</td>
                                <td>
                                    <form method="POST">
                                        <input type="hidden" name="checklist_name" value="{{ checklist }}">
                                        <input type="hidden" name="operator" value="{{ entry['Operator'] }}">
                                        <input type="hidden" name="date" value="{{ entry['Date'] }}">
                                        <button name="action" value="approved" class="btn approve-btn btn-sm">Approve</button>
                                        <button name="action" value="rejected" class="btn reject-btn btn-sm">Reject</button>
                                    </form>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p>No submissions yet.</p>
            {% endif %}
        {% endfor %}
        <a href="/" class="btn btn-secondary mt-3">Back to Home</a>
    </body>
    </html>
    ''', checklists=checklists)

@app.route('/maintenance')
def maintenance_dashboard():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Maintenance Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding-top: 30px;
                padding-bottom: 20px;
            }
            .logo {
                width: 120px;
                margin: 0 auto 20px;
                display: block;
            }
            h1 {
                font-size: 24px;
                margin-bottom: 20px;
                text-align: center;
            }
            .nav-button {
                background-color: #FFC72C;
                color: #004289;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                margin: 10px auto;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                width: 90%;
                max-width: 400px;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .nav-button:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
            .btn-back {
                background-color: #FFFFFF;
                color: #004289;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                margin-top: 15px;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .btn-back:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
            footer {
                margin-top: 40px;
                font-size: 13px;
                color: rgba(255,255,255,0.7);
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Republic Services Logo" class="logo">
            <h1>Maintenance Dashboard</h1>
            
            <div class="d-flex flex-column align-items-center">
                <a href="/work_orders" class="nav-button">Work Orders</a>
                <a href="/scheduled_pms" class="nav-button">Scheduled PMs</a>
                <a href="/repairs_outoforder" class="nav-button">Repairs & Out of Order</a>
                <a href="/storage_inventory" class="nav-button">Storage & Inventory Items</a>
                <a href="/" class="btn-back">Back to Dashboard</a>
            </div>

            <footer>A work in progress by Reginald Turner</footer>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    ''')
### ------------------ WORK ORDERS ------------------ ###
@app.route('/work_orders')
def work_orders():
    work_orders_data = [
        {"ID": 101, "Task": "Replace Belt", "Status": "In Progress", "Due Date": "2025-04-01"},
        {"ID": 102, "Task": "Inspect Hydraulic System", "Status": "Pending", "Due Date": "2025-04-05"},
        {"ID": 103, "Task": "Repair Conveyor Motor", "Status": "Completed", "Due Date": "2025-03-28"},
    ]
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Work Orders</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #003DA5; color: white; font-family: Arial, sans-serif; }
            .container { margin-top: 20px; }
            h1 { color: #FFC72C; }
            .table { background-color: white; color: black; border-radius: 10px; overflow: hidden; }
            .btn-back { margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Work Orders</h1>
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Task</th>
                        <th>Status</th>
                        <th>Due Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for order in work_orders_data %}
                    <tr>
                        <td>{{ order.ID }}</td>
                        <td>{{ order.Task }}</td>
                        <td>{{ order.Status }}</td>
                        <td>{{ order['Due Date'] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <a href="/maintenance" class="btn btn-warning btn-back">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''', work_orders_data=work_orders_data)

### ------------------ SCHEDULED PMs ------------------ ###
@app.route('/scheduled_pms')
def scheduled_pms():
    pms_data = [
        {"ID": 201, "Equipment": "Forklift #3", "Task": "Check Brake Fluid", "Date": "2025-04-05"},
        {"ID": 202, "Equipment": "Baler", "Task": "Lubricate Bearings", "Date": "2025-04-10"},
        {"ID": 203, "Equipment": "Washline System", "Task": "Inspect Filter", "Date": "2025-04-15"},
    ]
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Scheduled PMs</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #003DA5; color: white; font-family: Arial, sans-serif; }
            .container { margin-top: 20px; }
            h1 { color: #FFC72C; }
            .table { background-color: white; color: black; border-radius: 10px; overflow: hidden; }
            .btn-back { margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Scheduled PMs</h1>
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Equipment</th>
                        <th>Task</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for pm in pms_data %}
                    <tr>
                        <td>{{ pm.ID }}</td>
                        <td>{{ pm.Equipment }}</td>
                        <td>{{ pm.Task }}</td>
                        <td>{{ pm.Date }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <a href="/maintenance" class="btn btn-warning btn-back">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''', pms_data=pms_data)

### ------------------ REPAIRS & OUT OF ORDER ------------------ ###
@app.route('/repairs_outoforder')
def repairs_outoforder():
    repairs_data = [
        {"ID": 301, "Equipment": "Crosswrap Machine", "Status": "Out of Order", "Reported Date": "2025-03-25"},
        {"ID": 302, "Equipment": "Forklift #2", "Status": "In Repair", "Reported Date": "2025-03-20"},
    ]
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repairs & Out of Order</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #003DA5; color: white; font-family: Arial, sans-serif; }
            .container { margin-top: 20px; }
            h1 { color: #FFC72C; }
            .table { background-color: white; color: black; border-radius: 10px; overflow: hidden; }
            .btn-back { margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Repairs & Out of Order</h1>
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Equipment</th>
                        <th>Status</th>
                        <th>Reported Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for repair in repairs_data %}
                    <tr>
                        <td>{{ repair.ID }}</td>
                        <td>{{ repair.Equipment }}</td>
                        <td>{{ repair.Status }}</td>
                        <td>{{ repair['Reported Date'] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <a href="/maintenance" class="btn btn-warning btn-back">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''', repairs_data=repairs_data)

### ------------------ STORAGE & INVENTORY ------------------ ###
@app.route('/storage_inventory')
def storage_inventory():
    inventory_data = [
        {"ID": 401, "Item": "Baler Belt", "Quantity": 12, "Location": "Warehouse A"},
        {"ID": 402, "Item": "Hydraulic Fluid", "Quantity": 25, "Location": "Storage 2"},
        {"ID": 403, "Item": "Forklift Tires", "Quantity": 8, "Location": "Warehouse B"},
    ]
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Storage & Inventory</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #003DA5; color: white; font-family: Arial, sans-serif; }
            .container { margin-top: 20px; }
            h1 { color: #FFC72C; }
            .table { background-color: white; color: black; border-radius: 10px; overflow: hidden; }
            .btn-back { margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Storage & Inventory</h1>
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Item</th>
                        <th>Quantity</th>
                        <th>Location</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in inventory_data %}
                    <tr>
                        <td>{{ item.ID }}</td>
                        <td>{{ item.Item }}</td>
                        <td>{{ item.Quantity }}</td>
                        <td>{{ item.Location }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <a href="/maintenance" class="btn btn-warning btn-back">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''', inventory_data=inventory_data)

@app.route('/work_orders')
def work_orders():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Work Orders</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding-top: 30px;
                padding-bottom: 20px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
            }
            .content-box {
                background-color: #004A7C;
                border-radius: 15px;
                padding: 20px;
                margin: 20px auto;
                width: 90%;
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            }
            .btn-back {
                background-color: #FFC72C;
                color: #003DA5;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                width: 90%;
                max-width: 400px;
                margin-top: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            .btn-back:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Work Orders</h1>
            <div class="content-box">
                <p>✅ List of all open and completed work orders will be displayed here.</p>
            </div>
            <a href="/maintenance" class="btn btn-back">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''')

@app.route('/scheduled_pms')
def scheduled_pms():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Scheduled PMs</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding-top: 30px;
                padding-bottom: 20px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
            }
            .content-box {
                background-color: #004A7C;
                border-radius: 15px;
                padding: 20px;
                margin: 20px auto;
                width: 90%;
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            }
            .btn-back {
                background-color: #FFC72C;
                color: #003DA5;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                width: 90%;
                max-width: 400px;
                margin-top: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            .btn-back:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Scheduled PMs</h1>
            <div class="content-box">
                <p>🛠️ View all upcoming preventive maintenance tasks here.</p>
            </div>
            <a href="/maintenance" class="btn btn-back">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''')

@app.route('/repairs_outoforder')
def repairs_outoforder():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Repairs & Out of Order</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding-top: 30px;
                padding-bottom: 20px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
            }
            .content-box {
                background-color: #004A7C;
                border-radius: 15px;
                padding: 20px;
                margin: 20px auto;
                width: 90%;
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            }
            .btn-back {
                background-color: #FFC72C;
                color: #003DA5;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                width: 90%;
                max-width: 400px;
                margin-top: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            .btn-back:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Repairs & Out of Order</h1>
            <div class="content-box">
                <p>⚙️ Track machines that are under repair or out of order.</p>
            </div>
            <a href="/maintenance" class="btn btn-back">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''')

@app.route('/storage_inventory')
def storage_inventory():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Storage & Inventory</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding-top: 30px;
                padding-bottom: 20px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
            }
            .content-box {
                background-color: #004A7C;
                border-radius: 15px;
                padding: 20px;
                margin: 20px auto;
                width: 90%;
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            }
            .btn-back {
                background-color: #FFC72C;
                color: #003DA5;
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                width: 90%;
                max-width: 400px;
                margin-top: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            .btn-back:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Storage & Inventory</h1>
            <div class="content-box">
                <p>📦 View available inventory and storage space details.</p>
            </div>
            <a href="/maintenance" class="btn btn-back">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''')

