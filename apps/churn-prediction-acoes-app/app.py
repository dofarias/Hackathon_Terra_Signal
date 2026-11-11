"""App de predição de churn de clientes — Terra Signal (Telecom).

Recebe os dados de um cliente via formulário e consulta o endpoint de
Model Serving `churn-prediction-endpoint`, que serve o modelo registrado
no Unity Catalog (workspace.default.hackathon_databricks_model) e retorna
a probabilidade de churn do cliente.
"""

import requests
import streamlit as st
from databricks.sdk.core import Config

ENDPOINT = "churn-prediction-endpoint"

st.set_page_config(
    page_title="Terra Signal — Predição de Churn",
    page_icon="📡",
    layout="wide",
)

st.title("📡 Terra Signal — Predição de Churn")
st.caption(
    "Telecom Terra Signal: preencha os dados do cliente para estimar a "
    "probabilidade de cancelamento do serviço, com base no modelo registrado em "
    "`workspace.default.hackathon_databricks_model` (servido via endpoint "
    "de Model Serving)."
)

st.sidebar.caption(f"Scoring via endpoint `{ENDPOINT}`")
st.sidebar.markdown("📡 **Terra Signal** · Telecom")

# Tema visual Terra Signal — azul corporativo de Telecom
st.markdown(
    """
    <style>
    /* Barra superior em gradiente azul Terra Signal */
    header[data-testid="stHeader"] {
        background: linear-gradient(90deg, #003B73 0%, #0057B8 60%, #2E7CD6 100%);
    }
    /* Título principal em azul corporativo */
    h1 {
        color: #003B73;
    }
    /* Borda do formulário em azul claro */
    div[data-testid="stForm"] {
        border: 1px solid #B9D3F2;
        border-radius: 10px;
    }
    /* Cabeçalhos de seção do formulário em azul */
    div[data-testid="stForm"] h3 {
        color: #0057B8;
    }
    /* Botão de envio azul sólido */
    div[data-testid="stForm"] button {
        background-color: #0057B8;
        border-color: #0057B8;
        color: #FFFFFF;
    }
    /* Métricas de resultado com fundo azul claro */
    div[data-testid="stMetric"] {
        background-color: #EAF2FB;
        border-radius: 8px;
        padding: 0.6rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def predict_churn(record: dict) -> float:
    """Consulta o endpoint de serving e retorna a probabilidade de churn."""
    cfg = Config()  # credenciais OAuth do service principal do app
    resp = requests.post(
        f"{cfg.host.rstrip('/')}/serving-endpoints/{ENDPOINT}/invocations",
        headers=cfg.authenticate(),
        json={"dataframe_records": [record]},
        timeout=(10, 300),  # cold start pode levar alguns minutos
    )
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:500]}")
    return float(resp.json()["predictions"][0])


with st.form("dados_cliente", border=True):
    st.subheader("Dados do cliente")

    c1, c2 = st.columns(2)
    gender = c1.selectbox("Gênero", ["Male", "Female"])
    senior = c2.selectbox("Idoso (65+)", ["Não", "Sim"])
    senior_citizen = 1 if senior == "Sim" else 0

    c4, c5, c6 = st.columns(3)
    partner = c4.selectbox("Possui parceiro(a)?", ["No", "Yes"])
    dependents = c5.selectbox("Possui dependentes?", ["No", "Yes"])
    tenure = c6.number_input(
        "Meses de contrato (tenure)", min_value=0, max_value=120, value=12, step=1
    )

    st.subheader("Serviços contratados")

    c7, c8 = st.columns(2)
    phone_service = c7.selectbox("Serviço de telefone", ["Yes", "No"])
    multiple_lines = c8.selectbox(
        "Múltiplas linhas", ["No", "Yes", "No phone service"]
    )
    internet_service = c7.selectbox(
        "Serviço de internet", ["DSL", "Fiber optic", "No"]
    )

    no_internet = "No internet service"
    g1, g2, g3 = st.columns(3)
    online_security = g1.selectbox("Segurança online", ["Yes", "No", no_internet])
    online_backup = g2.selectbox("Backup online", ["No", "Yes", no_internet])
    device_protection = g3.selectbox("Proteção de dispositivo", ["No", "Yes", no_internet])

    g4, g5, g6 = st.columns(3)
    tech_support = g4.selectbox("Suporte técnico", ["No", "Yes", no_internet])
    streaming_tv = g5.selectbox("Streaming TV", ["No", "Yes", no_internet])
    streaming_movies = g6.selectbox("Streaming filmes", ["No", "Yes", no_internet])

    st.subheader("Contrato e cobrança")

    h1, h2 = st.columns(2)
    contract = h1.selectbox(
        "Tipo de contrato", ["Month-to-month", "One year", "Two year"]
    )
    paperless_billing = h2.selectbox("Fatura digital (paperless)", ["Yes", "No"])
    payment_method = h1.selectbox(
        "Forma de pagamento",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)",
        ],
    )

    i1, i2 = st.columns(2)
    monthly_charges = i1.number_input(
        "Cobrança mensal (R$/mês)", min_value=0.0, value=70.0, step=0.1
    )
    total_charges = i2.number_input(
        "Cobrança total acumulada", min_value=0.0, value=500.0, step=0.1
    )

    st.subheader("Perfil socioeconômico")

    monthly_income = st.number_input(
        "Renda mensal (R$)", min_value=0, value=5000, step=100
    )

    submitted = st.form_submit_button("🔮 Calcular probabilidade de churn",
                                     use_container_width=True)

if submitted:
    registro = {
        "customerID": "não informado",
        "gender": gender,
        "SeniorCitizen": int(senior_citizen),
        "Partner": partner,
        "Dependents": dependents,
        "tenure": str(int(tenure)),
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": float(monthly_charges),
        "TotalCharges": float(total_charges),
        "CustomerFeedback": "não informado",
        "MonthlyIncome": int(monthly_income),
        "motivo_feedback": "não informado",
    }

    try:
        with st.spinner(
            "Consultando o endpoint de serving... (a primeira chamada após "
            "um período de inatividade pode levar alguns minutos)"
        ):
            churn_prob = predict_churn(registro)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Falha ao calcular a predição: {exc}")
        st.stop()

    st.divider()
    st.subheader("Resultado")

    # Faixas de risco: <= 60% baixo (verde); > 60% e < 75% moderado (laranja); >= 75% alto (vermelho)
    if churn_prob <= 0.60:
        nivel, emoji, cor = 'Risco baixo', '🟢', '#1E8E3E'
    elif churn_prob < 0.75:
        nivel, emoji, cor = 'Risco moderado', '🟠', '#E37400'
    else:
        nivel, emoji, cor = 'Risco alto', '🔴', '#D93025'

    k1, k2 = st.columns(2)
    k1.metric('Probabilidade de churn', f'{churn_prob:.1%}')
    k2.metric('Faixa de risco', f'{emoji} {nivel}')

    st.markdown(
        f'''
        <div style='
            background-color: {cor}1A;
            border-left: 5px solid {cor};
            padding: 0.6rem 1rem;
            border-radius: 6px;
            font-size: 1.1rem;
        '>
            <b style='color: {cor};'>{emoji} {nivel}</b>
            <span style='color: #333333;'>— probabilidade de churn de {churn_prob:.1%}</span>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    st.progress(min(churn_prob, 1.0), text=f'Probabilidade de churn: {churn_prob:.1%}')

    # Sugestões de ação (aplicadas apenas quando a probabilidade de churn é maior que 60%)
    st.subheader('Sugestões de ação')

    if churn_prob <= 0.60:
        st.success('Sem ação sugerida — a probabilidade de churn está na faixa de baixo risco (até 60%).')
    else:
        sugestoes = []

        if contract == 'Month-to-month':
            sugestoes.append(
                '📌 **Contrato**: cliente com contrato month-to-month — oferecer migração '
                'para contrato de 1 ano (One year) ou 2 anos (Two year) com desconto padrão.'
            )

        itens_protecao = [
            ('Segurança online (OnlineSecurity)', online_security),
            ('Suporte técnico (TechSupport)', tech_support),
            ('Backup online (OnlineBackup)', online_backup),
        ]
        faltantes = [nome for nome, valor in itens_protecao if valor == 'No']
        if internet_service != 'No' and faltantes:
            itens_txt = ', '.join(f'**{nome}**' for nome in faltantes)
            sugestoes.append(
                '🛡️ **Serviços de proteção**: cliente com serviço de internet ativo e '
                'itens de proteção não contratados — oferecer adesão de: ' + itens_txt + '.'
            )

        if payment_method == 'Electronic check':
            sugestoes.append(
                '💳 **Forma de pagamento**: cliente paga via Electronic check — oferecer '
                'alteração para Bank transfer (automatic) ou Credit card (automatic).'
            )

        if sugestoes:
            for sugestao in sugestoes:
                st.info(sugestao)
        else:
            st.info(
                'Nenhuma ação adicional sugerida com base nos critérios atuais '
                '(probabilidade de churn acima de 60%, mas sem condições elegíveis).'
            )

    with st.expander('Ver dados enviados ao modelo'):
        st.json(registro)