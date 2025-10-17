from flask import Flask, render_template, request, redirect, session
import time, sqlite3
from otp import generate_otp, send_otp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_PATH = "/data/users.db"  # ✅ Path to SQLite DB on Render Disk

# 🔧 Helper to connect to the DB
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        password = request.form["password"]

        # 🔍 Check if email already exists
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return "⚠️ This Gmail is already registered!"

        # ✅ Generate OTP and send email
        otp, timestamp = generate_otp()
        send_otp(email, otp)

        # Store in session for verification
        session.update({
            "email": email,
            "password": password,
            "otp": otp,
            "time": timestamp,
            "name": name,
            "age": age
        })
        return redirect("/verify")
    return render_template("register.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        user_otp = request.form["otp"]
        sent_otp = session["otp"]
        sent_time = session["time"]

        if time.time() - sent_time > 120:
            return "⏰ OTP expired. Go back and try again."
        elif user_otp == sent_otp:
            # ✅ Save verified user to DB
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, age, email, password) VALUES (?, ?, ?, ?)",
                (session["name"], session["age"], session["email"], session["password"])
            )
            conn.commit()
            conn.close()

            send_success_email(session["email"], session["name"])
            return "✅ Registered successfully !"
        else:
            return "❌ Incorrect OTP!"
    return render_template("verify.html")

# ✉️ Send welcome mail after successful registration
def send_success_email(receiver_email, name):
    import smtplib
    sender_email = "420la007@gmail.com"
    sender_password = "otvr frxa rpxl ltjs"  # App password

    message = f"""Subject: Welcome to Our App 🎉

Hello {name},

🎉 Congratulations! You have successfully registered.
We are excited to have you on board.

Stay tuned for more updates.

Warm regards,
The Team
"""

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        print(f"Confirmation email sent to {receiver_email}")
    except Exception as e:
        print("Failed to send confirmation email:", e)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
