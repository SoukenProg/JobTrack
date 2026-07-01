from datetime import datetime
from sqlalchemy import select

from models import Companies, Applications, db


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d")

def register_commands(app):
    @app.cli.command("seed")
    def seed():
        mock_companies = [
            {
                "company_name": "株式会社テックソリューション",
                "industry": "IT・ソフトウェア",
                "website": "https://example.com",
                "location": "東京都渋谷区",
                "memo": "自社開発系。PythonやWebアプリ開発に強みがある想定。",
            },
            {
                "company_name": "株式会社デジタルワークス",
                "industry": "DX支援・業務改善",
                "website": "https://example.com",
                "location": "東京都新宿区",
                "memo": "中小企業向けに業務効率化ツールを提供している想定。",
            },
            {
                "company_name": "日本クラウドシステム株式会社",
                "industry": "クラウド・インフラ",
                "website": "https://example.com",
                "location": "東京都品川区",
                "memo": "AWS、Azure、Google Cloudなどの導入支援を行う想定。",
            },
            {
                "company_name": "株式会社ビジネスサポートラボ",
                "industry": "社内SE・情報システム",
                "website": "https://example.com",
                "location": "神奈川県横浜市",
                "memo": "社内システム運用やヘルプデスク業務を行う想定。",
            },
            {
                "company_name": "フューチャーリンク株式会社",
                "industry": "Webサービス",
                "website": "https://example.com",
                "location": "東京都港区",
                "memo": "Webサービスの企画・開発・運用を行う企業想定。",
            },
        ]

        created_count = 0
        skipped_count = 0

        for data in mock_companies:
            exists = db.session.execute(
                select(Companies).where(
                    Companies.company_name == data["company_name"]
                )
            ).scalar_one_or_none()

            if exists:
                skipped_count += 1
                continue

            company = Companies(**data)
            db.session.add(company)
            created_count += 1

        db.session.commit()

        print(
            f"companies のモックデータを追加しました。"
            f"追加: {created_count}件 / スキップ: {skipped_count}件"
        )

    @app.cli.command("clear-seed")
    def clear_seed():
        seed_company_names = [
            "株式会社テックソリューション",
            "株式会社デジタルワークス",
            "日本クラウドシステム株式会社",
            "株式会社ビジネスサポートラボ",
            "フューチャーリンク株式会社",
        ]

        deleted_count = 0

        for company_name in seed_company_names:
            company = db.session.execute(
                select(Companies).where(Companies.company_name == company_name)
            ).scalar_one_or_none()

            if company is None:
                continue

            db.session.delete(company)
            deleted_count += 1

        db.session.commit()

        print(f"モック企業データを削除しました。削除: {deleted_count}件")

    @app.cli.command("seed-applications")
    def seed_applications():
        mock_applications = [
            {
                "company_name": "株式会社テックソリューション",
                "job_title": "Pythonエンジニア",
                "application_route": "求人サイト",
                "status": "書類選考中",
                "application_date": "2026-06-10",
                "deadline": "2026-06-25",
                "salary": "月給25万円〜",
                "work_style": "ハイブリッド",
                "memo": "FlaskやPython経験をアピールしやすい求人。",
            },
            {
                "company_name": "株式会社デジタルワークス",
                "job_title": "DXサポート職",
                "application_route": "ハローワーク",
                "status": "一次面接",
                "application_date": "2026-06-12",
                "deadline": "2026-06-28",
                "salary": "月給23万円〜",
                "work_style": "出社",
                "memo": "業務改善・Google Workspace Studioの経験と相性が良い。",
            },
            {
                "company_name": "日本クラウドシステム株式会社",
                "job_title": "クラウド運用エンジニア",
                "application_route": "エージェント",
                "status": "応募済み",
                "application_date": "2026-06-15",
                "deadline": "2026-06-30",
                "salary": "月給26万円〜",
                "work_style": "リモート",
                "memo": "インフラ・クラウド系の経験を積める想定。",
            },
            {
                "company_name": "株式会社ビジネスサポートラボ",
                "job_title": "社内SE",
                "application_route": "企業HP",
                "status": "未応募",
                "application_date": None,
                "deadline": "2026-07-05",
                "salary": "月給24万円〜",
                "work_style": "出社",
                "memo": "社内業務改善やヘルプデスク寄りの求人。",
            },
            {
                "company_name": "フューチャーリンク株式会社",
                "job_title": "Webアプリケーションエンジニア",
                "application_route": "求人サイト",
                "status": "内定",
                "application_date": "2026-06-01",
                "deadline": None,
                "salary": "月給28万円〜",
                "work_style": "ハイブリッド",
                "memo": "ポートフォリオの説明と相性が良い想定。",
            },
        ]

        created_count = 0
        skipped_count = 0
        missing_company_count = 0

        for data in mock_applications:
            company = db.session.execute(
                select(Companies).where(
                    Companies.company_name == data["company_name"]
                )
            ).scalar_one_or_none()

            if company is None:
                missing_company_count += 1
                continue

            exists = db.session.execute(
                select(Applications).where(
                    Applications.company_id == company.id,
                    Applications.job_title == data["job_title"],
                )
            ).scalar_one_or_none()

            if exists:
                skipped_count += 1
                continue

            application = Applications(
                company_id=company.id,
                job_title=data["job_title"],
                application_route=data["application_route"],
                status=data["status"],
                application_date=parse_date(data["application_date"]) if data["application_date"] else None,
                deadline=parse_date(data["deadline"]) if data["deadline"] else None,
                salary=data["salary"],
                work_style=data["work_style"],
                memo=data["memo"],
            )

            db.session.add(application)
            created_count += 1

        db.session.commit()

        print(
            f"応募情報のモックデータを追加しました。"
            f"追加: {created_count}件 / "
            f"スキップ: {skipped_count}件 / "
            f"企業なし: {missing_company_count}件"
        )

    @app.cli.command("clear-seed-applications")
    def clear_seed_applications():
        seed_job_titles = [
            "Pythonエンジニア",
            "DXサポート職",
            "クラウド運用エンジニア",
            "社内SE",
            "Webアプリケーションエンジニア",
        ]

        deleted_count = 0

        for job_title in seed_job_titles:
            applications = db.session.execute(
                select(Applications).where(Applications.job_title == job_title)
            ).scalars().all()

            for application in applications:
                db.session.delete(application)
                deleted_count += 1

        db.session.commit()

        print(f"応募情報のモックデータを削除しました。削除: {deleted_count}件")