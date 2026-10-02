# titulo - Sistema de vendas
# Seção Cadastrar Vendas
    # Campo Data
    # Campo Vendedor - Ana, Bruno, Carla
    # Campo produto - Notebook, Fone, Celular
    # Campo quantidade 
    # Campo valor
    # Botão Cadastrar Venda
        # Quando eu clicar no botão -> adicionar a venda na tabela
# Seção Vendas Cadastradas
    # Tabela com as vendas
# Seção Dashboard
    # Card/metrica -> Faturamento total
    # Grafico de barra/coluna -> Venda por vendedor
    # Grafico de pizza -> Venda por produto

import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# carregar a base de vendas
tabela_vendas = pd.read_csv("vendas.csv")

st.write("# Sistema de vendas KMS")
st.title = "KMS System"

# Seção cadastro de vendas
st.sidebar.write("## Cadastrar Vendas")
data = st.sidebar.date_input("Data", min_value="today")
vendedor = st.sidebar.selectbox("Vendedor", ["Ana", "Bruno", "Carla"])
produto = st.sidebar.selectbox("Produto", ["Notebook", "Fone", "Celular"])
quantidade = st.sidebar.number_input("Quantidade", step=1)
valor = st.sidebar.number_input("Valor")
botao_cadastrar = st.sidebar.button("Cadastrar Venda")

# logica de cadastro
if botao_cadastrar:
    if quantidade <= 0:
        st.warning("O campo quantidade não foi preenchido!")
        # Script JS para colocar o foco de volta no campo Data
        focus_script = """
        <script>
            const input = window.parent.document.querySelector('input[aria-label="Quantidade"]');
            if (input) {
                input.focus();
            }
        </script>
        """
        components.html(focus_script, height=0)      

    if valor <= 0:
        st.warning("O campo valor não foi preenchido!")
        # Script JS para colocar o foco de volta no campo Data
        focus_script = """
        <script>
            const input = window.parent.document.querySelector('input[aria-label="Valor"]');
            if (input) {
                input.focus();
            }
        </script>
        """
        components.html(focus_script, height=0)  

    nova_venda = [str(data), vendedor, produto, quantidade, valor]
    ultima_linha = len(tabela_vendas)       
    tabela_vendas.loc[ultima_linha] = nova_venda  
    tabela_vendas.to_csv("vendas.csv", index=False)
    
    st.success("Venda cadastrada com sucesso!")

# Seção visualizar vendas
st.dataframe(tabela_vendas)

# Seção Dashboard
st.write("## Dashboard")
faturamento = tabela_vendas["valor"].sum()
st.metric("Faturamento Total", f"R$ {faturamento}")

# Grafico de Barra/Coluna -> venda por vendedor
grafico1 = px.bar(tabela_vendas, x="vendedor", y="valor", color="produto")
st.plotly_chart(grafico1)

# Grafico de pizza -> venda por produto
grafico2 = px.pie(tabela_vendas, names="produto", values="valor", hole=0.5)
st.plotly_chart(grafico2)