from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import select

from constants import BADGE_COLOR
from models import Applications, Companies, db


from constants import APPLICATION_STATUSES, WORK_STYLES, APPLICATION_ROUTES, BADGE_COLOR

bp = Blueprint("applications", __name__)


def parse_date(value):
    if not value:
        return None

    return datetime.strptime(value, "%Y-%m-%d")


# 日付を与えて見た目を変える関数
def calc_deadline(deadline):
    if not deadline:
        return {"color": "secondary", "comment": "未設定"}

    today = datetime.now().date()
    three_days_later = today + timedelta(days=3)
    if deadline.date() < today:
        return {"color": "danger", "comment": "期限切れ"}
    elif deadline.date() == today:
        return {"color": "danger", "comment": "本日まで"}
    elif deadline.date() <= three_days_later:
        return {"color": "warning", "comment": ""}
    else:
        return {"color": "body", "comment": ""}


@bp.route("/applications")
def index():
    applications = (
        db.session.execute(
            select(Applications).order_by(Applications.deadline.asc().nulls_last())
        )
        .scalars()
        .all()
    )

    return render_template(
        "applications/index.html", applications=applications, bg_color=BADGE_COLOR,calc_deadline=calc_deadline
    )


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


@bp.route("/applications/<int:application_id>")
def detail(application_id):
    application = db.get_or_404(Applications, application_id)

    return render_template(
        "applications/detail.html", application=application, bg_color=BADGE_COLOR
    )


@bp.route("/applications/<int:application_id>/edit", methods=["GET", "POST"])
def edit(application_id):
    application = db.get_or_404(Applications, application_id)

    if request.method == "POST":
        application.job_title = request.form["job_title"].strip()
        application.application_route = request.form.get(
            "application_route", ""
        ).strip()
        application.status = request.form["status"].strip()
        application.application_date = parse_date(request.form.get("application_date"))
        application.deadline = parse_date(request.form.get("deadline"))
        application.salary = request.form.get("salary", "").strip()
        application.work_style = request.form.get("work_style", "").strip()
        application.memo = request.form.get("memo", "").strip()

        db.session.commit()

        return redirect(url_for("applications.detail", application_id=application.id))

    return render_template(
        "applications/edit.html",
        application=application,
        application_statuses=APPLICATION_STATUSES,
        work_styles=WORK_STYLES,
        application_routes=APPLICATION_ROUTES,
    )


@bp.route("/applications/<int:application_id>/delete", methods=["POST"])
def delete(application_id):
    application = db.get_or_404(Applications, application_id)
    company_id = application.company_id

    db.session.delete(application)
    db.session.commit()

    return redirect(url_for("companies.detail", company_id=company_id))
