from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import select

from models import Applications, Companies, db


bp = Blueprint("companies", __name__, url_prefix="/companies")


@bp.route("/")
def index():
    companies = db.session.execute(
        select(Companies).order_by(Companies.created_at.desc())
    ).scalars().all()

    return render_template("companies/index.html", companies=companies)


@bp.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        company = Companies(
            company_name=request.form["company_name"].strip(),
            industry=request.form["industry"].strip(),
            website=request.form.get("website", "").strip(),
            location=request.form.get("location", "").strip(),
            memo=request.form.get("memo", "").strip(),
        )

        db.session.add(company)
        db.session.commit()

        return redirect(url_for("companies.index"))

    return render_template("companies/new.html")

@bp.route("/<int:company_id>")
def detail(company_id):
    company = db.get_or_404(Companies, company_id)
    return render_template("companies/detail.html")

@bp.route("/<int:company_id>/edit", methods=["GET", "POST"])
def edit(company_id):
    company = db.get_or_404(Companies, company_id)

    if request.method == "POST":
        company.company_name = request.form["company_name"].strip()
        company.industry = request.form["industry"].strip()
        company.website = request.form["website"].strip()
        company.location = request.form["location"].strip()
        company.memo = request.form["memo"].strip()

        db.session.add(company)
        db.session.commit()
        return redirect(url_for("companies.detail", company_id=company_id))
    return render_template("companies/edit.html", company=company)

@bp.route("/<int:company_id>/delete", methods=["POST"])
def delete(company_id):
    company = db.get_or_404(Companies, company_id)
    db.session.delete(company)
    db.session.commit()
    return redirect(url_for("companies.index"))