from pydantic import BaseModel, EmailStr
from pydantic.fields import Field
from typing import Optional, List
from uuid import uuid4

class ComplexAlgo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="ID único do objeto")
    mensagem: str = Field(..., min_length=5, max_length=255, description="Mensagem de conteúdo textual")
    prioridade: Optional[int] = Field(None, ge=1, le=5, description="Nível de prioridade, de 1 a 5")
    email: EmailStr = Field(..., description="Endereço de email válido associado ao objeto")
    tags: List[str] = Field(default_factory=list, description="Lista de tags associadas ao objeto")
