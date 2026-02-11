import streamlit as st

st.set_page_config(
    page_title="Calculadora de Preço de Venda",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Calculadora de Preço de Venda")

st.markdown("Calcule o preço ideal para seu produto ou serviço considerando custos, impostos e margem de lucro.")

st.divider()

# -----------------------------
# ENTRADAS
# -----------------------------

st.subheader("📥 Dados de Entrada")

custo_produto = st.number_input("Custo do Produto (R$)", min_value=0.0, step=0.01)
frete = st.number_input("Frete / Custos Adicionais (R$)", min_value=0.0, step=0.01)

st.markdown("### Percentuais (%)")

margem = st.number_input("Margem de Lucro (%)", min_value=0.0, max_value=100.0, step=0.1)
impostos = st.number_input("Impostos (%)", min_value=0.0, max_value=100.0, step=0.1)
comissoes = st.number_input("Comissões (%)", min_value=0.0, max_value=100.0, step=0.1)
taxas = st.number_input("Taxas de Pagamento (%)", min_value=0.0, max_value=100.0, step=0.1)

st.divider()

# -----------------------------
# CÁLCULO
# -----------------------------

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

        st.write(f"• Custo Total: R$ {custo_total:,.2f}")
        st.write(f"• Impostos: R$ {valor_impostos:,.2f}")
        st.write(f"• Comissões: R$ {valor_comissao:,.2f}")
        st.write(f"• Taxas: R$ {valor_taxas:,.2f}")

        st.divider()

        # -----------------------------
        # SIMULAÇÃO DE CENÁRIOS
        # -----------------------------

        st.subheader("📈 Simulação de Cenários")

        cenarios = []

        for margem_simulada in [10, 20, 30, 40, 50]:
            percentual_simulado = (margem_simulada + impostos + comissoes + taxas) / 100
            if percentual_simulado < 1:
                preco_simulado = custo_total / (1 - percentual_simulado)
                cenarios.append({
                    "Margem (%)": margem_simulada,
                    "Preço de Venda (R$)": round(preco_simulado, 2)
                })

        st.table(cenarios)