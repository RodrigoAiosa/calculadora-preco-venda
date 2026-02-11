import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Precificador",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# ESTILO (cards simples)
# -----------------------------
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f7f7f7;
    margin-bottom: 10px;
    border: 1px solid #e6e6e6;
}
.metric-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #ffffff;
    border: 1px solid #e6e6e6;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Precificador de Produtos e Serviços")

# -----------------------------
# SESSION STATE
# -----------------------------
if "cenarios_salvos" not in st.session_state:
    st.session_state.cenarios_salvos = {}

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Cenários")

cenarios_exemplo = {
    "Manual": None,
    "Revenda": (45, 5, 30, 12, 5, 3),
    "Freelancer": (300, 0, 40, 6, 0, 4),
    "Pequeno Negócio": (8, 2, 35, 10, 8, 2),
}

opcao = st.sidebar.selectbox(
    "Escolha um cenário",
    list(cenarios_exemplo.keys()) + list(st.session_state.cenarios_salvos.keys())
)

def carregar(op):
    if op in cenarios_exemplo and cenarios_exemplo[op]:
        return cenarios_exemplo[op]
    if op in st.session_state.cenarios_salvos:
        return st.session_state.cenarios_salvos[op]
    return (0, 0, 0, 0, 0, 0)

custo, frete, margem, impostos, comissoes, taxas = carregar(opcao)

# -----------------------------
# INPUTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    custo = st.number_input("Custo", value=float(custo))
    frete = st.number_input("Custos adicionais", value=float(frete))
    margem = st.number_input("Margem (%)", value=float(margem))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    impostos = st.number_input("Impostos (%)", value=float(impostos))
    comissoes = st.number_input("Comissões (%)", value=float(comissoes))
    taxas = st.number_input("Taxas (%)", value=float(taxas))
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# CÁLCULO
# -----------------------------
if st.button("Calcular"):

    custo_total = custo + frete
    perc_total = (margem + impostos + comissoes + taxas) / 100

    if perc_total >= 1:
        st.error("Percentuais inválidos")
    else:
        preco = custo_total / (1 - perc_total)

        impostos_v = preco * (impostos / 100)
        comissao_v = preco * (comissoes / 100)
        taxas_v = preco * (taxas / 100)
        lucro_v = preco * (margem / 100)

        # -----------------------------
        # CARDS RESULTADO
        # -----------------------------
        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Preço de Venda", f"R$ {preco:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Lucro", f"R$ {lucro_v:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        # -----------------------------
        # GRÁFICO DE COMPOSIÇÃO
        # -----------------------------
        st.subheader("Composição do preço")

        labels = ["Custo", "Impostos", "Comissões", "Taxas", "Lucro"]
        valores = [custo_total, impostos_v, comissao_v, taxas_v, lucro_v]

        fig, ax = plt.subplots()
        ax.pie(valores, labels=labels, autopct='%1.1f%%')
        st.pyplot(fig)

        st.divider()

        # -----------------------------
        # SIMULAÇÃO
        # -----------------------------
        st.subheader("Simulação de Margens")

        simulacao = []
        for m in [10, 20, 30, 40, 50]:
            p = (m + impostos + comissoes + taxas) / 100
            if p < 1:
                preco_sim = custo_total / (1 - p)
                simulacao.append([m, round(preco_sim, 2)])

        df = pd.DataFrame(simulacao, columns=["Margem %", "Preço"])

        st.dataframe(df)

        # -----------------------------
        # EXPORTAR CSV
        # -----------------------------
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Exportar simulação CSV", csv, "simulacao.csv")

# -----------------------------
# SALVAR CENÁRIO
# -----------------------------
st.sidebar.divider()
st.sidebar.subheader("Salvar cenário")

nome = st.sidebar.text_input("Nome do cenário")

if st.sidebar.button("Salvar"):
    st.session_state.cenarios_salvos[nome] = (
        custo,
        frete,
        margem,
        impostos,
        comissoes,
        taxas
    )
    st.sidebar.success("Cenário salvo!")
