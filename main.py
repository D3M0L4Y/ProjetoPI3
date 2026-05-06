import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <-- Linha nova aqui
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

app = FastAPI(title="API Imobiliária Estrela")

# --- CONFIGURAÇÃO DE CORS (NOVO) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que qualquer site consuma a API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# ... (O resto do código das rotas continua igual para baixo)

@app.get("/")
def read_root():
    return {"mensagem": "API da Imobiliária Estrela rodando perfeitamente em Python!"}

# ROTA 1: Fornecimento de API (Lista todos os imóveis)
@app.get("/imoveis")
def listar_imoveis():
    query = "SELECT * FROM imoveis;"
    # O Pandas lê o banco e transforma em um DataFrame
    df = pd.read_sql(query, engine)
    
    # Converte datas para string para evitar erros no JSON
    if "data_cadastro" in df.columns:
        df["data_cadastro"] = df["data_cadastro"].astype(str)
        
    return df.to_dict(orient="records")

# ROTA 2: Análise de Dados (Requisito do Projeto Integrador)
@app.get("/analise")
def analise_dados():
    query = "SELECT * FROM imoveis;"
    df = pd.read_sql(query, engine)
    
    # Fazendo análises estatísticas automáticas com Pandas
    media_preco = df["preco"].mean()
    imoveis_por_cidade = df["cidade"].value_counts().to_dict()
    total_quartos = int(df["quartos"].sum())

    return {
        "insight": "Análise de Dados do Portfólio da Imobiliária",
        "total_imoveis_cadastrados": len(df),
        "preco_medio_mercado": round(media_preco, 2),
        "total_quartos_disponiveis": total_quartos,
        "distribuicao_por_cidade": imoveis_por_cidade
    }