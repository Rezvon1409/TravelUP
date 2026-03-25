from pydantic import BaseModel

class RegisterSchema(BaseModel):
    username : str
    password : str

class LoginSchema(BaseModel):
    username : str
    passwrod : str

class TokenSchema(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str = 'bearer'

class RefreshSchema(BaseModel):
    refresh_token : str