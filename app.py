import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "service_orders.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-me"


STATUS_OPTIONS = ["Pendiente", "En progreso", "Completada", "Cancelada"]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS service_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT NOT NULL UNIQUE,
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendiente',
            created_at TEXT NOT NULL
        );
        """
    )
    db.commit()
    db.close()


def validate_form(reference, company, description, status):
    errors = []
    if not reference.strip():
        errors.append("La referencia es obligatoria.")
    if not company.strip():
        errors.append("La empresa es obligatoria.")
    if not description.strip():
        errors.append("La descripción es obligatoria.")
    if status not in STATUS_OPTIONS:
        errors.append("Estado no válido.")
    return errors


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    db = get_db()

    if query:
        like_query = f"%{query}%"
        orders = db.execute(
            """
            SELECT * FROM service_orders
            WHERE reference LIKE ? OR company LIKE ? OR description LIKE ?
            ORDER BY id DESC
            """,
            (like_query, like_query, like_query),
        ).fetchall()
    else:
        orders = db.execute(
            "SELECT * FROM service_orders ORDER BY id DESC"
        ).fetchall()

    return render_template("index.html", orders=orders, query=query)


@app.route("/orders/new", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        reference = request.form.get("reference", "")
        company = request.form.get("company", "")
        description = request.form.get("description", "")
        status = request.form.get("status", "Pendiente")

        errors = validate_form(reference, company, description, status)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "form.html",
                order=request.form,
                status_options=STATUS_OPTIONS,
                mode="create",
            )

        db = get_db()
        try:
            db.execute(
                """
                INSERT INTO service_orders (reference, company, description, status, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    reference.strip(),
                    company.strip(),
                    description.strip(),
                    status,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            db.commit()
            flash("Orden creada correctamente.", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("La referencia ya existe. Debe ser única.", "error")

    return render_template(
        "form.html", order=None, status_options=STATUS_OPTIONS, mode="create"
    )


@app.route("/orders/<int:order_id>/edit", methods=["GET", "POST"])
def edit_order(order_id):
    db = get_db()
    order = db.execute(
        "SELECT * FROM service_orders WHERE id = ?", (order_id,)
    ).fetchone()

    if order is None:
        flash("Orden no encontrada.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        reference = request.form.get("reference", "")
        company = request.form.get("company", "")
        description = request.form.get("description", "")
        status = request.form.get("status", "Pendiente")

        errors = validate_form(reference, company, description, status)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "form.html",
                order=request.form,
                status_options=STATUS_OPTIONS,
                mode="edit",
                order_id=order_id,
            )

        try:
            db.execute(
                """
                UPDATE service_orders
                SET reference = ?, company = ?, description = ?, status = ?
                WHERE id = ?
                """,
                (reference.strip(), company.strip(), description.strip(), status, order_id),
            )
            db.commit()
            flash("Orden actualizada correctamente.", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("La referencia ya existe. Debe ser única.", "error")

    return render_template(
        "form.html",
        order=order,
        status_options=STATUS_OPTIONS,
        mode="edit",
        order_id=order_id,
    )


@app.post("/orders/<int:order_id>/delete")
def delete_order(order_id):
    db = get_db()
    db.execute("DELETE FROM service_orders WHERE id = ?", (order_id,))
    db.commit()
    flash("Orden eliminada correctamente.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
else:
    init_db()
