from typing import Optional

from pydantic import BaseModel, validator


class modelData(BaseModel):
    Age: Optional[int] = None
    SibSp: Optional[int] = None
    Parch: Optional[int] = None
    Sex: Optional[str] = None
    Embarked: Optional[str] = None
    Pclass: Optional[int] = None

    @validator("Embarked")
    def validate_embarked(cls, value):
        if value not in ["C", "Q", "S"]:
            raise ValueError("must be C, Q or S")
        return value

    @validator("Pclass")
    def validate_class(cls, value):
        if value not in [1, 2, 3]:
            raise ValueError("must be 1, 2 or 3")
        return value

    @validator("Sex")
    def validate_sex(cls, value):
        if value not in ["male", "female"]:
            raise ValueError("must be male or female")
        return value
