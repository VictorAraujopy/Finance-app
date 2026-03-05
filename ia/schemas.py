from pydantic import BaseModel

#define o que a IA vai devolver
class InsightResponse(BaseModel):
    resumo: str
    alertas: list[str]
    sugestoes: list[str]
    investimento: dict