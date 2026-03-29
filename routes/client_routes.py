from flask import render_template, request, redirect, session, Blueprint
from models.db import init_db, get_connection

client_bp = Blueprint("client", __name__)

init_db()


# ---------- DASHBOARD ----------
@client_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    clients = cur.fetchall()
    conn.close()

    return render_template("dashboard.html",
                           clients=clients,
                           session_user=session["user"])


# ---------- DELETE CLIENT ----------
@client_bp.route("/delete_client/<int:id>")
def delete_client(id):
    if "user" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clients WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")