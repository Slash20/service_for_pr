from datetime import datetime, timezone

from fastapi import HTTPException

from src.models import UserModel, PullRequestModel
from src.storage import users_db, prs_db


def now_iso() -> str:
    """Текущее время в формате ISO-8601."""
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def get_user_or_404(user_id: str) -> UserModel:
    """Получить пользователя или вернуть 404."""
    user = users_db.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": "user not found"
                }
            }
        )
    return user


def get_pr_or_404(pr_id: str) -> PullRequestModel:
    """Получить Pull Request или вернуть 404."""
    pr = prs_db.get(pr_id)
    if pr is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": "PR not found"
                }
            }
        )
    return pr