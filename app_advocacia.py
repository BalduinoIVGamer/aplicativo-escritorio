import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="App Advocacia", page_icon="⚖️", layout="wide")

# Logo no topo
tst_logo = "logo.png"  # imagem local na mesma pasta
st.image(tst_logo, width=200)
st.title("⚖️ App de Advocacia")

# ------------------------------
# Menu de abas
# ------------------------------
aba = st.sidebar.radio(
    "Navegação",
    ["📊 Calculadora Financeira", "📈 Projeção de Crescimento", "👥 Gestão de Clientes", "📘 Sobre o eBook"]
)

# ------------------------------
# 1) Calculadora Financeira
# ------------------------------
if aba == "📊 Calculadora Financeira":
    st.header("📊 Calculadora Financeira")

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

# ------------------------------
# 2) Projeção de Crescimento
# ------------------------------
elif aba == "📈 Projeção de Crescimento":
    st.header("📈 Projeção de Crescimento do Escritório")

    clientes_iniciais = st.number_input("Clientes atuais", min_value=0, step=1)
    novos_clientes_mes = st.number_input("Novos clientes por mês", min_value=0, step=1)
    ticket_medio = st.number_input("Ticket médio por cliente (R$)", min_value=0.0, step=100.0, format="%.2f")
    crescimento_percentual = st.slider("Taxa de crescimento (%) ao mês", 0, 50, 5)

    meses = [6, 12, 24]
    projecoes = {}

    for m in meses:
        clientes = clientes_iniciais + (novos_clientes_mes * m)
        clientes = int(clientes * ((1 + crescimento_percentual/100) ** m))
        receita = clientes * ticket_medio
        projecoes[m] = {"clientes": clientes, "receita": receita}

    st.subheader("Projeções Resumidas")
    df = pd.DataFrame(projecoes).T
    st.dataframe(df.style.format({"receita": "R$ {:,.2f}"}))

    st.subheader("📊 Gráfico de Receita")
    fig, ax = plt.subplots()
    ax.plot(df.index, df["receita"], marker="o")
    ax.set_xlabel("Meses")
    ax.set_ylabel("Receita (R$)")
    ax.set_title("Projeção de Receita")
    st.pyplot(fig)

# ------------------------------
# 3) Gestão de Clientes
# ------------------------------
elif aba == "👥 Gestão de Clientes":
    st.header("👥 Gestão de Clientes")

    if "clientes" not in st.session_state:
        st.session_state.clientes = []

    with st.form("cadastro_cliente"):
        nome = st.text_input("Nome do cliente")
        causa = st.text_input("Tipo de causa")
        valor = st.number_input("Valor da causa (R$)", min_value=0.0, step=100.0, format="%.2f")
        submit = st.form_submit_button("Cadastrar Cliente")

        if submit and nome:
            st.session_state.clientes.append({"Nome": nome, "Causa": causa, "Valor": valor})
            st.success(f"Cliente {nome} cadastrado!")

    if st.session_state.clientes:
        df_clientes = pd.DataFrame(st.session_state.clientes)
        st.subheader("📋 Lista de Clientes")
        st.dataframe(df_clientes)

        # Exportar CSV
        csv = df_clientes.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar CSV", csv, "clientes.csv", "text/csv")

# ------------------------------
# 4) Sobre o eBook
# ------------------------------
else:
    st.header("📘 Sobre o eBook")
    st.image("capa_ebook.png", caption="Capa do eBook", use_column_width=True)
    st.write("Este aplicativo acompanha o eBook de Direito, com dicas práticas para advogados e escritórios.")
    st.markdown("[📖 Clique aqui para acessar o eBook](https://exemplo.com/seu-ebook.pdf)")
