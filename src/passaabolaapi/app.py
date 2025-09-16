from fastapi import FastAPI, Depends, HTTPException
from .schemas.SchemaTime import SchemaTime, SchemaGetTime
from .schemas.SchemaJogadora import Schema_Jogadora
from .schemas.SchemaJogo import SchemaJogo
from .schemas.SchemaMessage import SchemaMessage
from .schemas.SchemaPostGol import SchemaPostGol
from .database.tables_database import get_session, JogoDB, TimeDB, JogadoraDB
from sqlalchemy import select

app = FastAPI()

# ===================================

@app.get('/pegar_time/', status_code=200, response_model=SchemaTime)
def pegarTimes(query_limit: int = 1, session=Depends(get_session)):
    time = session.scalars(select(TimeDB).limit(query_limit)).all()
    if not time:
        raise HTTPException(status_code=404, detail="Nenhum Time Cadastrado")
    return time

@app.get("/pegar_placar/{jogo_id}", response_model=SchemaJogo, status_code=200)
def pegar_placar(jogo_id: int, session=Depends(get_session)):
    jogo = session.scalar(select(JogoDB).where((JogoDB.id == jogo_id)))
    if not jogo:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return jogo

@app.get("/pegar_jogadoras/{jogadora_id}", response_model=Schema_Jogadora, status_code=200)
def pegar_jogadora(jogadora_id: int, query_limit: int = 1, session=Depends(get_session)):
    jogadora = session.scalar(select(JogadoraDB).where((jogadora_id == JogadoraDB.id)))
    if not jogadora:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return jogadora

# ^============= GET ============== ^

# v============= POST ============= v

@app.post('/cadastrar_times', status_code=201, response_model=SchemaMessage)
def cadastrarTime(time: SchemaGetTime, session=Depends(get_session)):
    existing = session.scalar(select(TimeDB).where(TimeDB.nome == time.nome.upper()))
    if existing:
        raise HTTPException(status_code=400, detail="Time já existe")

    db_time = TimeDB(nome=time.nome.upper())
    session.add(db_time)
    session.commit()
    session.refresh(db_time)
    return {'message': 'Team created!'}


@app.post(path="/cadastrar_jogadora", status_code=201, response_model=SchemaMessage)
def cadastrarJogadora(jogadora: Schema_Jogadora, session=Depends(get_session)):
    time = session.scalar(select(TimeDB).where(TimeDB.nome == jogadora.nome_time))
    if not time:
        raise HTTPException(status_code=400, detail="Time Não existe")

    db_jogadora = JogadoraDB(nome=jogadora.nome, id_time=time.id)
    session.add(db_jogadora)
    session.commit()
    session.refresh(db_jogadora)
    return {'message': 'User created!'}


@app.post(path="/cadastrar_gol", status_code=201, response_model=SchemaMessage)
def cadastrarGol(gol: SchemaPostGol, session=Depends(get_session)):
    jogo = session.scalar(select(JogoDB).where(JogoDB.id == gol.jogo_id))
    jogadora = session.scalar(select(JogadoraDB).where(JogadoraDB.id == gol.jogadora_id))
    time = session.scalar(select(TimeDB).where(TimeDB.id == jogadora.id_time))
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    if not jogadora:
        raise HTTPException(status_code=404, detail="Jogadora não encontrada")
    if not time:
        raise HTTPException(status_code=404, detail="Time da jogadora não encontrado")
    if time.id == jogo.time_1_id:
        jogo.gols_1 += 1
    elif time.id == jogo.time_2_id:
        jogo.gols_2 += 1
    else:
        raise HTTPException(status_code=400, detail="Jogadora não pertence a nenhum dos times do jogo")
    session.add(jogo)
    session.commit()
    session.refresh(jogo)
    return {"message": f"Gol registrado para {jogadora.nome} no jogo {jogo.id}"}

@app.post('/criar_chaveamento', status_code=201)
def criarChaveamento():
    pass

@app.post('/atualizar_placar_e_avancar', status_code=201)
def atualizar_placar_e_avancar():
    pass
