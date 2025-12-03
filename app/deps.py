
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import get_db
from .models import ADPUser, ADPRole, ADPUserRole
from .auth_utils import decode_access_token
from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> TokenData:
    try:
        token_data = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = db.query(ADPUser).filter(ADPUser.user_id == token_data.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # roles already embedded in token, but we could re-fetch if needed
    return token_data


def require_role(required_role: str):
    def checker(current: TokenData = Depends(get_current_user)):
        if required_role not in current.roles:
            raise HTTPException(
                status_code=403,
                detail=f"Requires role {required_role}",
            )
        return current
    return checker
