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
# SIDEBAR
# -----------------------------
st.sidebar.title("Cenários")

cenarios_exemplo = {
    "Manual": (0, 0, 0, 0, 0, 0),
    "Revenda": (45, 5, 30, 12, 5, 3),
    "Freelancer": (300, 0, 40, 6, 0, 4),
    "Pequeno Negócio": (8, 2, 35, 10, 8, 2),
}

opcao = st.sidebar.selectbox("Escolha um cenário", list(cenarios_exemplo.keys()))

custo, frete, margem, impostos, comissoes, taxas = cenarios_exemplo[opcao]

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

custos_fixos = st.number_input("Custos Fixos Mensais", value=1000.0)

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

        # MARKUP
        markup = preco / custo_total if custo_total > 0 else 0

        # PONTO DE EQUILÍBRIO
        margem_contribuicao = preco - (custo_total + impostos_v + comissao_v + taxas_v)
        ponto_equilibrio = custos_fixos / margem_contribuicao if margem_contribuicao > 0 else 0

        # KPIs
        c1, c2, c3 = st.columns(3)
        c1.metric("Preço de Venda", f"R$ {preco:,.2f}")
        c2.metric("Lucro", f"R$ {lucro_v:,.2f}")
        c3.metric("Markup", f"{markup:.2f}x")

        st.metric("Ponto de Equilíbrio (unidades)", f"{ponto_equilibrio:.1f}")

        st.divider()

        # -----------------------------
        # GRÁFICO COMPOSIÇÃO
        # -----------------------------
        st.subheader("Composição do preço")

        componentes = {
            "Custo": custo_total,
            "Impostos": impostos_v,
            "Comissões": comissao_v,
            "Taxas": taxas_v,
            "Lucro": lucro_v,
        }

        componentes_filtrados = {k: v for k, v in componentes.items() if v > 0}

        labels = list(componentes_filtrados.keys())
        valores = list(componentes_filtrados.values())

        cores = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F"]

        fig1, ax1 = plt.subplots()
        ax1.pie(
            valores,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=cores[:len(valores)],
            wedgeprops={"linewidth": 1, "edgecolor": "white"},
        )
        ax1.axis("equal")
        st.pyplot(fig1)

        st.divider()

        # -----------------------------
        # GRÁFICO LUCRO VS CUSTO
        # -----------------------------
        st.subheader("Lucro vs Custo")

        fig2, ax2 = plt.subplots()
        categorias = ["Custo Total", "Lucro"]
        valores_barra = [custo_total, lucro_v]

        ax2.bar(categorias, valores_barra)
        ax2.set_ylabel("Valor (R$)")
        st.pyplot(fig2)

        st.divider()

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
