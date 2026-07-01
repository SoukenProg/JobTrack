from datetime import datetime

from sqlalchemy import func, select
from flask import Blueprint, render_template
from constants import APPLICATION_STATUSES
from models import Companies, Applications, Interviews, db

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def index():
    applications = db.session.execute(
        select(Applications)
        .join(Companies)
        .order_by(Applications.created_at.desc())
        .limit(10)
    ).scalars().all()
    active_status = APPLICATION_STATUSES[1:6]
    # データ
    stats = {
        "companies": db.session.scalar(select(func.count()).select_from(Companies)),
        "active": db.session.scalar(
            select(func.count()).select_from(Applications).where(Applications.status.in_(active_status))),
        "interview": db.session.scalar(
            select(func.count()).select_from(Interviews).where(Interviews.interview_date >= datetime.now())),
        "success": db.session.scalar(
            select(func.count()).select_from(Applications).where(Applications.status == "内定")),
    }

    return render_template("dashboard.html", stats=stats,applications=applications)
