import random

from fastapi import APIRouter, HTTPException, status

from src.models import (
    CreatePRRequest,
    MergePRRequest,
    ReassignReviewerRequest,
    PullRequestResponse,
    ReassignResponse,
    PullRequestShort, PRStatus, PullRequestModel
)
from src.storage import prs_db, users_db
from src.utils import now_iso, get_pr_or_404, get_user_or_404

router = APIRouter(tags=["PullRequests"])


@router.post(
    "/pullRequest/create",
    status_code=status.HTTP_201_CREATED,
    response_model=PullRequestResponse,
)
async def create_pr(body: CreatePRRequest):
    if body.pull_request_id in prs_db:
        raise HTTPException(
            status_code=409,
            detail={
                "error": {
                    "code": "PR_EXISTS",
                    "message": "PR id already exists",
                }
            },
        )

    author = get_user_or_404(body.author_id)

    # кандидаты: активные, из той же команды, не автор
    candidates = [
        u
        for u in users_db.values()
        if u.team_name == author.team_name
        and u.is_active
        and u.user_id != body.author_id
    ]

    reviewers = random.sample(candidates, k=min(2, len(candidates)))

    pr = PullRequestModel(
        pull_request_id=body.pull_request_id,
        pull_request_name=body.pull_request_name,
        author_id=body.author_id,
        status=PRStatus.OPEN,
        assigned_reviewers=[u.user_id for u in reviewers],
        createdAt=now_iso(),
        mergedAt=None
    )

    prs_db[body.pull_request_id] = pr

    return PullRequestResponse(pr=pr)


@router.post(
    "/pullRequest/merge",
    response_model=PullRequestResponse,
)
async def merge_pr(body: MergePRRequest):
    pr = get_pr_or_404(body.pull_request_id)

    if pr.status == PRStatus.MERGED:
        return PullRequestResponse(pr=pr)

    pr.status = "MERGED"
    pr.mergedAt = now_iso()

    return PullRequestResponse(pr=pr)


@router.post(
    "/pullRequest/reassign",
    response_model=ReassignResponse,
)
async def reassign_reviewer(body: ReassignReviewerRequest):
    pr = get_pr_or_404(body.pull_request_id)

    if pr.status == "MERGED":
        raise HTTPException(
            status_code=409,
            detail={
                "error": {
                    "code": "PR_MERGED",
                    "message": "cannot reassign on merged PR",
                }
            },
        )

    if body.old_user_id not in pr.assigned_reviewers:
        raise HTTPException(
            status_code=409,
            detail={
                "error": {
                    "code": "NOT_ASSIGNED",
                    "message": "reviewer is not assigned to this PR",
                }
            },
        )

    old_user = get_user_or_404(body.old_user_id)

    candidates = [
        u
        for u in users_db.values()
        if u.team_name == old_user.team_name
        and u.is_active
        and u.user_id != pr.author_id
        and u.user_id not in pr.assigned_reviewers
    ]

    if not candidates:
        raise HTTPException(
            status_code=409,
            detail={
                "error": {
                    "code": "NO_CANDIDATE",
                    "message": "no active replacement candidate in team",
                }
            },
        )

    new_user = random.choice(candidates)

    # заменяем одного ревьювера
    pr.assigned_reviewers = [
        new_user.user_id if uid == body.old_user_id else uid
        for uid in pr.assigned_reviewers
    ]

    return ReassignResponse(
        pr=pr,
        replaced_by=new_user.user_id,
    )


def to_short(pr):
    return PullRequestShort(
        pull_request_id=pr.pull_request_id,
        pull_request_name=pr.pull_request_name,
        author_id=pr.author_id,
        status=pr.status,
    )