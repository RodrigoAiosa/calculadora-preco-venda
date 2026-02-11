import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Precificador MEI", page_icon="💼", layout="wide")

st.title("💼 Precificador Profissional para MEI")
st.markdown("Ferramenta estratégica para definição de preço sustentável.")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Configurações MEI")

simples = st.sidebar.number_input("Imposto Simples Nacional (%)", value=6.0)
meta_faturamento = st.sidebar.number_input("Meta de Faturamento Mensal (R$)", value=10000.0)

# -----------------------------
# INPUTS PRINCIPAIS
# -----------------------------
st.subheader("Custos Variáveis por Unidade")

col1, col2 = st.columns(2)

with col1:
    custo_produto = st.number_input("Custo do Produto/Serviço", value=0.0)
    frete = st.number_input("Frete / Custos adicionais", value=0.0)
    comissoes = st.number_input("Comissões (%)", value=0.0)

with col2:
    taxas = st.number_input("Taxas de Pagamento (%)", value=0.0)
    margem = st.number_input("Margem de Lucro Desejada (%)", value=30.0)
    custos_fixos = st.number_input("Custos Fixos Mensais (R$)", value=2000.0)

st.divider()

# -----------------------------
# CÁLCULO
# -----------------------------
if st.button("Calcular Precificação"):

    custo_total = custo_produto + frete
    impostos_total = simples + comissoes + taxas + margem
    percentual_total = impostos_total / 100

    if percentual_total >= 1:
        st.error("Percentual total inválido.")
    else:
        preco = custo_total / (1 - percentual_total)

        imposto_v = preco * (simples / 100)
        comissao_v = preco * (comissoes / 100)
        taxa_v = preco * (taxas / 100)
        lucro_v = preco * (margem / 100)

        markup = preco / custo_total if custo_total > 0 else 0

        margem_contribuicao = preco - (custo_total + imposto_v + comissao_v + taxa_v)
        ponto_equilibrio = custos_fixos / margem_contribuicao if margem_contribuicao > 0 else 0

        preco_minimo = custo_total / (1 - ((simples + comissoes + taxas) / 100))

        unidades_meta = meta_faturamento / preco if preco > 0 else 0

        # -----------------------------
        # KPIs
        # -----------------------------
        st.subheader("Indicadores Estratégicos")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Preço Ideal", f"R$ {preco:,.2f}")
        c2.metric("Lucro por Unidade", f"R$ {lucro_v:,.2f}")
        c3.metric("Markup", f"{markup:.2f}x")
        c4.metric("Preço Mínimo Sustentável", f"R$ {preco_minimo:,.2f}")

        st.metric("Ponto de Equilíbrio (unidades)", f"{ponto_equilibrio:.1f}")
        st.metric("Unidades para atingir meta", f"{unidades_meta:.0f}")

        st.divider()

        # -----------------------------
        # GRÁFICO COMPOSIÇÃO
        # -----------------------------
        st.subheader("Composição do Preço")

        componentes = {
            "Custo": custo_total,
            "Imposto MEI": imposto_v,
            "Comissões": comissao_v,
            "Taxas": taxa_v,
            "Lucro": lucro_v,
        }

        componentes_filtrados = {k: v for k, v in componentes.items() if v > 0}

        fig1, ax1 = plt.subplots()
        ax1.pie(
            list(componentes_filtrados.values()),
            labels=list(componentes_filtrados.keys()),
            autopct="%1.1f%%",
            startangle=90,
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
        ax2.bar(["Custo Total", "Lucro"], [custo_total, lucro_v])
        ax2.set_ylabel("Valor (R$)")
        st.pyplot(fig2)

        st.divider()

        # -----------------------------
        # RELATÓRIO XLSX
        # -----------------------------
        relatorio = pd.DataFrame({
            "Custo Produto": [custo_produto],
            "Frete": [frete],
            "Custo Total": [custo_total],
            "Preço Ideal": [preco],
            "Preço Mínimo": [preco_minimo],
            "Lucro": [lucro_v],
            "Markup": [markup],
            "Ponto Equilíbrio": [ponto_equilibrio],
            "Unidades Meta": [unidades_meta],
        })

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            relatorio.to_excel(writer, index=False, sheet_name="Relatorio")

        st.download_button(
            "📥 Baixar Relatório Profissional (XLSX)",
            output.getvalue(),
            "relatorio_precificacao_mei.xlsx"
        )
