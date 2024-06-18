from bot import ADMINS, OWNER_ID


def authorize_admin(user_id: int) -> bool:
    return user_id in ADMINS or user_id == OWNER_ID
