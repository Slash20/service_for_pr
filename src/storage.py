from src.models import UserModel, PullRequestModel

users_db: dict[str, UserModel] = {}

teams_db: set[str] = set()

prs_db: dict[str, PullRequestModel] = {}