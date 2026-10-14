import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000/v1"

st.set_page_config(page_title="Forzy Digital Twin", layout="wide")
st.title("🔌 Monitoramento de Sensores e Observabilidade")

# Headers exigidos pela disciplina de Governança
headers_contexto = {
    "X-Session-Id": "sessao_admin_123",
    "X-Feature": "painel_streamlit"
}

tag_sensor = st.text_input("Tag do Sensor", value="sensor_temperatura_motor_A")

if st.button("Buscar Dados do Sensor"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Leitura Atual")
        try:
            res_atual = requests.get(f"{API_URL}/sensores/{tag_sensor}/leitura-atual", headers=headers_contexto)
            if res_atual.status_code == 200:
                dados = res_atual.json()
                st.metric(label=f"Sensor: {dados['tag']}", value=f"{dados['leitura']} {dados['unidade']}", delta=dados['severidade'])
                st.json(dados)
            else:
                st.error("Erro ao buscar a leitura atual da API.")
        except Exception as e:
            st.error(f"A API está rodando? Erro de conexão: {e}")

    with col2:
        st.subheader("Histórico (Gráfico)")
        try:
            res_hist = requests.get(f"{API_URL}/sensores/{tag_sensor}/historico", headers=headers_contexto)
            if res_hist.status_code == 200:
                dados_hist = res_hist.json().get("historico", [])
                if dados_hist:
                    # Monta o DataFrame para o Streamlit gerar o gráfico de linha automaticamente
                    df = pd.DataFrame(dados_hist)
                    df['data'] = pd.to_datetime(df['data'])
                    st.line_chart(df.set_index("data"))
                else:
                    st.warning("Histórico vazio.")
            else:
                st.error("Erro ao buscar o histórico.")
        except Exception as e:
            pass # Erro já tratado no bloco anterior

st.divider()

st.subheader("📊 Registros de Observabilidade (Governança)")
st.caption("Esses são os dados que a sua API registrou. Seu amigo usará isso para auditar latência e requisições.")

if st.button("Atualizar Tabela de Observabilidade"):
    try:
        res_obs = requests.get(f"{API_URL}/observabilidade", headers=headers_contexto)
        if res_obs.status_code == 200:
            logs = res_obs.json().get("logs", [])
            if logs:
                df_logs = pd.DataFrame(logs)
                st.dataframe(df_logs, use_container_width=True)
            else:
                st.info("Nenhum log registrado ainda. Clique em 'Buscar Dados do Sensor' ali em cima primeiro para gerar registros!")
    except Exception as e:
        st.error("Não foi possível conectar à API de observabilidade.")