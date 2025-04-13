from flask import Flask, render_template, redirect, url_for, session, request
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class Node:
    def __init__(self, url):
        self.url = url
        self.prev = None
        self.next = None

class HistoryManager:
    def __init__(self):
        self.head = None
        self.current = None

    def visit(self, url):
        new_node = Node(url)
        if self.current:
            self.current.next = new_node
            new_node.prev = self.current
        else:
            self.head = new_node
        self.current = new_node

    def back(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        return self.current.url if self.current else None

    def forward(self):
        if self.current and self.current.next:
            self.current = self.current.next
        return self.current.url if self.current else None

    def get_history(self):
        history = []
        temp = self.head
        while temp:
            history.append(temp.url)
            temp = temp.next
        return history

history_manager = HistoryManager()

MOCK_DATA = {
    "tabs_used": 12,
    "most_visited": "YouTube",
    "average_time": "2.4 min",
    "longest_session": "45 min",
    "least_used": "Reddit",
    "used_time": "5 hrs 30 mins",
    "saved_sessions": 4,
    "insights": "You're most productive in the morning!",
    "labels": ["YouTube", "Gmail", "GitHub", "Google", "ChatGPT"],
    "data": [2.5, 1.2, 0.8, 0.6, 0.4]
}

@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple mock login check
        if username == "Hazel" and password == "password":  # Replace with real authentication
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return "<h1 style='color:white;'>Invalid credentials, try again!</h1>"

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('landing'))  # Redirect to the landing page if not logged in

    history_manager.visit('/dashboard')
    return render_template("dashboard.html",
        username="Hazel",
        used_time=MOCK_DATA["used_time"],
        saved_sessions=MOCK_DATA["saved_sessions"],
        insights=MOCK_DATA["insights"],
        tabs_used=MOCK_DATA["tabs_used"],
        most_visited=MOCK_DATA["most_visited"],
        average_time=MOCK_DATA["average_time"],
        longest_session=MOCK_DATA["longest_session"],
        least_used=MOCK_DATA["least_used"],
        labels=MOCK_DATA["labels"],
        data=MOCK_DATA["data"]
    )

@app.route('/about')
def about():
    history_manager.visit('/about')
    return "<h1 style='color:white;'>About WebWiz</h1>"

@app.route('/how-it-works')
def how_it_works():
    history_manager.visit('/how-it-works')
    return "<h1 style='color:white;'>WebWiz tracks your browser tab activity and gives productivity insights!</h1>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/save_session', methods=['POST'])
def save_session():
    MOCK_DATA["saved_sessions"] += 1
    return redirect(url_for('dashboard'))

@app.route('/history')
def view_history():
    return {
        "history": history_manager.get_history(),
        "current": history_manager.current.url if history_manager.current else None
    }

@app.route('/back')
def go_back():
    return {"navigated_to": history_manager.back()}

@app.route('/forward')
def go_forward():
    return {"navigated_to": history_manager.forward()}

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not session.get('logged_in'):
        return redirect(url_for('landing'))

    if request.method == 'POST':
        if 'clear_history' in request.form:
            history_manager = HistoryManager()
        elif 'disable_tracking' in request.form:
            session['tracking_enabled'] = False 
        elif 'enable_tracking' in request.form:
            session['tracking_enabled'] = True
        elif 'change_password' in request.form:
            #password change logic
            new_password = request.form['new_password']
            #mock password change 
            return "<h1 style='color:white;'>Password changed successfully!</h1>"
    tracking_status = session.get('tracking_enabled', True)

    return render_template("settings.html", tracking_status=tracking_status)

@app.route('/tools')
def tools():
    return render_template('tools.html')

if __name__ == '__main__':
    app.run(debug=True)

