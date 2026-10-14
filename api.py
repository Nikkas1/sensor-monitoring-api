from fastapi import FastAPI, Request
import time
from datetime import datetime

app = FastAPI(title="Sensor Monitoring API")


observabilidade_logs = []

# Middleware para rastrear a latência e os headers de todas as requisições
@app.middleware("http")
async def rastrear_observabilidade(request: Request, call_next):
    start_time = time.time()
    
    # Processa a requisição e gera a resposta
    response = await call_next(request)
    
    # Calcula a latência em milissegundos
    process_time = time.time() - start_time
    latencia_ms = round(process_time * 1000, 2)
    
    
    x_session_id = request.headers.get("X-Session-Id", "Nao-Informado")
    x_feature = request.headers.get("X-Feature", "Nao-Informado")
    
    
    if request.url.path.startswith("/v1/"):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": request.url.path,
            "metodo": request.method,
            "latencia_ms": latencia_ms,
            "x_session_id": x_session_id,
            "x_feature": x_feature,
            "status_code": response.status_code
        }
        observabilidade_logs.append(log_entry)
        
    return response

@app.get("/v1/sensores/{tag}/leitura-atual")
def get_leitura_atual(tag: str):
    # Retorna dados simulados do sensor
    return {
        "tag": tag, 
        "leitura": 25.4, 
        "severidade": "Normal", 
        "unidade": "Celsius"
    }

@app.get("/v1/sensores/{tag}/historico")
def get_historico(tag: str):
    # Retorna histórico simulado
    historico = [
        {"data": "2026-10-14T00:00:00", "valor": 24.5},
        {"data": "2026-10-14T00:15:00", "valor": 25.1},
        {"data": "2026-10-14T00:30:00", "valor": 25.4},
        {"data": "2026-10-14T00:45:00", "valor": 26.0}
    ]
    return {"tag": tag, "historico": historico}

@app.get("/v1/observabilidade")
def get_observabilidade():
    # Retorna a lista de logs registrados
    return {"logs": observabilidade_logs}