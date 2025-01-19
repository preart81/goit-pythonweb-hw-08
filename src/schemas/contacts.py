from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ContactBase(BaseModel):
    """
    ContactBase schema for contact information.
    Attributes:
        first_name (str): The first name of the contact. Must be between 2 and 50 characters.
        last_name (str): The last name of the contact. Must be between 2 and 50 characters.
        email (EmailStr): The email address of the contact.
        phone_number (str): The phone number of the contact. Must be between 6 and 20 characters.
        birthday (date): The birthday of the contact. Cannot be a future date.
        additional_data (Optional[str]): Additional information about the contact. Maximum length is 150 characters.
    Methods:
        validate_birthday(cls, v): Validates that the birthday is not in the future.
    """

    first_name: str = Field(max_length=50, min_length=2)
    last_name: str = Field(max_length=50, min_length=2)
    email: EmailStr
    phone_number: str = Field(max_length=20, min_length=6)
    birthday: date
    additional_data: Optional[str] = Field(max_length=150)

    @field_validator("birthday")
    def validate_birthday(self, v):
        """
        Validates that the provided birthday is not in the future.

        Args:
            v (date): The birthday to validate.

        Raises:
            ValueError: If the birthday is in the future.

        Returns:
            date: The validated birthday.
        """
        if v > date.today():
            raise ValueError("Birthday cannot be in the future")
        return v


class ContactResponse(ContactBase):
    """
    ContactResponse is a data model that extends ContactBase and includes additional fields for
    id, created_at, and updated_at.
    Attributes:
        id (int): The unique identifier for the contact.
        created_at (datetime | None): The timestamp when the contact was created. Can be None.
        updated_at (Optional[datetime] | None): The timestamp when the contact was last updated. Can be None.
    Config:
        model_config (ConfigDict): Configuration dictionary with attributes settings.
    """

    id: int
    created_at: datetime | None
    updated_at: Optional[datetime] | None

    model_config = ConfigDict(from_attributes=True)


class ContactBirthdayRequest(BaseModel):
    """
    ContactBirthdayRequest is a Pydantic model that represents a request for contact birthdays.

    Attributes:
        days (int): The number of days within which to search for birthdays.
                    Must be between 0 and 366 inclusive.
    """

    days: int = Field(ge=0, le=366)
