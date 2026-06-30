from flask import Blueprint, render_template

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def index():
    #モックデータ
    stats = {
        "companies": 0,
        "active": 0,
        "interview": 0,
        "success": 0,
    }

    return render_template("dashboard.html", stats=stats)