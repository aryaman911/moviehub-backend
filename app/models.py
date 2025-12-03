
from sqlalchemy import (
    Column, Integer, BigInteger, String, Date, Numeric,
    ForeignKey, Text
)
from sqlalchemy.orm import relationship
from .database import Base


class ADPUser(Base):
    __tablename__ = "adp_user"

    user_id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)

    roles = relationship("ADPUserRole", back_populates="user")


class ADPRole(Base):
    __tablename__ = "adp_role"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)

    users = relationship("ADPUserRole", back_populates="role")


class ADPUserRole(Base):
    __tablename__ = "adp_user_role"

    user_id = Column(BigInteger, ForeignKey("adp_user.user_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("adp_role.role_id"), primary_key=True)

    user = relationship("ADPUser", back_populates="roles")
    role = relationship("ADPRole", back_populates="users")


class ADPSeries(Base):
    __tablename__ = "adp_series"

    series_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(160), nullable=False)
    num_episodes = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    adp_language_language_code = Column(String(8), nullable=False)
    origin_country = Column(String(80), nullable=False)

    feedback = relationship("ADPFeedback", back_populates="series")


class ADPFeedback(Base):
    __tablename__ = "adp_feedback"

    adp_account_account_id = Column(BigInteger, primary_key=True)
    adp_series_series_id = Column(BigInteger, primary_key=True)

    feedback_text = Column(String(2000))
    rating = Column(Integer, nullable=False)
    feedback_date = Column(Date, nullable=False)

    series = relationship("ADPSeries", back_populates="feedback")


class ADPContract(Base):
    __tablename__ = "adp_contract"

    contract_id = Column(BigInteger, primary_key=True, index=True)
    contract_start_date = Column(Date, nullable=False)
    contract_end_date = Column(Date, nullable=False)
    per_episode_charge = Column(Numeric(10, 2), nullable=False)
    status = Column(String(12), nullable=False)
    adp_series_series_id = Column(BigInteger, ForeignKey("adp_series.series_id"), nullable=False)
    adp_production_house_house_id = Column(BigInteger, nullable=False)
