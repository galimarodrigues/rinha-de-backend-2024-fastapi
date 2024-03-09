from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class Cliente(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    limite = Column(Integer)
    saldo = Column(Integer)
    transacoes = relationship("Transacao", back_populates="cliente")

class Transacao(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    valor = Column(Integer)
    tipo = Column(String)
    descricao = Column(String)
    realizada_em = Column(DateTime, default=datetime.now())
    cliente_id = Column(Integer, ForeignKey("clients.id"))
    cliente = relationship("Cliente", back_populates="transacoes")