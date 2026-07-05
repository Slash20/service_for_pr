from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class PRStatus(str, Enum):
    OPEN = "OPEN"
    MERGED = "MERGED"


class TeamMember(BaseModel):
    user_id: str
    username: str
    is_active: bool


class Team(BaseModel):
    team_name: str
    members: List[TeamMember]


class UserModel(BaseModel):
    user_id: str
    username: str
    team_name: str
    is_active: bool


class PullRequestModel(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: PRStatus
    assigned_reviewers: List[str] = Field(default_factory=list)
    createdAt: Optional[str] = None
    mergedAt: Optional[str] = None


class PullRequestShort(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: PRStatus


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


class SetUserActiveRequest(BaseModel):
    user_id: str
    is_active: bool


class CreatePRRequest(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str


class MergePRRequest(BaseModel):
    pull_request_id: str


class ReassignReviewerRequest(BaseModel):
    pull_request_id: str
    old_user_id: str


class TeamResponse(BaseModel):
    team: Team


class UserResponse(BaseModel):
    user: UserModel


class PullRequestResponse(BaseModel):
    pr: PullRequestModel


class ReassignResponse(BaseModel):
    pr: PullRequestModel
    replaced_by: str


class UserReviewsResponse(BaseModel):
    user_id: str
    pull_requests: List[PullRequestShort]