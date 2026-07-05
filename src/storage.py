from src.models import UserModel, PullRequestModel

# user_id -> UserModel
users_db: dict[str, UserModel] = {}

# Названия существующих команд
teams_db: set[str] = set()

# pull_request_id -> PullRequestModel
prs_db: dict[str, PullRequestModel] = {}