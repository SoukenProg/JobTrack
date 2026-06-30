from sqlalchemy import select

from models import Companies, db


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