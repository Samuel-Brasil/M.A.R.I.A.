import streamlit as st
import joblib
import os
import numpy as np
import pandas as pd
import requests

model_filename = 'best_model.joblib'

if not os.path.exists(model_filename):
    with st.spinner('Baixando o modelo...'):
        url = 'https://github.com/Samuel-Brasil/M.A.R.I.A./releases/download/v1.3/best_model.joblib'
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(model_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            st.success('Modelo baixado com sucesso.')
        else:
            st.error('Falha ao baixar o modelo.')
            st.stop()

# Carrega o modelo
model = joblib.load(model_filename)

# Define a função de previsão
def predict_decision(input_data):
    # Converte os dados de entrada em um DataFrame
    input_df = pd.DataFrame([input_data])
    # Faz a previsão
    prediction = model.predict(input_df)
    prediction_proba = model.predict_proba(input_df)
    return prediction[0], prediction_proba[0][1]

# Layout do aplicativo Streamlit
st.title('M.A.R.I.A.')
st.write('### Modelagem da Avaliação de Risco com Inteligência Artificial')

st.write("""
This app predicts whether a protective measure will be granted based on the input data.
""")

# Bloco 1: Identificação das Partes
st.header("Informação das Partes")
# Coleta das informações de idade
idade_vitima = st.number_input("Idade da vítima", min_value=0, value=30, step=1)
escolaridade_vitima = st.selectbox(
    "Escolaridade da vítima",
    ["Nihil", "Fundamental", "Médio", "Superior", "Pós-graduação", "Mestrado", "Doutorado"]
)
idade_agressor = st.number_input("Idade do(a) agressor(a)", min_value=0, value=30, step=1)
escolaridade_agressor = st.selectbox(
    "Escolaridade do(a) agressor(a)",
    ["Nihil", "Fundamental", "Médio", "Superior", "Pós-graduação", "Mestrado", "Doutorado"]
)
vinculo = st.text_input("Vínculo entre a vítima e o(a) agressor(a)")
data = st.date_input("Data")

# Coleta dos dados para o modelo
input_data = {}

# Idades (ajustando os nomes das colunas)
input_data['idade_vit'] = idade_vitima
input_data['idade_agr'] = idade_agressor

# As variáveis de escolaridade não estão presentes no dataset, portanto, não serão incluídas em input_data

# Bloco I: Sobre o Histórico de Violência
st.header("Bloco I - Sobre o Histórico de Violência")
ameacas = st.multiselect(
    "O(A) agressor(a) já ameaçou a vítima ou algum familiar?",
    ["Sim, utilizando arma de fogo", "Sim, utilizando faca", "Sim, de outra forma", "Não"]
)

# Mapeando para 'historico_ameaca' no dataset
input_data['historico_ameaca'] = 1 if any(option != "Não" for option in ameacas) else 0

# Agressões físicas graves
agressoes_fisicas = st.multiselect(
    "O(A) agressor(a) já praticou alguma(s) destas agressões físicas contra a vítima?",
    ["Queimadura", "Enforcamento", "Sufocamento", "Tiro", "Afogamento",
     "Facada", "Paulada", "Nenhuma das agressões acima"]
)
agressoes_fisicas_options = ["Afogamento", "Enforcamento", "Facada", "Paulada",
                             "Queimadura", "Sufocamento", "Tiro", "Nenhuma das agressões acima"]
for ag in agressoes_fisicas_options:
    key = f"a_graves_{ag}"
    input_data[key] = 1 if ag in agressoes_fisicas else 0

# Outras agressões físicas
outros_agressoes = st.multiselect(
    "O(A) agressor(a) já praticou alguma(s) destas outras agressões físicas contra a vítima?",
    ["Socos", "Chutes", "Tapas", "Empurrões", "Puxões de Cabelo", "Nenhuma das agressões acima"]
)
outros_agressoes_options = ["Socos", "Chutes", "Tapas", "Empurrões", "puxoes_cabelo", "Nenhuma das agressões acima"]
for ag in outros_agressoes_options:
    key = f"agressoes_{ag}"
    input_data[key] = 1 if ag in outros_agressoes else 0

# Obrigação de sexo
obrigou_sexo = st.radio(
    "O(A) agressor(a) já obrigou a vítima a fazer sexo ou praticar atos sexuais contra sua vontade?",
    ["Sim", "Não"]
)
input_data['sexo_forcado'] = 1 if obrigou_sexo == "Sim" else 0

# Ocorrência policial ou medida protetiva
ocorrencia_registrada = st.radio(
    "A vítima já registrou ocorrência policial ou formulou pedido de medida protetiva?",
    ["Sim", "Não"]
)
input_data['bo_mpu'] = 1 if ocorrencia_registrada == "Sim" else 0

# Ameaças ou agressões frequentes
ameacas_recorrentes = st.radio(
    "As ameaças ou agressões se tornaram mais frequentes ou graves nos últimos meses?",
    ["Sim", "Não"]
)
input_data['frequente'] = 1 if ameacas_recorrentes == "Sim" else 0

# Bloco II: Sobre o(a) Agressor(a)
st.header("Bloco II - Sobre o(a) Agressor(a)")
uso_abusivo = st.multiselect(
    "O(A) agressor(a) faz uso abusivo de álcool ou drogas?",
    ["Sim, de álcool", "Sim, de drogas", "Não", "Não sei"]
)
# Mapeando para 'agr_alcool_drogas' no dataset
input_data['agr_alcool_drogas'] = 1 if any(option in ["Sim, de álcool", "Sim, de drogas"] for option in uso_abusivo) else 0

# Doença mental
doenca_mental = st.radio(
    "O(A) agressor(a) tem doença mental comprovada?",
    ["Sim, faz uso de medicação", "Sim, não faz uso de medicação", "Não", "Não sei"]
)
input_data['agr_doenca_mental'] = 1 if doenca_mental.startswith("Sim") else 0

# Descumpriu medida protetiva
descumpriu_medida = st.radio(
    "O(A) agressor(a) já descumpriu medida protetiva?",
    ["Sim", "Não"]
)
input_data['agr_descumpriu_mpu'] = 1 if descumpriu_medida == "Sim" else 0

# Tentou suicídio
tentou_suicidio = st.radio(
    "O(A) agressor(a) já tentou suicídio ou falou em suicidar-se?",
    ["Sim", "Não"]
)
input_data['agr_suicidio'] = 1 if tentou_suicidio == "Sim" else 0

# Dificuldades financeiras
dificuldades_financeiras = st.radio(
    "O(A) agressor(a) está desempregado ou tem dificuldades financeiras?",
    ["Sim", "Não", "Não sei"]
)
input_data['agr_desempregado'] = 1 if dificuldades_financeiras == "Sim" else 0

# Acesso a armas
acesso_armas = st.radio(
    "O(A) agressor(a) tem acesso a armas de fogo?",
    ["Sim", "Não", "Não sei"]
)
input_data['agr_arma_fogo'] = 1 if acesso_armas == "Sim" else 0

# Ameaçou outras pessoas
ameacou_outras_pessoas = st.multiselect(
    "O(A) agressor(a) já ameaçou ou agrediu outras pessoas ou animais?",
    ["Filhos", "Outros familiares", "Outras pessoas", "Animais", "Não", "Não sei"]
)
input_data['agr_terceiro'] = 1 if any(option in ["Filhos", "Outros familiares", "Outras pessoas", "Animais"] for option in ameacou_outras_pessoas) else 0

# Bloco III: Sobre a Vítima
st.header("Bloco III - Sobre a Vítima")
separacao_recente = st.radio(
    "A vítima se separou recentemente ou tentou se separar?",
    ["Sim", "Não"]
)
input_data['vit_separacao_recente'] = 1 if separacao_recente == "Sim" else 0

tem_filhos = st.radio(
    "A vítima tem filhos?",
    ["Sim, com o agressor", "Sim, de outro relacionamento", "Não"]
)
# Não há coluna específica para 'tem_filhos', então não adicionamos ao input_data

if tem_filhos != "Não":
    faixa_etaria = st.multiselect(
        "Faixa etária dos filhos:",
        ["0 a 11 anos", "12 a 17 anos", "A partir de 18 anos"]
    )
    filhos_presenciaram = st.radio(
        "Os filhos da vítima já presenciaram violência?",
        ["Sim", "Não"]
    )
    input_data['vit_filho_assistiu'] = 1 if filhos_presenciaram == "Sim" else 0

    conflito_guarda = st.radio(
        "A vítima vive conflito com o(a) agressor(a) sobre guarda, visitas ou pensão?",
        ["Sim", "Não"]
    )
    input_data['vit_guarda_pensao'] = 1 if conflito_guarda == "Sim" else 0

    filhos_deficiencia = st.radio(
        "Algum filho tem deficiência?",
        ["Sim", "Não"]
    )
    # Não há coluna específica para 'filhos_deficiencia', então não adicionamos ao input_data

violencia_gravidez = st.radio(
    "A vítima sofreu violência durante a gravidez ou pós-parto?",
    ["Sim", "Não"]
)
input_data['vit_violencia_gravidez'] = 1 if violencia_gravidez == "Sim" else 0

novo_relacionamento = st.radio(
    "As ameaças aumentaram devido a um novo relacionamento?",
    ["Sim", "Não"]
)
input_data['vit_novo_relacionamento'] = 1 if novo_relacionamento == "Sim" else 0

deficiencia_vulnerabilidade = st.radio(
    "A vítima possui deficiência ou doença limitante?",
    ["Sim", "Não"]
)
input_data['vit_pne'] = 1 if deficiencia_vulnerabilidade == "Sim" else 0

cor_raca = st.selectbox(
    "Com qual cor/raça a vítima se identifica?",
    ["Branca", "Preta", "Parda", "Amarela/Oriental", "Indígena", "Não informada"]
)
cor_raca_mapping = {
    "Branca": "etnia_branca",
    "Preta": "etnia_preta",
    "Parda": "etnia_parda",
    "Amarela/Oriental": "etnia_amarela/oriental",
    "Indígena": "etnia_indígena",
    "Não informada": "etnia_nao_informada"
}
for cor in cor_raca_mapping.values():
    input_data[cor] = 0
if cor_raca != "Não informada":
    input_data[cor_raca_mapping[cor_raca]] = 1

# Bloco IV: Outras Informações
st.header("Bloco IV - Outras Informações")
bairro_risco = st.radio(
    "A vítima considera morar em área de risco?",
    ["Sim", "Não", "Não sei"]
)
input_data['moradia_violencia'] = 1 if bairro_risco == "Sim" else 0

dependencia_financeira = st.radio(
    "A vítima é dependente financeiramente do(a) agressor(a)?",
    ["Sim", "Não"]
)
input_data['dependencia_economica'] = 1 if dependencia_financeira == "Sim" else 0

# Bloco V: Predição
st.header("Bloco V - Predição")

# Realiza a previsão ao clicar no botão
if st.button('Prever'):
    prediction, probability = predict_decision(input_data)
    if prediction:
        st.success(f"O modelo prevê que a medida protetiva será **CONCEDIDA** com probabilidade de {probability:.2f}.")
    else:
        st.error(f"O modelo prevê que a medida protetiva será **NEGADA** com probabilidade de {1 - probability:.2f}.")
