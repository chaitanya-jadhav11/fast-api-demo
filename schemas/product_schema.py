from pydantic import BaseModel, validator, Field, field_validator


class ProductRequest(BaseModel):
    id : int
    name: str
    description: str = Field(min_length=3)
    price: float =Field(gt=0)
    quantity: int = Field(gt=0)

    # Custom validator
    @field_validator('name')
    @classmethod
    def no_spaces_in_username(cls, v: str) -> str:
        if ' ' in v:
            #raise ValueError('name cannot contain spaces')
            return {"message": "name cannot contain spaces'"}

        return v  # You must always return the validated value
