from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str | None = None


class UserLogin(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=4, max_length=12)
    new_password: str = Field(min_length=6, max_length=128)


class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=4, max_length=12)


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    name: str | None
    email_verified: bool
    phone: str | None = None
    pending_email: str | None = None

    model_config = {"from_attributes": True}


class UserRegisterOut(UserOut):
    """Same as signup response, plus optional code when EXPOSE_VERIFICATION_CODES is enabled."""

    verification_code: str | None = None


class VerifyEmailResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class AccountUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=32)
    current_password: str | None = None
    new_password: str | None = Field(None, min_length=6)


class ProfileUpdate(BaseModel):
    age: int | None = Field(None, ge=1, le=120)
    sex: str | None = Field(None, max_length=32)
    height_cm: float | None = Field(None, ge=50, le=250)
    weight_kg: float | None = Field(None, ge=10, le=400)
    profile_image_base64: str | None = None


class ProfileOut(BaseModel):
    age: int | None
    sex: str | None
    height_cm: float | None
    weight_kg: float | None
    profile_image_base64: str | None

    model_config = {"from_attributes": True}


class PlanUpdate(BaseModel):
    category: str | None = Field(None, min_length=2, max_length=64)
    duration_weeks: int | None = Field(None, ge=4, le=12)
    before_photo_base64: str | None = None
    after_photo_base64: str | None = None
    onboarding_completed: bool | None = None


class PlanOut(BaseModel):
    category: str | None
    duration_weeks: int | None
    before_photo_base64: str | None
    after_photo_base64: str | None
    onboarding_completed: bool

    model_config = {"from_attributes": True}


class MeOut(BaseModel):
    user: UserOut
    profile: ProfileOut | None
    plan: PlanOut | None


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    messages: list[ChatMessage] = Field(default_factory=list)
    message: str | None = None
    image_base64: str | None = Field(default=None, alias="imageBase64")
    assistant_tone: str | None = None
    prefer_short_reply: bool | None = None
    cross_chat_summary: str | None = Field(default=None, alias="crossChatSummary")


class ChatResponse(BaseModel):
    reply: str


class WorkoutCreate(BaseModel):
    exercise_label: str = Field(min_length=1, max_length=128)
    reps: int = Field(ge=0)
    duration_sec: int | None = Field(None, ge=0)
    source: Literal["auto_classify", "manual_exercise"]
    weight_kg: float | None = Field(None, ge=0, le=600)
    equipment: Literal["bar", "dumbbell", "bodyweight", "other"] | None = None
    sets: int | None = Field(None, ge=1, le=50)
    estimated_kcal: float | None = Field(None, ge=0)
    generate_ai_report: bool = False
    language_code: str = Field(default="en", alias="languageCode")


class WorkoutOut(BaseModel):
    id: int
    exercise_label: str
    reps: int
    duration_sec: int | None
    source: str
    created_at: str
    weight_kg: float | None = None
    equipment: str | None = None
    sets: int | None = None
    estimated_kcal: float | None = None
    session_report: str | None = None

    model_config = {"from_attributes": True}
