from fastapi import APIRouter

from src.models import (
    SetUserActiveRequest,
    UserResponse,
    UserReviewsResponse,
    PullRequestShort,
)
from src.storage import prs_db
from src.utils import get_user_or_404

router = APIRouter(tags=["Users"])


@router.post(
    "/users/setIsActive",
    response_model=UserResponse
)
async def set_user_active(body: SetUserActiveRequest):
    user = get_user_or_404(body.user_id)

    user.is_active = body.is_active

    return UserResponse(user=user)


@router.get(
    "/users/getReview",
    response_model=UserReviewsResponse
)
async def get_user_reviews(user_id: str):
    get_user_or_404(user_id)

    pull_requests = [
        PullRequestShort(
            pull_request_id=pr.pull_request_id,
            pull_request_name=pr.pull_request_name,
            author_id=pr.author_id,
            status=pr.status,
        )
        for pr in prs_db.values()
        if user_id in pr.assigned_reviewers
    ]

    return UserReviewsResponse(
        user_id=user_id,
        pull_requests=pull_requests,
    )