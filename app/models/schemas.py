from pydantic import BaseModel, Field


class InputModel(BaseModel):
    """Модель входных данных для PassThroughRunnable"""

    input: str = Field(..., description="Входной текст для обработки")
