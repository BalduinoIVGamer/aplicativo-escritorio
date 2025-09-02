import streamlit as st

st.set_page_config(page_title="App Advocacia", page_icon="⚖️", layout="centered")

st.title("⚖️ App de Advocacia — Calculadora Financeira")

# Escolha do método
metodo = st.radio("Método de cálculo:", ["Percentual sobre a causa", "Por hora", "Valor fixo"])

honorarios = 0.0

if metodo == "Percentual sobre a causa":
    valor_causa = st.number_input("Valor da causa (R$)", min_value=0.0, step=100.0, format="%.2f")
    percentual = st.number_input("Percentual (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
    if st.button("Calcular Honorários"):
        honorarios = valor_causa * (percentual / 100)
        st.success(f"Honorários: R$ {honorarios:,.2f}")

elif metodo == "Por hora":
    valor_hora = st.number_input("Valor da hora (R$)", min_value=0.0, step=50.0, format="%.2f")
    horas = st.number_input("Horas trabalhadas", min_value=0.0, step=1.0)
    if st.button("Calcular Honorários"):
        honorarios = valor_hora * horas
        st.success(f"Honorários: R$ {honorarios:,.2f}")

else:  # Valor fixo
    valor_fixo = st.number_input("Valor fixo (R$)", min_value=0.0, step=100.0, format="%.2f")
    if st.button("Confirmar Honorários"):
        honorarios = valor_fixo
        st.success(f"Honorários: R$ {honorarios:,.2f}")

# ROI
st.subheader("📊 ROI — Retorno sobre Investimento")
investimento = st.number_input("Investimento (R$)", min_value=0.0, step=100.0, format="%.2f")
retorno = st.number_input("Retorno (R$)", min_value=0.0, step=100.0, format="%.2f")

if st.button("Calcular ROI"):
    if investimento > 0:
        roi = ((retorno - investimento) / investimento) * 100
        st.info(f"ROI: {roi:.2f}%")
    else:
        st.warning("O investimento deve ser maior que zero.")
