from flask_mail import Mail, Message
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev_secret")

DB = "database.db"
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "youremail@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your_app_password"),
    MAIL_USE_TLS=True
)

mail = Mail(app)

def get_db_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn 

@app.route("/")
def home():
    conn = get_db_conn()
    opportunities = conn.execute("""
        SELECT o.*, org.name as org_name 
        FROM opportunities o
        JOIN organisations org ON o.org_id = org.id
        ORDER BY o.created_at DESC
    """).fetchall()
    conn.close()
    return render_template("opportunities.html", opportunities=opportunities)

@app.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    if request.method == "POST":
        name = request.form.get("name") 
        email = request.form.get("email") 
        skills = request.form.get("skills") 
        interests = request.form.get("interests", "")
        availability = request.form.get("availability") 

        conn = get_db_conn()
        conn.execute("""
            INSERT INTO volunteers (name, email, skills, interests, availability) 
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, skills, interests, availability))
        conn.commit()
        conn.close()

        flash("Volunteer registered. Thank you!")
        return redirect(url_for("home"))

    return render_template("volunteer.html")

@app.route("/org/post", methods=["GET", "POST"])
def org_post():
    if request.method == "POST":
        name = request.form.get("org_name") 
        email = request.form.get("email") 
        desc = request.form.get("description") 
        file = request.files.get("verification_doc")  
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = get_db_conn()
        conn.execute("""
            INSERT INTO organisations (name, email, description) 
            VALUES (?, ?, ?)
        """, (name, email, desc))
        conn.commit()
        conn.close()

        flash("Organisation submitted for approval.")
        return redirect(url_for("home"))

    return render_template("org_post.html")

@app.route("/apply", methods=["POST"])
def apply():
    volunteer_id = request.form.get("volunteer_id")
    opp_id = request.form.get("opportunity_id")

    conn = get_db_conn()
    conn.execute("INSERT INTO applications (volunteer_id, opportunity_id) VALUES (?, ?)", 
                 (volunteer_id, opp_id))
    
    volunteer = conn.execute("SELECT * FROM volunteers WHERE id=?", (volunteer_id,)).fetchone()
    opp = conn.execute("SELECT * FROM opportunities WHERE id=?", (opp_id,)).fetchone()
    org = conn.execute("SELECT * FROM organisations WHERE id=?", (opp["org_id"],)).fetchone()
    
    conn.commit()
    conn.close()

    if org and volunteer:
        msg = Message(
            "New Volunteer Application",
            sender=app.config['MAIL_USERNAME'],
            recipients=[org["email"]]
        )
        msg.body = f"{volunteer['name']} ({volunteer['email']}) applied for {opp['title']}."
        mail.send(msg)

    flash("Applied - organization will be notified.")
    return redirect(url_for("home"))

@app.route("/admin/orgs")
def admin_orgs():
    conn = get_db_conn()
    orgs = conn.execute("SELECT * FROM organisations WHERE verified=0").fetchall()
    conn.close()
    return render_template("admin_orgs.html", orgs=orgs)

@app.route("/admin/verify/<int:org_id>")
def verify_org(org_id):
    conn = get_db_conn()
    conn.execute("UPDATE organisations SET verified=1 WHERE id=?", (org_id,))
    conn.commit()
    conn.close()
    flash("Organization verified!")
    return redirect(url_for("admin_orgs"))

if __name__ == "_main_":
    app.run(debug=True)