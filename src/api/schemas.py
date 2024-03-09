from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class TransactionType(str, Enum):
    credito = "c"
    debito = "d"

class TransactionBase(BaseModel):
    valor: int
    tipo: TransactionType
    descricao: str = Field(max_length=10, min_length=1)

class TransactionCreate(TransactionBase):
    id: int
    cliente_id: int
    realizada_em: str

class Transaction(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    realizada_em: datetime

class AccountDetails(BaseModel):
    limite: int
    saldo: int

class ClientDetails(BaseModel):
    limite: int
    saldo: int

class ClientCreate(ClientDetails):
    id: int

class Client(ClientDetails):
    model_config = ConfigDict(from_attributes=True)
