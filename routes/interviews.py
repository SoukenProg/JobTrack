from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for

from models import Applications, Interviews, db


from constants import INTERVIEW_TYPES, INTERVIEW_ROUNDS

bp = Blueprint("interviews", __name__)


def parse_datetime(value):
    if not value:
        return None

    return datetime.strptime(value, "%Y-%m-%dT%H:%M")


@bp.route(
    "/applications/<int:application_id>/interviews/new",
    methods=["GET", "POST"],
)
def new(application_id):
    application = db.get_or_404(Applications, application_id)
    if request.method == "POST":
        interview = Interviews(
            application_id=application.id,
            interview_date=parse_datetime(request.form.get("interview_date")),
            interview_type=request.form["interview_type"].strip(),
            interview_round=request.form["interview_round"].strip(),
            interviewer=request.form.get("interviewer").strip(),
            location=request.form.get("location").strip(),
            prepare_memo=request.form.get("prepare_memo", "").strip(),
            result_memo=request.form.get("result_memo", "").strip(),
        )
        db.session.add(interview)
        db.session.commit()
        return redirect(
            url_for(
                "applications.detail",
                application_id=application.id,
            )
        )

    return render_template(
        "interviews/new.html",
        application=application,
        interview_types=INTERVIEW_TYPES,
        interview_rounds=INTERVIEW_ROUNDS,
    )


@bp.route("/interviews/<int:interview_id>")
def detail(interview_id):
    interview = db.get_or_404(Interviews, interview_id)

    return render_template("interviews/detail.html", interview=interview)


@bp.route("/interviews/<int:interview_id>/edit", methods=["GET", "POST"])
def edit(interview_id):
    interview = db.get_or_404(Interviews, interview_id)

    if request.method == "POST":

        interview.interview_date = parse_datetime(request.form.get("interview_date"))
        interview.interview_type = request.form["interview_type"].strip()
        interview.interview_round = request.form["interview_round"].strip()
        interview.interviewer = request.form.get("interviewer").strip()
        interview.location = request.form.get("location").strip()
        interview.prepare_memo = request.form.get("prepare_memo", "").strip()
        interview.result_memo = request.form.get("result_memo", "").strip()

        db.session.commit()

        return redirect(url_for("interviews.detail", interview_id=interview_id))
    return render_template(
        "interviews/edit.html",
        interview=interview,
        interview_types=INTERVIEW_TYPES,
        interview_rounds=INTERVIEW_ROUNDS,
    )


@bp.route("/interviews/<int:interview_id>/delete", methods=["POST"])
def delete(interview_id):
    interview = db.get_or_404(Interviews, interview_id)
    application_id = interview.application_id

    db.session.delete(interview)
    db.session.commit()

    return redirect(url_for("applications.detail", application_id=application_id))
