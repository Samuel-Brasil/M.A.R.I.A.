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
st.header("Identificação das Partes")
delegacia = st.text_input("Delegacia de Polícia")
nome_vitima = st.text_input("Nome da vítima")
idade_vitima = st.number_input("Idade da vítima", min_value=0, value=30, step=1)
escolaridade_vitima = st.selectbox(
    "Escolaridade da vítima",
    ["Nihil", "Fundamental", "Médio", "Superior", "Pós-graduação", "Mestrado", "Doutorado"]
)
nacionalidade_vitima = st.text_input("Nacionalidade da vítima")

nome_agressor = st.text_input("Nome do(a) agressor(a)")
idade_agressor = st.number_input("Idade do(a) agressor(a)", min_value=0, value=30, step=1)

escolaridade_agressor = st.selectbox(
    "Escolaridade do(a) agressor(a)",
    ["Nihil", "Fundamental", "Médio", "Superior", "Pós-graduação", "Mestrado", "Doutorado"]
)
nacionalidade_agressor = st.text_input("Nacionalidade do(a) agressor(a)")
vinculo = st.text_input("Vínculo entre a vítima e o(a) agressor(a)")
data = st.date_input("Data")

# Coleta dos dados para o modelo
input_data = {}

# Idades
input_data['idade_vitima'] = idade_vitima
input_data['idade_agressor'] = idade_agressor

# Escolaridade (convertida para numérico)
escolaridade_mapping = {
    "Nihil": 0,
    "Fundamental": 1,
    "Médio": 2,
    "Superior": 3,
    "Pós-graduação": 4,
    "Mestrado": 5,
    "Doutorado": 6
}
input_data['escolaridade_vitima'] = escolaridade_mapping[escolaridade_vitima]
input_data['escolaridade_agressor'] = escolaridade_mapping[escolaridade_agressor]

# Bloco I: Sobre o Histórico de Violência
st.header("Bloco I - Sobre o Histórico de Violência")
ameacas = st.multiselect(
    "O(A) agressor(a) já ameaçou você ou algum familiar?",
    ["Sim, utilizando arma de fogo", "Sim, utilizando faca", "Sim, de outra forma", "Não"]
)
input_data['ameaca_arma_fogo'] = 1 if "Sim, utilizando arma de fogo" in ameacas else 0
input_data['ameaca_faca'] = 1 if "Sim, utilizando faca" in ameacas else 0
input_data['ameaca_outra'] = 1 if "Sim, de outra forma" in ameacas else 0
input_data['ameaca_nao'] = 1 if "Não" in ameacas else 0

agressoes_fisicas = st.multiselect(
    "O(A) agressor(a) já praticou alguma(s) destas agressões físicas contra você?",
    ["Queimadura", "Enforcamento", "Sufocamento", "Tiro", "Afogamento", 
     "Facada", "Paulada", "Nenhuma das agressões acima"]
)
agressoes_fisicas_options = ["Queimadura", "Enforcamento", "Sufocamento", "Tiro", "Afogamento", 
                             "Facada", "Paulada", "Nenhuma das agressões acima"]
for ag in agressoes_fisicas_options:
    input_data[f"agressao_{ag.lower()}"] = 1 if ag in agressoes_fisicas else 0

outros_agressoes = st.multiselect(
    "O(A) agressor(a) já praticou alguma(s) destas outras agressões físicas contra você?",
    ["Socos", "Chutes", "Tapas", "Empurrões", "Puxões de Cabelo", "Nenhuma das agressões acima"]
)
outros_agressoes_options = ["Socos", "Chutes", "Tapas", "Empurrões", "Puxões de Cabelo", "Nenhuma das agressões acima"]
for ag in outros_agressoes_options:
    input_data[f"agressao_{ag.lower().replace(' ', '_')}"] = 1 if ag in outros_agressoes else 0

obrigou_sexo = st.radio(
    "O(A) agressor(a) já obrigou você a fazer sexo ou praticar atos sexuais contra sua vontade?",
    ["Sim", "Não"]
)
input_data['obrigou_sexo'] = 1 if obrigou_sexo == "Sim" else 0

comportamentos = st.multiselect(
    "O(A) agressor(a) já teve algum destes comportamentos?",
    [
        "Disse algo como: 'se não for minha, não será de mais ninguém'",
        "Perturbou, perseguiu ou vigiou você nos locais em que frequenta",
        "Proibiu você de visitar familiares ou amigos",
        "Proibiu você de trabalhar ou estudar",
        "Fez telefonemas ou enviou mensagens de forma insistente",
        "Impediu você de acessar dinheiro ou bens",
        "Ciúmes excessivos e controle",
        "Nenhum dos comportamentos acima"
    ]
)
comportamentos_options = [
    "Disse algo como: 'se não for minha, não será de mais ninguém'",
    "Perturbou, perseguiu ou vigiou você nos locais em que frequenta",
    "Proibiu você de visitar familiares ou amigos",
    "Proibiu você de trabalhar ou estudar",
    "Fez telefonemas ou enviou mensagens de forma insistente",
    "Impediu você de acessar dinheiro ou bens",
    "Ciúmes excessivos e controle",
    "Nenhum dos comportamentos acima"
]
for comp in comportamentos_options:
    key = comp[:20].replace(" ", "_").replace("'", "").replace(",", "").lower()
    input_data[f"comportamento_{key}"] = 1 if comp in comportamentos else 0

ocorrencia_registrada = st.radio(
    "Você já registrou ocorrência policial ou formulou pedido de medida protetiva?",
    ["Sim", "Não"]
)
input_data['ocorrencia_registrada'] = 1 if ocorrencia_registrada == "Sim" else 0

ameacas_recorrentes = st.radio(
    "As ameaças ou agressões se tornaram mais frequentes ou graves nos últimos meses?",
    ["Sim", "Não"]
)
input_data['ameacas_recorrentes'] = 1 if ameacas_recorrentes == "Sim" else 0

# Bloco II: Sobre o(a) Agressor(a)
st.header("Bloco II - Sobre o(a) Agressor(a)")
uso_abusivo = st.multiselect(
    "O(A) agressor(a) faz uso abusivo de álcool ou drogas?",
    ["Sim, de álcool", "Sim, de drogas", "Não", "Não sei"]
)
input_data['uso_abusivo_alcool'] = 1 if "Sim, de álcool" in uso_abusivo else 0
input_data['uso_abusivo_drogas'] = 1 if "Sim, de drogas" in uso_abusivo else 0
input_data['uso_abusivo_nao'] = 1 if "Não" in uso_abusivo else 0
input_data['uso_abusivo_nao_sei'] = 1 if "Não sei" in uso_abusivo else 0

doenca_mental = st.radio(
    "O(A) agressor(a) tem doença mental comprovada?",
    ["Sim, faz uso de medicação", "Sim, não faz uso de medicação", "Não", "Não sei"]
)
input_data['doenca_mental_usando_medicacao'] = 1 if doenca_mental == "Sim, faz uso de medicação" else 0
input_data['doenca_mental_nao_usando_medicacao'] = 1 if doenca_mental == "Sim, não faz uso de medicação" else 0
input_data['doenca_mental_nao'] = 1 if doenca_mental == "Não" else 0
input_data['doenca_mental_nao_sei'] = 1 if doenca_mental == "Não sei" else 0

descumpriu_medida = st.radio(
    "O(A) agressor(a) já descumpriu medida protetiva?",
    ["Sim", "Não"]
)
input_data['descumpriu_medida'] = 1 if descumpriu_medida == "Sim" else 0

tentou_suicidio = st.radio(
    "O(A) agressor(a) já tentou suicídio ou falou em suicidar-se?",
    ["Sim", "Não"]
)
input_data['tentou_suicidio'] = 1 if tentou_suicidio == "Sim" else 0

dificuldades_financeiras = st.radio(
    "O(A) agressor(a) está desempregado ou tem dificuldades financeiras?",
    ["Sim", "Não", "Não sei"]
)
input_data['dificuldades_financeiras_sim'] = 1 if dificuldades_financeiras == "Sim" else 0
input_data['dificuldades_financeiras_nao'] = 1 if dificuldades_financeiras == "Não" else 0
input_data['dificuldades_financeiras_nao_sei'] = 1 if dificuldades_financeiras == "Não sei" else 0

acesso_armas = st.radio(
    "O(A) agressor(a) tem acesso a armas de fogo?",
    ["Sim", "Não", "Não sei"]
)
input_data['acesso_armas_sim'] = 1 if acesso_armas == "Sim" else 0
input_data['acesso_armas_nao'] = 1 if acesso_armas == "Não" else 0
input_data['acesso_armas_nao_sei'] = 1 if acesso_armas == "Não sei" else 0

ameacou_outras_pessoas = st.multiselect(
    "O(A) agressor(a) já ameaçou ou agrediu outras pessoas ou animais?",
    ["Filhos", "Outros familiares", "Outras pessoas", "Animais", "Não", "Não sei"]
)
input_data['ameacou_filhos'] = 1 if "Filhos" in ameacou_outras_pessoas else 0
input_data['ameacou_outros_familiares'] = 1 if "Outros familiares" in ameacou_outras_pessoas else 0
input_data['ameacou_outras_pessoas'] = 1 if "Outras pessoas" in ameacou_outras_pessoas else 0
input_data['ameacou_animais'] = 1 if "Animais" in ameacou_outras_pessoas else 0
input_data['ameacou_nao'] = 1 if "Não" in ameacou_outras_pessoas else 0
input_data['ameacou_nao_sei'] = 1 if "Não sei" in ameacou_outras_pessoas else 0

# Bloco III: Sobre Você
st.header("Bloco III - Sobre Você")
separacao_recente = st.radio(
    "Você se separou recentemente ou tentou se separar?",
    ["Sim", "Não"]
)
input_data['separacao_recente'] = 1 if separacao_recente == "Sim" else 0

tem_filhos = st.radio(
    "Você tem filhos?",
    ["Sim, com o agressor", "Sim, de outro relacionamento", "Não"]
)
input_data['tem_filhos_com_agressor'] = 1 if tem_filhos == "Sim, com o agressor" else 0
input_data['tem_filhos_outro_relacionamento'] = 1 if tem_filhos == "Sim, de outro relacionamento" else 0
input_data['tem_filhos_nao'] = 1 if tem_filhos == "Não" else 0

if tem_filhos != "Não":
    faixa_etaria = st.multiselect(
        "Faixa etária dos filhos:",
        ["0 a 11 anos", "12 a 17 anos", "A partir de 18 anos"]
    )
    input_data['filhos_0_11'] = 1 if "0 a 11 anos" in faixa_etaria else 0
    input_data['filhos_12_17'] = 1 if "12 a 17 anos" in faixa_etaria else 0
    input_data['filhos_18_mais'] = 1 if "A partir de 18 anos" in faixa_etaria else 0

    filhos_deficiencia = st.radio(
        "Algum filho tem deficiência?",
        ["Sim", "Não"]
    )
    input_data['filhos_deficiencia'] = 1 if filhos_deficiencia == "Sim" else 0

    conflito_guarda = st.radio(
        "Você vive conflito com o(a) agressor(a) sobre guarda, visitas ou pensão?",
        ["Sim", "Não"]
    )
    input_data['conflito_guarda'] = 1 if conflito_guarda == "Sim" else 0

    filhos_presenciaram = st.radio(
        "Seus filhos já presenciaram violência?",
        ["Sim", "Não"]
    )
    input_data['filhos_presenciaram'] = 1 if filhos_presenciaram == "Sim" else 0

violencia_gravidez = st.radio(
    "Você sofreu violência durante a gravidez ou pós-parto?",
    ["Sim", "Não"]
)
input_data['violencia_gravidez'] = 1 if violencia_gravidez == "Sim" else 0

novo_relacionamento = st.radio(
    "As ameaças aumentaram devido a um novo relacionamento?",
    ["Sim", "Não"]
)
input_data['novo_relacionamento'] = 1 if novo_relacionamento == "Sim" else 0

deficiencia_vulnerabilidade = st.radio(
    "Você possui deficiência ou doença limitante?",
    ["Sim", "Não"]
)
input_data['deficiencia_vulnerabilidade'] = 1 if deficiencia_vulnerabilidade == "Sim" else 0

cor_raca = st.selectbox(
    "Com qual cor/raça você se identifica?",
    ["Branca", "Preta", "Parda", "Amarela/Oriental", "Indígena", "Não informada"]
)
cor_raca_options = ["Branca", "Preta", "Parda", "Amarela/Oriental", "Indígena", "Não informada"]
for cor in cor_raca_options:
    input_data[f"cor_{cor.replace('/', '_').replace(' ', '_').lower()}"] = 1 if cor_raca == cor else 0

# Bloco IV: Outras Informações
st.header("Bloco IV - Outras Informações")
bairro_risco = st.radio(
    "Você considera morar em área de risco?",
    ["Sim", "Não", "Não sei"]
)
input_data['bairro_risco_sim'] = 1 if bairro_risco == "Sim" else 0
input_data['bairro_risco_nao'] = 1 if bairro_risco == "Não" else 0
input_data['bairro_risco_nao_sei'] = 1 if bairro_risco == "Não sei" else 0

dependencia_financeira = st.radio(
    "Você é dependente financeiramente do(a) agressor(a)?",
    ["Sim", "Não"]
)
input_data['dependencia_financeira'] = 1 if dependencia_financeira == "Sim" else 0

# Bloco 1: Identificação das Partes
st.header("Predição")

# Realiza a previsão ao clicar no botão
if st.button('Prever'):
    prediction, probability = predict_decision(input_data)
    if prediction:
        st.success(f"O modelo prevê que a medida protetiva será **CONCEDIDA** com probabilidade de {probability:.2f}.")
    else:
        st.error(f"O modelo prevê que a medida protetiva será **NEGADA** com probabilidade de {1 - probability:.2f}.")
