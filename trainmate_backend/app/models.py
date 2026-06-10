from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    pending_email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    verification_code_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    verification_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verification_last_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    password_reset_code_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    password_reset_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    password_reset_last_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    profile: Mapped["UserProfile | None"] = relationship(
        "UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    plan: Mapped["UserPlan | None"] = relationship(
        "UserPlan", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    workouts: Mapped[list["WorkoutSession"]] = relationship(
        "WorkoutSession", back_populates="user", cascade="all, delete-orphan"
    )


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sex: Mapped[str | None] = mapped_column(String(32), nullable=True)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    profile_image_base64: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="profile")


class UserPlan(Base):
    __tablename__ = "user_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    duration_weeks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    before_photo_base64: Mapped[str | None] = mapped_column(Text, nullable=True)
    after_photo_base64: Mapped[str | None] = mapped_column(Text, nullable=True)
    onboarding_completed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["User"] = relationship("User", back_populates="plan")


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    exercise_label: Mapped[str] = mapped_column(String(128), nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False)

    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    equipment: Mapped[str | None] = mapped_column(String(32), nullable=True)
    sets: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estimated_kcal: Mapped[float | None] = mapped_column(Float, nullable=True)
    session_report: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="workouts")
