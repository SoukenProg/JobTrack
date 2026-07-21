INTERVIEW_STAGE_NAMES = [
    "一次面接",
    "二次面接",
    "最終面接",
]

APPLICATION_STATUSES = [
    "未応募",
    "応募済み",
    "書類選考中",
    *INTERVIEW_STAGE_NAMES,
    "内定",
    "辞退",
    "不採用",
]

INTERVIEW_ROUNDS = [
    "カジュアル面談",
    *INTERVIEW_STAGE_NAMES,
    "その他",
]

WORK_STYLES = [
    "出社",
    "リモート",
    "ハイブリッド",
    "未定",
]

APPLICATION_ROUTES = [
    "求人サイト",
    "ハローワーク",
    "企業HP",
    "紹介",
    "エージェント",
    "その他",
]

INTERVIEW_TYPES = [
    "対面",
    "オンライン",
    "その他",
]
