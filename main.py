import streamlit as st

st.set_page_config(
    page_title="Calculadora de Preço de Venda",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Calculadora de Preço de Venda")

st.markdown(
    "Calcule o preço ideal para seu produto ou serviço considerando custos, impostos e margem de lucro."
)

# ---------------------------------------------------
# SIDEBAR - CENÁRIOS
# ---------------------------------------------------

st.sidebar.title("Cenários de Exemplo")

cenarios_exemplo = {
    "Nenhum": {
        "custo": 0.0,
        "frete": 0.0,
        "margem": 0.0,
        "impostos": 0.0,
        "comissoes": 0.0,
        "taxas": 0.0,
    },
    "Revenda de Produto": {
        "custo": 45.0,
        "frete": 5.0,
        "margem": 30.0,
        "impostos": 12.0,
        "comissoes": 5.0,
        "taxas": 3.0,
    },
    "Serviço Freelancer": {
        "custo": 300.0,
        "frete": 0.0,
        "margem": 40.0,
        "impostos": 6.0,
        "comissoes": 0.0,
        "taxas": 4.0,
    },
    "Pequeno Negócio": {
        "custo": 8.0,
        "frete": 2.0,
        "margem": 35.0,
        "impostos": 10.0,
        "comissoes": 8.0,
        "taxas": 2.0,
    },
    "Produção Artesanal": {
        "custo": 12.0,
        "frete": 3.0,
        "margem": 50.0,
        "impostos": 8.0,
        "comissoes": 0.0,
        "taxas": 3.0,
    },
}

cenario_selecionado = st.sidebar.selectbox(
    "Escolha um cenário:",
    list(cenarios_exemplo.keys())
)

dados = cenarios_exemplo[cenario_selecionado]

st.divider()

# ---------------------------------------------------
# ENTRADAS
# ---------------------------------------------------

st.subheader("📥 Dados de Entrada")

custo_produto = st.number_input(
    "Custo do Produto (R$)", value=dados["custo"], min_value=0.0, step=0.01
)

frete = st.number_input(
    "Frete / Custos Adicionais (R$)", value=dados["frete"], min_value=0.0, step=0.01
)

st.markdown("### Percentuais (%)")

margem = st.number_input(
    "Margem de Lucro (%)", value=dados["margem"], min_value=0.0, max_value=100.0
)

impostos = st.number_input(
    "Impostos (%)", value=dados["impostos"], min_value=0.0, max_value=100.0
)

comissoes = st.number_input(
    "Comissões (%)", value=dados["comissoes"], min_value=0.0, max_value=100.0
)

taxas = st.number_input(
    "Taxas de Pagamento (%)", value=dados["taxas"], min_value=0.0, max_value=100.0
)

st.divider()

# ---------------------------------------------------
# CÁLCULO
# ---------------------------------------------------

if st.button("Calcular Preço de Venda"):

    custo_total = custo_produto + frete
    percentual_total = (margem + impostos + comissoes + taxas) / 100

    if percentual_total >= 1:
        st.error("A soma dos percentuais não pode ser 100% ou mais.")
    else:
        preco_venda = custo_total / (1 - percentual_total)

        valor_impostos = preco_venda * (impostos / 100)
        valor_comissao = preco_venda * (comissoes / 100)
        valor_taxas = preco_venda * (taxas / 100)
        lucro_reais = preco_venda * (margem / 100)

        st.success("Cálculo realizado com sucesso!")

        st.subheader("📊 Resultado")

        st.metric("Preço de Venda Ideal", f"R$ {preco_venda:,.2f}")
        st.metric("Lucro em Reais", f"R$ {lucro_reais:,.2f}")

        st.markdown("### 📋 Detalhamento")

        st.write(f"Custo Total: R$ {custo_total:,.2f}")
        st.write(f"Impostos: R$ {valor_impostos:,.2f}")
        st.write(f"Comissões: R$ {valor_comissao:,.2f}")
        st.write(f"Taxas: R$ {valor_taxas:,.2f}")
