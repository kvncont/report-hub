"""This class represent the Report model"""

from pydantic import BaseModel, Field


class Report(BaseModel):
    """Class representing the Report model"""

    name: str
    template_url: str = Field(alias="templateUrl")
    data: dict = {}
