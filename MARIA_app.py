import streamlit as st
import joblib
import os
import numpy as np
import pandas as pd
import requests


## Head
st.set_page_config(layout="wide")


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


with st.sidebar:
    img1a = 'https://media.meer.com/attachments/6e0514895e44505c7b68e082756d61d8c7760249/store/fill/690/388/ec6748c00eb0c873c497eeb74a8c05aa270d7d0b1da90c41c2a3c4cf7ad4/Medusa-particolare-della-statua-di-Luciano-Garbati-Ogni-donna-e-attraente-finche-linvidia-e-la.jpg'
    img_head = [img1a]
    st.image(img_head, width=300)
    st.markdown(f'<div><span style="color:#750014; font-size:40px; font-weight:bold;">M.A.R.I.A.</span></div>', unsafe_allow_html=True)
#    st.divider()
    st.write('#### Principal Investigators:')
#    img2 = 'https://radcliffe-harvard-edu.imgix.net/67a0f0b5-89c8-49ea-9565-ed9b7294a078/Minow-Martha_9123_radcliffe-TR.jpg?auto=compress%2Cformat&fit=min&fm=jpg&q=80&rect=257%2C486%2C1829%2C1819'
#    img3 = 'https://pbs.twimg.com/profile_images/1349456113046056961/j0BvBsaT_400x400.jpg'
#    images = [img2, img3]
#    st.image(images, width=64, caption=["Martha Minow", "Deb Roy"])
    st.write('Samuel Brasil')




# Carrega o modelo
model = joblib.load(model_filename)

# Lista de features esperadas pelo modelo, na ordem correta
expected_features = ['idade_vit', 'idade_agr', 'historico_ameaca', 'sexo_forcado', 'bo_mpu', 'frequente',
                     'agr_alcool_drogas', 'agr_doenca_mental', 'agr_descumpriu_mpu', 'agr_suicidio',
                     'agr_desempregado', 'agr_arma_fogo', 'agr_terceiro', 'vit_separacao_recente',
                     'vit_guarda_pensao', 'vit_filho_assistiu', 'vit_violencia_gravidez',
                     'vit_novo_relacionamento', 'vit_pne', 'moradia_violencia', 'dependencia_economica',
                     'etnia_amarela/oriental', 'etnia_branca', 'etnia_indígena', 'etnia_parda', 'etnia_preta',
                     'a_graves_Afogamento', 'a_graves_Enforcamento', 'a_graves_Facada', 'a_graves_Paulada',
                     'a_graves_Queimadura', 'a_graves_Sufocamento', 'a_graves_Tiro', 'agressoes_Chutes',
                     'agressoes_Empurrões', 'agressoes_puxoes_cabelo', 'agressoes_Socos', 'agressoes_Tapas']



# Define a função de previsão
def predict_decision(input_data):
    # Converte os dados de entrada em um DataFrame com as colunas na ordem correta
    input_df = pd.DataFrame([input_data], columns=expected_features)
    # Faz a previsão
    prediction = model.predict(input_df)
    prediction_proba = model.predict_proba(input_df)
    return prediction[0], prediction_proba[0][1]


# Layout do aplicativo Streamlit
# st.title('M.A.R.I.A.')
st.header('Modelagem da Avaliação de Risco com Inteligência Artificial')

st.write("""
This app predicts whether a protective measure will be granted based on the input data.
""")

# Bloco 1: Identificação das Partes
st.header("Informação das Partes")
idade_vitima = st.number_input("Idade da vítima", min_value=0, value=30, step=1)
idade_agressor = st.number_input("Idade do(a) agressor(a)", min_value=0, value=30, step=1)
vinculo = st.text_input("Vínculo entre a vítima e o(a) agressor(a)")
data = st.date_input("Data")

# Inicializa o dicionário de entrada com zeros para todas as features esperadas
input_data = {feature: 0 for feature in expected_features}

# Idades
input_data['idade_vit'] = idade_vitima
input_data['idade_agr'] = idade_agressor

# Bloco I: Sobre o Histórico de Violência
st.header("Bloco I - Sobre o Histórico de Violência")
ameacas = st.multiselect(
    "O(A) agressor(a) já ameaçou a vítima ou algum familiar?",
    ["Sim, utilizando arma de fogo", "Sim, utilizando faca", "Sim, de outra forma", "Não"]
)
input_data['historico_ameaca'] = 1 if any(option != "Não" for option in ameacas) else 0

# Agressões físicas graves
agressoes_fisicas = st.multiselect(
    "O(A) agressor(a) já praticou alguma(s) destas agressões físicas contra a vítima?",
    ["Afogamento", "Enforcamento", "Facada", "Paulada", "Queimadura", "Sufocamento", "Tiro"]
)
mapping_agressoes_graves = {
    "Afogamento": 'a_graves_Afogamento',
    "Enforcamento": 'a_graves_Enforcamento',
    "Facada": 'a_graves_Facada',
    "Paulada": 'a_graves_Paulada',
    "Queimadura": 'a_graves_Queimadura',
    "Sufocamento": 'a_graves_Sufocamento',
    "Tiro": 'a_graves_Tiro'
}
for ag in agressoes_fisicas:
    if ag in mapping_agressoes_graves:
        input_data[mapping_agressoes_graves[ag]] = 1

# Outras agressões físicas
outros_agressoes = st.multiselect(
    "O(A) agressor(a) já praticou alguma(s) destas outras agressões físicas contra a vítima?",
    ["Chutes", "Empurrões", "Puxões de Cabelo", "Socos", "Tapas"]
)
mapping_outros_agressoes = {
    "Chutes": 'agressoes_Chutes',
    "Empurrões": 'agressoes_Empurrões',
    "Puxões de Cabelo": 'agressoes_puxoes_cabelo',
    "Socos": 'agressoes_Socos',
    "Tapas": 'agressoes_Tapas'
}
for ag in outros_agressoes:
    if ag in mapping_outros_agressoes:
        input_data[mapping_outros_agressoes[ag]] = 1

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
    ["Sim, de álcool", "Sim, de drogas"]
)
input_data['agr_alcool_drogas'] = 1 if uso_abusivo else 0

# Doença mental
doenca_mental = st.radio(
    "O(A) agressor(a) tem doença mental comprovada?",
    ["Sim", "Não"]
)
input_data['agr_doenca_mental'] = 1 if doenca_mental == "Sim" else 0

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
    ["Sim", "Não"]
)
input_data['agr_desempregado'] = 1 if dificuldades_financeiras == "Sim" else 0

# Acesso a armas
acesso_armas = st.radio(
    "O(A) agressor(a) tem acesso a armas de fogo?",
    ["Sim", "Não"]
)
input_data['agr_arma_fogo'] = 1 if acesso_armas == "Sim" else 0

# Ameaçou outras pessoas
ameacou_outras_pessoas = st.multiselect(
    "O(A) agressor(a) já ameaçou ou agrediu outras pessoas ou animais?",
    ["Filhos", "Outros familiares", "Outras pessoas", "Animais"]
)
input_data['agr_terceiro'] = 1 if ameacou_outras_pessoas else 0

# Bloco III: Sobre a Vítima
st.header("Bloco III - Sobre a Vítima")
separacao_recente = st.radio(
    "A vítima se separou recentemente ou tentou se separar?",
    ["Sim", "Não"]
)
input_data['vit_separacao_recente'] = 1 if separacao_recente == "Sim" else 0

# Conflito sobre guarda ou pensão
conflito_guarda = st.radio(
    "A vítima vive conflito com o(a) agressor(a) sobre guarda, visitas ou pensão?",
    ["Sim", "Não"]
)
input_data['vit_guarda_pensao'] = 1 if conflito_guarda == "Sim" else 0

# Filhos presenciaram violência
filhos_presenciaram = st.radio(
    "Os filhos da vítima já presenciaram violência?",
    ["Sim", "Não"]
)
input_data['vit_filho_assistiu'] = 1 if filhos_presenciaram == "Sim" else 0

# Violência durante gravidez
violencia_gravidez = st.radio(
    "A vítima sofreu violência durante a gravidez ou pós-parto?",
    ["Sim", "Não"]
)
input_data['vit_violencia_gravidez'] = 1 if violencia_gravidez == "Sim" else 0

# Novo relacionamento
novo_relacionamento = st.radio(
    "As ameaças aumentaram devido a um novo relacionamento?",
    ["Sim", "Não"]
)
input_data['vit_novo_relacionamento'] = 1 if novo_relacionamento == "Sim" else 0

# Deficiência ou doença limitante
deficiencia_vulnerabilidade = st.radio(
    "A vítima possui deficiência ou doença limitante?",
    ["Sim", "Não"]
)
input_data['vit_pne'] = 1 if deficiencia_vulnerabilidade == "Sim" else 0

# Cor/Raça
cor_raca = st.selectbox(
    "Com qual cor/raça a vítima se identifica?",
    ["Amarela/Oriental", "Branca", "Indígena", "Parda", "Preta"]
)
cor_raca_mapping = {
    "Amarela/Oriental": "etnia_amarela/oriental",
    "Branca": "etnia_branca",
    "Indígena": "etnia_indígena",
    "Parda": "etnia_parda",
    "Preta": "etnia_preta"
}
# Zera todas as etnias
for etnia in cor_raca_mapping.values():
    input_data[etnia] = 0
# Seta a etnia selecionada
input_data[cor_raca_mapping[cor_raca]] = 1

# Bloco IV: Outras Informações
st.header("Bloco IV - Outras Informações")
bairro_risco = st.radio(
    "A vítima considera morar em área de risco?",
    ["Sim", "Não"]
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
