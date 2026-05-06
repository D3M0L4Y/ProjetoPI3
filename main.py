import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# 1. Tenta carregar o .env (funciona no seu PC)
load_dotenv()

# 2. Pega a URL (Prioriza o que estiver no painel do Render)
DATABASE_URL = os.environ.get("DATABASE_URL")

# Se a URL vier vazia, o código para aqui com um aviso claro
if not DATABASE_URL:
    print("ERRO CRÍTICO: DATABASE_URL não encontrada nas variáveis de ambiente!")
    # Apenas para teste local se tudo falhar, você pode colocar a string direta aqui, 
    # mas o ideal é que o Render forneça.
    raise ValueError("DATABASE_URL is missing!")

# 3. Ajuste de compatibilidade (O Render às vezes usa postgres:// e o SQLAlchemy exige postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 4. Criar o motor do banco
engine = create_engine(DATABASE_URL)

app = FastAPI(title="API Imobiliária Estrela")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # O asterisco permite que qualquer site (incluindo o GitHub) acesse sua API
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, etc.
    allow_headers=["*"], # Permite todos os cabeçalhos
)
# ... resto do código (CORS e Rotas)
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