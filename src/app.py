import time
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from src import schemas
from src.models import Transacao, Cliente
from src.database import SessionLocal

app = FastAPI()

async def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@app.post("/clientes/{cliente_id}/transacoes", response_model=schemas.AccountDetails)
async def post_transacao(cliente_id: int,
                         transaction: schemas.TransactionBase, 
                         db_session: Session = Depends(get_db_session)):
    client = db_session.get(Cliente, cliente_id)

    if not client:
        raise HTTPException(status_code=404, detail="Cliente not found")

    if transaction.tipo == schemas.TransactionType.debito:
        if client.saldo - transaction.valor < -client.limite:
            raise HTTPException(status_code=422, detail="Transação de débito excede o limite disponível")
        client.saldo -= transaction.valor

    elif transaction.tipo == schemas.TransactionType.credito:
        client.saldo += transaction.valor

    new_transaction = Transacao(
        valor=transaction.valor,
        tipo=transaction.tipo,
        descricao=transaction.descricao,
        cliente_id=cliente_id
    )
    db_session.add(new_transaction)
    db_session.commit()

    return {
        "limite": client.limite,
        "saldo": client.saldo,
    }


@app.get("/clientes/{id}/extrato")
async def get_extrato(id: int, 
                      db_session: Session = Depends(get_db_session)):
    client = db_session.get(Cliente, id)
    
    if not client:
        raise HTTPException(status_code=404, detail="Cliente not found")
    
    transactions = db_session.execute(
        select(Transacao)
        .where(Transacao.cliente_id == id)
        .order_by(Transacao.id.desc()).limit(10)
    )

    return {
        "saldo": {
            "total": client.saldo,
            "data_extrato": time.strftime("%Y/%m/%dT%H:%M:%S", time.gmtime()),
            "limite": client.limite
        },
        "ultimas_transacoes":[
                schemas.Transaction.model_validate(t) for t in transactions.scalars()
            ]
    }