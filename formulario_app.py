import streamlit as st
import pandas as pd
import os

# Função para salvar dados no Excel
def save_to_excel(data, file_path):
    if os.path.exists(file_path):
        existing_data = pd.read_excel(file_path)
        updated_data = pd.concat([existing_data, data], ignore_index=True)
    else:
        updated_data = data
    updated_data.to_excel(file_path, index=False)

# Nome do arquivo Excel
excel_file = "dados_violencia_domestica.xlsx"

# Título
st.title("Formulário Nacional de Avaliação de Risco - Violência Doméstica")

# Campos do formulário
st.header("Identificação das Partes")
delegacia = st.text_input("Delegacia de Polícia")
nome_vitima = st.text_input("Nome da vítima")
idade_vitima = st.number_input("Idade da vítima", min_value=0, step=1)
escolaridade_vitima = st.text_input("Escolaridade da vítima")
nacionalidade_vitima = st.text_input("Nacionalidade da vítima")

nome_agressor = st.text_input("Nome do(a) agressor(a)")
idade_agressor = st.number_input("Idade do(a) agressor(a)", min_value=0, step=1)
escolaridade_agressor = st.text_input("Escolaridade do(a) agressor(a)")
nacionalidade_agressor = st.text_input("Nacionalidade do(a) agressor(a)")
vinculo = st.text_input("Vínculo entre a vítima e o(a) agressor(a)")
data = st.date_input("Data")

# Exemplo de mais campos
st.header("Bloco I - Sobre o histórico de violência")
ameacas = st.selectbox(
    "O(A) agressor(a) já ameaçou você ou algum familiar?",
    ["Sim, utilizando arma de fogo", "Sim, utilizando faca", "Sim, de outra forma", "Não"]
)

# Botão para salvar os dados
if st.button("Salvar dados"):
    # Estrutura de dados
    data_dict = {
        "Delegacia": [delegacia],
        "Nome da vítima": [nome_vitima],
        "Idade da vítima": [idade_vitima],
        "Escolaridade da vítima": [escolaridade_vitima],
        "Nacionalidade da vítima": [nacionalidade_vitima],
        "Nome do(a) agressor(a)": [nome_agressor],
        "Idade do(a) agressor(a)": [idade_agressor],
        "Escolaridade do(a) agressor(a)": [escolaridade_agressor],
        "Nacionalidade do(a) agressor(a)": [nacionalidade_agressor],
        "Vínculo": [vinculo],
        "Data": [data],
        "Ameaças": [ameacas]
    }
    
    # Criar DataFrame
    df = pd.DataFrame(data_dict)
    
    # Salvar no Excel
    save_to_excel(df, excel_file)
    st.success("Dados salvos com sucesso!")

# Link para baixar o arquivo Excel
if os.path.exists(excel_file):
    with open(excel_file, "rb") as file:
        st.download_button(
            label="Baixar planilha Excel",
            data=file,
            file_name=excel_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
