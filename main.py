import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(
    page_title="Precificador",
    page_icon="💰",
    layout="wide"
)

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
    custo = st.number_input("Custo", value=float(custo))
    frete = st.number_input("Custos adicionais", value=float(frete))
    margem = st.number_input("Margem (%)", value=float(margem))

with col2:
    impostos = st.number_input("Impostos (%)", value=float(impostos))
    comissoes = st.number_input("Comissões (%)", value=float(comissoes))
    taxas = st.number_input("Taxas (%)", value=float(taxas))

st.divider()

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
        # MARKUP
        # -----------------------------
        markup = preco / custo_total if custo_total > 0 else 0

        # -----------------------------
        # PONTO DE EQUILÍBRIO
        # -----------------------------
        custos_fixos = st.number_input("Custos Fixos Mensais", value=1000.0)
        margem_contribuicao = preco - (custo_total + impostos_v + comissao_v + taxas_v)

        if margem_contribuicao > 0:
            ponto_equilibrio = custos_fixos / margem_contribuicao
        else:
            ponto_equilibrio = 0

        st.subheader("Resultados")

        c1, c2, c3 = st.columns(3)
        c1.metric("Preço de Venda", f"R$ {preco:,.2f}")
        c2.metric("Lucro", f"R$ {lucro_v:,.2f}")
        c3.metric("Markup", f"{markup:.2f}x")

        st.metric("Ponto de Equilíbrio (unidades)", f"{ponto_equilibrio:.1f}")

        st.divider()

        # -----------------------------
        # GRÁFICO
        # -----------------------------
        labels = ["Custo", "Impostos", "Comissões", "Taxas", "Lucro"]
        valores = [custo_total, impostos_v, comissao_v, taxas_v, lucro_v]

        fig, ax = plt.subplots()
        ax.pie(valores, labels=labels, autopct='%1.1f%%')
        st.pyplot(fig)

        # -----------------------------
        # SIMULAÇÃO
        # -----------------------------
        simulacao = []
        for m in [10, 20, 30, 40, 50]:
            p = (m + impostos + comissoes + taxas) / 100
            if p < 1:
                preco_sim = custo_total / (1 - p)
                simulacao.append([m, round(preco_sim, 2)])

        df = pd.DataFrame(simulacao, columns=["Margem %", "Preço"])
        st.dataframe(df)

        # -----------------------------
        # EXPORTAR XLSX
        # -----------------------------
        relatorio = pd.DataFrame({
            "Custo Produto": [custo],
            "Frete": [frete],
            "Custo Total": [custo_total],
            "Preço Venda": [preco],
            "Lucro": [lucro_v],
            "Markup": [markup],
            "Impostos": [impostos_v],
            "Comissões": [comissao_v],
            "Taxas": [taxas_v],
            "Ponto Equilíbrio": [ponto_equilibrio]
        })

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            relatorio.to_excel(writer, index=False, sheet_name="Relatorio")
            df.to_excel(writer, index=False, sheet_name="Simulacao")

        st.download_button(
            "Baixar relatório XLSX",
            output.getvalue(),
            "relatorio_precificacao.xlsx"
        )

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
