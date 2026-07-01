import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import select

from models import Applications, Companies, db
from routes.dashboard import bp

from constants import APPLICATION_STATUSES, WORK_STYLES, APPLICATION_ROUTES

bp = Blueprint('applications', __name__)

def parse_date(value):
    if not value:
        return None

    return datetime.strptime(value, "%Y-%m-%d")
@bp.route("/applications")
def index():
    return render_template("applications/index.html")

@bp.route("/companies/<int:company_id>/applications/new", methods=["GET", "POST"])
def new(company_id):
    company = db.get_or_404(Companies, company_id)
    if request.method == "POST":
        application = Applications(
            company_id=company.id,
            job_title=request.form["job_title"].strip(),
            application_route=request.form.get("application_route", "").strip(),
            status=request.form["status"].strip(),
            application_date=parse_date(request.form.get("application_date")),
            deadline=parse_date(request.form.get("deadline")),
            salary=request.form.get("salary", "").strip(),
            work_style=request.form.get("work_style", "").strip(),
            memo=request.form.get("memo", "").strip(),
        )

        db.session.add(application)
        db.session.commit()

        return redirect(url_for("companies.detail", company_id=company.id))

    return render_template(
        "applications/new.html",
        company=company,
        application_statuses=APPLICATION_STATUSES,
        work_styles=WORK_STYLES,
        application_routes=APPLICATION_ROUTES,
    )