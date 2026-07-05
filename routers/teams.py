from fastapi import APIRouter, HTTPException, status

from src.models import (
    Team,
    TeamMember,
    TeamResponse,
    UserModel,
)
from src.storage import teams_db, users_db

router = APIRouter(tags=["Teams"])


@router.post(
    "/team/add",
    status_code=status.HTTP_201_CREATED,
    response_model=TeamResponse
)
def add_team(team: Team):
    if team.team_name in teams_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "TEAM_EXISTS",
                    "message": "team_name already exists"
                }
            }
        )

    teams_db.add(team.team_name)

    for member in team.members:
        users_db[member.user_id] = UserModel(
            user_id=member.user_id,
            username=member.username,
            team_name=team.team_name,
            is_active=member.is_active
        )

    members = [
        TeamMember(
            user_id=user.user_id,
            username=user.username,
            is_active=user.is_active
        )
        for user in users_db.values()
        if user.team_name == team.team_name
    ]

    return TeamResponse(
        team=Team(
            team_name=team.team_name,
            members=members
        )
    )


@router.get(
    "/team/get",
    response_model=Team
)
def get_team(team_name: str):
    if team_name not in teams_db:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": "team not found"
                }
            }
        )

    members = [
        TeamMember(
            user_id=user.user_id,
            username=user.username,
            is_active=user.is_active
        )
        for user in users_db.values()
        if user.team_name == team_name
    ]

    return Team(
        team_name=team_name,
        members=members
    )