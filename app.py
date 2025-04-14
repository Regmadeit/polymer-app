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

@app.route('/logistics', methods=['GET', 'POST'])
def logistics_dashboard():
    if request.method == 'POST':
        # Handle form data
        trailer_num = request.form.get('trailer_number')
        status = request.form.get('status')
        contents = request.form.get('contents')
        buyer = request.form.get('buyer')
        direction = request.form.get('direction')
        time = request.form.get('time')
        
        print(f"📦 Trailer {trailer_num} - {status} - {contents} - {buyer} - {direction} at {time}")

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
            .logo {
                width: 100px;
                display: block;
                margin: auto;
            }
            h1 {
                font-size: 26px;
                text-align: center;
                margin-top: 20px;
            }
            label {
                font-weight: bold;
            }
            .form-section {
                background-color: #004A7C;
                padding: 20px;
                margin: 15px;
                border-radius: 10px;
            }
            .btn-submit {
                background-color: #FFC72C;
                color: #004289;
                font-weight: bold;
                border-radius: 12px;
                width: 100%;
            }
            canvas {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
            .btn-back {
                background-color: white;
                color: #004289;
                border-radius: 12px;
                font-weight: bold;
                padding: 10px;
                width: 100%;
                max-width: 400px;
                margin: 20px auto;
                display: block;
            }
        </style>
    </head>
    <body>
        <img src="{{ url_for('static', filename='logo.png') }}" alt="Republic Services Logo" class="logo">
        <h1>Logistics Dashboard</h1>

        <div class="form-section container">
            <form method="POST">
                <div class="mb-3">
                    <label for="trailer_number">Trailer Number</label>
                    <input type="text" class="form-control" id="trailer_number" name="trailer_number" required>
                </div>
                <div class="mb-3">
                    <label for="status">Status</label>
                    <select class="form-control" id="status" name="status" required>
                        <option value="Empty">Empty</option>
                        <option value="Loaded">Loaded</option>
                        <option value="Discrepancy">Discrepancy</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="contents">Contents</label>
                    <select class="form-control" id="contents" name="contents" required>
                        <option value="PP Other">PP Other</option>
                        <option value="PET Color">PET Color</option>
                        <option value="HD Color (Raw Material)">HD Color (Raw Material)</option>
                        <option value="PET Clear Flake">PET Clear Flake</option>
                        <option value="Flake Fines">Flake Fines</option>
                        <option value="Flake Caps & Rings">Flake Caps & Rings</option>
                        <option value="Flake Reject">Flake Reject</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="buyer">Buyer Name</label>
                    <input type="text" class="form-control" id="buyer" name="buyer">
                </div>
                <div class="mb-3">
                    <label for="direction">Inbound/Outbound</label>
                    <select class="form-control" id="direction" name="direction">
                        <option value="Inbound">Inbound</option>
                        <option value="Outbound">Outbound</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="time">Expected Time</label>
                    <input type="time" class="form-control" id="time" name="time">
                </div>
                <button type="submit" class="btn btn-submit mt-3">Submit Trailer Entry</button>
            </form>
        </div>

        <div class="container mt-5">
            <h2 class="text-center mb-3">Commodity Summary Chart</h2>
            <canvas id="logisticsChart" height="200"></canvas>
        </div>

        <a href="/" class="btn-back">Back to Dashboard</a>

        <script>
            const ctx = document.getElementById('logisticsChart').getContext('2d');
            const logisticsChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['PP Other', 'PET Color', 'HD Color', 'PET Clear Flake', 'Flake Fines', 'Caps & Rings', 'Reject'],
                    datasets: [{
                        label: 'Trailer Counts',
                        data: [4, 2, 1, 3, 1, 0, 2],
                        backgroundColor: '#FFC72C',
                        borderColor: '#004A7C',
                        borderWidth: 2
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                color: '#003DA5'
                            }
                        },
                        x: {
                            ticks: {
                                color: '#003DA5'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: '#003DA5'
                            }
                        }
                    }
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
                font-weight: bold;
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
                <a href="/repairs_out_of_order" class="nav-button">Repairs & Out of Order</a>
                <a href="/storage_inventory" class="nav-button">Storage & Inventory</a>
                <a href="/" class="btn-back">Back to Dashboard</a>
            </div>

            <footer>
                <p class="mt-4">A work in progress by Reginald Turner</p>
            </footer>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    ''')


# Store active work orders as a global list
active_work_orders = []

@app.route('/work_orders', methods=['GET', 'POST'])
def work_orders():
    if request.method == 'POST':
        # Capture form data
        form_data = {
            'equipment_name': request.form['equipment_name'],
            'issue_description': request.form['issue_description'],
            'priority_level': request.form['priority_level'],
            'submitted_by': request.form['submitted_by'],
            'date_submitted': request.form['date_submitted']
        }
        
        # Add form data to active work orders
        active_work_orders.append(form_data)
        print(f"New Work Order Submitted: {form_data}")

        # Redirect back to work orders page to refresh the list
        return redirect(url_for('work_orders'))

    # Render the Work Orders form with active orders
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
            }
            .container {
                margin-top: 20px;
            }
            .form-container {
                background-color: #004A7C;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                margin-bottom: 20px;
                width: 90%;
                max-width: 500px;
                margin-left: auto;
                margin-right: auto;
            }
            .btn-submit {
                background-color: #FFC72C;
                color: #003DA5;
                padding: 15px;
                border-radius: 12px;
                width: 100%;
                font-weight: bold;
                margin-top: 15px;
            }
            .btn-back {
                background-color: #FFFFFF;
                color: #004289;
                border-radius: 12px;
                padding: 15px;
                margin-top: 15px;
                width: 100%;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                font-weight: bold;
            }
            .active-orders {
                background-color: #FFC72C;
                border-radius: 12px;
                padding: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                margin-top: 20px;
                width: 90%;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            .order-item {
                background-color: #004A7C;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
                color: white;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1 class="mb-4">Work Orders</h1>

            <!-- Work Order Form -->
            <div class="form-container">
                <form method="POST">
                    <div class="mb-3 text-start">
                        <label class="form-label">Equipment Name</label>
                        <input type="text" name="equipment_name" class="form-control" required>
                    </div>
                    
                    <div class="mb-3 text-start">
                        <label class="form-label">Issue Description</label>
                        <textarea name="issue_description" class="form-control" rows="3" required></textarea>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Priority Level</label>
                        <select name="priority_level" class="form-control">
                            <option value="Low">Low</option>
                            <option value="Medium">Medium</option>
                            <option value="High">High</option>
                        </select>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Submitted By</label>
                        <input type="text" name="submitted_by" class="form-control" required>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Date Submitted</label>
                        <input type="date" name="date_submitted" class="form-control" required>
                    </div>

                    <button type="submit" class="btn-submit">Submit Work Order</button>
                </form>
            </div>

            <!-- Active Work Orders Section -->
            <div class="active-orders">
                <h3 class="text-center">Active Work Orders</h3>
                {% if active_work_orders %}
                    {% for order in active_work_orders %}
                        <div class="order-item">
                            <p><strong>Equipment:</strong> {{ order['equipment_name'] }}</p>
                            <p><strong>Description:</strong> {{ order['issue_description'] }}</p>
                            <p><strong>Priority:</strong> {{ order['priority_level'] }}</p>
                            <p><strong>Submitted By:</strong> {{ order['submitted_by'] }}</p>
                            <p><strong>Date:</strong> {{ order['date_submitted'] }}</p>
                        </div>
                    {% endfor %}
                {% else %}
                    <p>No active work orders available.</p>
                {% endif %}
            </div>

            <a href="/maintenance" class="btn-back mt-4">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''', active_work_orders=active_work_orders)

# Store scheduled PMs in a list
scheduled_pms_list = [
    {'equipment': 'Krones Side - Conveyor 1', 'due_date': '2025-04-01', 'status': 'Pending'},
    {'equipment': 'Stadler Side - Feeder Motor', 'due_date': '2025-04-02', 'status': 'In Progress'},
    {'equipment': 'Washline - Pump 2', 'due_date': '2025-04-05', 'status': 'Pending'}
]

# Store completed PMs
completed_pms_list = []

@app.route('/scheduled_pms', methods=['GET', 'POST'])
def scheduled_pms():
    if request.method == 'POST':
        # Capture form data for completed PM
        completed_pm = {
            'equipment': request.form['equipment'],
            'completed_by': request.form['completed_by'],
            'completion_date': request.form['completion_date'],
            'notes': request.form['notes']
        }
        
        # Add completed PM to the list
        completed_pms_list.append(completed_pm)
        print(f"Completed PM Submitted: {completed_pm}")
        
        return redirect(url_for('scheduled_pms'))

    # Render the Scheduled PMs page
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
            }
            .container {
                margin-top: 20px;
            }
            .content-box {
                background-color: #004A7C;
                border-radius: 12px;
                padding: 20px;
                margin-top: 15px;
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                width: 90%;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            .btn-submit {
                background-color: #FFC72C;
                color: #003DA5;
                padding: 15px;
                border-radius: 12px;
                width: 100%;
                font-weight: bold;
                margin-top: 15px;
            }
            .btn-back {
                background-color: #FFFFFF;
                color: #004289;
                border-radius: 12px;
                padding: 15px;
                width: 90%;
                max-width: 400px;
                font-weight: bold;
                margin-top: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            .pm-item {
                background-color: #FFC72C;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
                color: #003DA5;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Scheduled PMs</h1>

            <!-- Scheduled PMs List -->
            <div class="content-box">
                <h3>Upcoming Scheduled PMs</h3>
                {% for pm in scheduled_pms_list %}
                    <div class="pm-item">
                        <p><strong>Equipment:</strong> {{ pm['equipment'] }}</p>
                        <p><strong>Due Date:</strong> {{ pm['due_date'] }}</p>
                        <p><strong>Status:</strong> {{ pm['status'] }}</p>
                    </div>
                {% else %}
                    <p>No scheduled PMs available.</p>
                {% endfor %}
            </div>

            <!-- PM Completion Form -->
            <div class="content-box mt-4">
                <h3>Log Completed PM</h3>
                <form method="POST">
                    <div class="mb-3 text-start">
                        <label class="form-label">Equipment Name</label>
                        <input type="text" name="equipment" class="form-control" required>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Completed By</label>
                        <input type="text" name="completed_by" class="form-control" required>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Completion Date</label>
                        <input type="date" name="completion_date" class="form-control" required>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Notes (Optional)</label>
                        <textarea name="notes" class="form-control" rows="3"></textarea>
                    </div>

                    <button type="submit" class="btn-submit">Submit Completed PM</button>
                </form>
            </div>

            <!-- Completed PMs List -->
            <div class="content-box mt-4">
                <h3>Completed PMs</h3>
                {% if completed_pms_list %}
                    {% for completed in completed_pms_list %}
                        <div class="pm-item">
                            <p><strong>Equipment:</strong> {{ completed['equipment'] }}</p>
                            <p><strong>Completed By:</strong> {{ completed['completed_by'] }}</p>
                            <p><strong>Completion Date:</strong> {{ completed['completion_date'] }}</p>
                            <p><strong>Notes:</strong> {{ completed['notes'] }}</p>
                        </div>
                    {% endfor %}
                {% else %}
                    <p>No completed PMs available.</p>
                {% endif %}
            </div>

            <a href="/maintenance" class="btn-back mt-4">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''', scheduled_pms_list=scheduled_pms_list, completed_pms_list=completed_pms_list)

# Store repairs and out-of-order records
repair_records = []
out_of_order_records = [
    {'equipment': 'Krones Side - Conveyor 2', 'status': 'Out of Order', 'reported_by': 'John Doe', 'date': '2025-03-28', 'notes': 'Motor malfunction'},
    {'equipment': 'Stadler Side - Feeder Motor', 'status': 'In Repair', 'reported_by': 'Mike Smith', 'date': '2025-03-27', 'notes': 'Awaiting new parts'}
]

@app.route('/repairs_out_of_order', methods=['GET', 'POST'])
def repairs_out_of_order():
    if request.method == 'POST':
        # Capture form data for new repairs
        repair_data = {
            'equipment': request.form['equipment'],
            'status': request.form['status'],
            'reported_by': request.form['reported_by'],
            'date': request.form['date'],
            'notes': request.form['notes']
        }
        
        # Add repair data to the list
        out_of_order_records.append(repair_data)
        print(f"New Repair Submitted: {repair_data}")
        
        return redirect(url_for('repairs_out_of_order'))

    # Render the Repairs & Out of Order page
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
            }
            .container {
                margin-top: 20px;
            }
            .content-box {
                background-color: #004A7C;
                border-radius: 12px;
                padding: 20px;
                margin-top: 15px;
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                width: 90%;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            .btn-submit {
                background-color: #FFC72C;
                color: #003DA5;
                padding: 15px;
                border-radius: 12px;
                width: 100%;
                font-weight: bold;
                margin-top: 15px;
            }
            .btn-back {
                background-color: #FFFFFF;
                color: #004289;
                border-radius: 12px;
                padding: 15px;
                width: 90%;
                max-width: 400px;
                font-weight: bold;
                margin-top: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            .record-item {
                background-color: #FFC72C;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
                color: #003DA5;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Repairs & Out of Order</h1>

            <!-- List of Repairs & Out of Order -->
            <div class="content-box">
                <h3>Current Out of Order / In Repair</h3>
                {% for record in out_of_order_records %}
                    <div class="record-item">
                        <p><strong>Equipment:</strong> {{ record['equipment'] }}</p>
                        <p><strong>Status:</strong> {{ record['status'] }}</p>
                        <p><strong>Reported By:</strong> {{ record['reported_by'] }}</p>
                        <p><strong>Date:</strong> {{ record['date'] }}</p>
                        <p><strong>Notes:</strong> {{ record['notes'] }}</p>
                    </div>
                {% else %}
                    <p>No current repairs or out-of-order records.</p>
                {% endfor %}
            </div>

            <!-- Add New Repair / Out of Order -->
            <div class="content-box mt-4">
                <h3>Report New Repair or Out of Order</h3>
                <form method="POST">
                    <div class="mb-3 text-start">
                        <label class="form-label">Equipment Name</label>
                        <input type="text" name="equipment" class="form-control" required>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Status</label>
                        <select name="status" class="form-control" required>
                            <option value="Out of Order">Out of Order</option>
                            <option value="In Repair">In Repair</option>
                            <option value="Back in Service">Back in Service</option>
                        </select>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Reported By</label>
                        <input type="text" name="reported_by" class="form-control" required>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Date Reported</label>
                        <input type="date" name="date" class="form-control" required>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Notes (Optional)</label>
                        <textarea name="notes" class="form-control" rows="3"></textarea>
                    </div>

                    <button type="submit" class="btn-submit">Submit Repair / Out of Order</button>
                </form>
            </div>

            <a href="/maintenance" class="btn-back mt-4">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''', out_of_order_records=out_of_order_records)

# Store inventory records
inventory_records = [
    {'item': 'Hydraulic Hose', 'quantity': 10, 'location': 'Maintenance Room 1', 'status': 'In Stock', 'last_updated': '2025-03-28'},
    {'item': 'Conveyor Belt Roll', 'quantity': 5, 'location': 'Storage Area A', 'status': 'In Stock', 'last_updated': '2025-03-27'}
]

@app.route('/storage_inventory', methods=['GET', 'POST'])
def storage_inventory():
    if request.method == 'POST':
        # Capture form data for new inventory submission
        inventory_data = {
            'item': request.form['item'],
            'quantity': int(request.form['quantity']),
            'location': request.form['location'],
            'status': request.form['status'],
            'last_updated': request.form['last_updated']
        }

        # Add inventory data to the list
        inventory_records.append(inventory_data)
        print(f"New Inventory Item Added: {inventory_data}")
        
        return redirect(url_for('storage_inventory'))

    # Render the Storage & Inventory page
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Storage & Inventory Items</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #003DA5;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .container {
                margin-top: 20px;
            }
            .content-box {
                background-color: #004A7C;
                border-radius: 12px;
                padding: 20px;
                margin-top: 15px;
                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                width: 90%;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            .btn-submit {
                background-color: #FFC72C;
                color: #003DA5;
                padding: 15px;
                border-radius: 12px;
                width: 100%;
                font-weight: bold;
                margin-top: 15px;
            }
            .btn-back {
                background-color: #FFFFFF;
                color: #004289;
                border-radius: 12px;
                padding: 15px;
                width: 90%;
                max-width: 400px;
                font-weight: bold;
                margin-top: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            .record-item {
                background-color: #FFC72C;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
                color: #003DA5;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>Storage & Inventory Items</h1>

            <!-- List of Inventory Items -->
            <div class="content-box">
                <h3>Available Inventory</h3>
                {% for record in inventory_records %}
                    <div class="record-item">
                        <p><strong>Item:</strong> {{ record['item'] }}</p>
                        <p><strong>Quantity:</strong> {{ record['quantity'] }}</p>
                        <p><strong>Location:</strong> {{ record['location'] }}</p>
                        <p><strong>Status:</strong> {{ record['status'] }}</p>
                        <p><strong>Last Updated:</strong> {{ record['last_updated'] }}</p>
                    </div>
                {% else %}
                    <p>No inventory records available.</p>
                {% endfor %}
            </div>

            <!-- Add New Inventory Item -->
            <div class="content-box mt-4">
                <h3>Add New Inventory Item</h3>
                <form method="POST">
                    <div class="mb-3 text-start">
                        <label class="form-label">Item Name</label>
                        <input type="text" name="item" class="form-control" required>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Quantity</label>
                        <input type="number" name="quantity" class="form-control" required>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Location</label>
                        <input type="text" name="location" class="form-control" required>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Status</label>
                        <select name="status" class="form-control" required>
                            <option value="In Stock">In Stock</option>
                            <option value="Out of Stock">Out of Stock</option>
                            <option value="Pending Delivery">Pending Delivery</option>
                        </select>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Last Updated</label>
                        <input type="date" name="last_updated" class="form-control" required>
                    </div>

                    <button type="submit" class="btn-submit">Add Inventory Item</button>
                </form>
            </div>

            <a href="/maintenance" class="btn-back mt-4">Back to Maintenance</a>
        </div>
    </body>
    </html>
    ''', inventory_records=inventory_records)


