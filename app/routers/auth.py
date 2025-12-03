from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ADPUser, ADPRole, ADPUserRole
from app.auth_utils import hash_password, verify_password, create_access_token
from app.schemas import UserCreate, UserOut, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(ADPUser).filter(ADPUser.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Basic user_id assignment: you already have seed users, so we take max+1
    max_id = db.query(ADPUser.user_id).order_by(ADPUser.user_id.desc()).first()
    new_id = (max_id[0] + 1) if max_id and max_id[0] else 1

    user = ADPUser(
        user_id=new_id,
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.flush()

    # Default role = CUSTOMER (assumes a row in adp_role with role_name='CUSTOMER')
    customer_role = db.query(ADPRole).filter(ADPRole.role_name == "CUSTOMER").first()
    roles = []
    if customer_role:
        db.add(ADPUserRole(user_id=user.user_id, role_id=customer_role.role_id))
        roles.append(customer_role.role_name)

    db.commit()
    return UserOut(
        user_id=user.user_id,
        email=user.email,
        full_name=user.full_name,
        roles=roles,
    )


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(ADPUser).filter(ADPUser.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    roles = (
        db.query(ADPRole.role_name)
        .join(ADPUserRole, ADPUserRole.role_id == ADPRole.role_id)
        .filter(ADPUserRole.user_id == user.user_id)
        .all()
    )
    role_names = [r[0] for r in roles]

    token = create_access_token(user.user_id, user.email, role_names)
    return Token(access_token=token)
