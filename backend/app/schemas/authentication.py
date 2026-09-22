from pydantic import BaseModel


class RegisterRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    role: str
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str