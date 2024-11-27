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

# Bloco 1: Identificação das Partes
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

# Bloco I: Histórico de Violência
st.header("Bloco I - Sobre o Histórico de Violência")
ameacas = st.multiselect(
    "O(A) agressor(a) já ameaçou você ou algum familiar?",
    ["Sim, utilizando arma de fogo", "Sim, utilizando faca", "Sim, de outra forma", "Não"]
)
agressoes_fisicas = st.multiselect(
    "O(A) agressor(a) já praticou alguma(s) destas agressões físicas contra você?",
    ["Queimadura", "Enforcamento", "Sufocamento", "Tiro", "Afogamento", 
     "Facada", "Paulada", "Nenhuma das agressões acima"]
)
outros_agressoes = st.multiselect(
    "O(A) agressor(a) já praticou alguma(s) destas outras agressões físicas contra você?",
    ["Socos", "Chutes", "Tapas", "Empurrões", "Puxões de Cabelo", "Nenhuma das agressões acima"]
)
obrigou_sexo = st.radio(
    "O(A) agressor(a) já obrigou você a fazer sexo ou praticar atos sexuais contra sua vontade?",
    ["Sim", "Não"]
)
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
ocorrencia_registrada = st.radio(
    "Você já registrou ocorrência policial ou formulou pedido de medida protetiva?",
    ["Sim", "Não"]
)
ameacas_recorrentes = st.radio(
    "As ameaças ou agressões se tornaram mais frequentes ou graves nos últimos meses?",
    ["Sim", "Não"]
)

# Bloco II: Sobre o(a) Agressor(a)
st.header("Bloco II - Sobre o(a) Agressor(a)")
uso_abusivo = st.multiselect(
    "O(A) agressor(a) faz uso abusivo de álcool ou drogas?",
    ["Sim, de álcool", "Sim, de drogas", "Não", "Não sei"]
)
doenca_mental = st.radio(
    "O(A) agressor(a) tem doença mental comprovada?",
    ["Sim, faz uso de medicação", "Sim, não faz uso de medicação", "Não", "Não sei"]
)
descumpriu_medida = st.radio(
    "O(A) agressor(a) já descumpriu medida protetiva?",
    ["Sim", "Não"]
)
tentou_suicidio = st.radio(
    "O(A) agressor(a) já tentou suicídio ou falou em suicidar-se?",
    ["Sim", "Não"]
)
dificuldades_financeiras = st.radio(
    "O(A) agressor(a) está desempregado ou tem dificuldades financeiras?",
    ["Sim", "Não", "Não sei"]
)
acesso_armas = st.radio(
    "O(A) agressor(a) tem acesso a armas de fogo?",
    ["Sim", "Não", "Não sei"]
)
ameaçou_outras_pessoas = st.multiselect(
    "O(A) agressor(a) já ameaçou ou agrediu outras pessoas ou animais?",
    ["Filhos", "Outros familiares", "Outras pessoas", "Animais", "Não", "Não sei"]
)

# Bloco III: Sobre Você
st.header("Bloco III - Sobre Você")
separacao_recente = st.radio(
    "Você se separou recentemente ou tentou se separar?",
    ["Sim", "Não"]
)
tem_filhos = st.radio(
    "Você tem filhos?",
    ["Sim, com o agressor", "Sim, de outro relacionamento", "Não"]
)
if tem_filhos != "Não":
    faixa_etaria = st.multiselect(
        "Faixa etária dos filhos:",
        ["0 a 11 anos", "12 a 17 anos", "A partir de 18 anos"]
    )
    filhos_deficiencia = st.radio(
        "Algum filho tem deficiência?",
        ["Sim", "Não"]
    )
    conflito_guarda = st.radio(
        "Você vive conflito com o(a) agressor(a) sobre guarda, visitas ou pensão?",
        ["Sim", "Não"]
    )
    filhos_presenciaram = st.radio(
        "Seus filhos já presenciaram violência?",
        ["Sim", "Não"]
    )
violencia_gravidez = st.radio(
    "Você sofreu violência durante a gravidez ou pós-parto?",
    ["Sim", "Não"]
)
novo_relacionamento = st.radio(
    "As ameaças aumentaram devido a um novo relacionamento?",
    ["Sim", "Não"]
)
deficiencia_vulnerabilidade = st.radio(
    "Você possui deficiência ou doença limitante?",
    ["Sim", "Não"]
)
cor_raca = st.radio(
    "Com qual cor/raça você se identifica?",
    ["Branca", "Preta", "Parda", "Amarela/Oriental", "Indígena"]
)

# Bloco IV: Outras Informações Importantes
st.header("Bloco IV - Outras Informações")
bairro_risco = st.radio(
    "Você considera morar em área de risco?",
    ["Sim", "Não", "Não sei"]
)
dependencia_financeira = st.radio(
    "Você é dependente financeiramente do(a) agressor(a)?",
    ["Sim", "Não"]
)

# Botão para salvar os dados
if st.button("Salvar dados"):
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
        "Ameaças": [", ".join(ameacas)],
        "Agressões Físicas": [", ".join(agressoes_fisicas)],
        "Outras Agressões": [", ".join(outros_agressoes)],
        "Obrigou Sexo": [obrigou_sexo],
        "Comportamentos": [", ".join(comportamentos)],
        "Ocorrência Registrada": [ocorrencia_registrada],
        "Ameaças Frequentes": [ameacas_recorrentes],
        "Uso Abusivo": [", ".join(uso_abusivo)],
        "Doença Mental": [doenca_mental],
        "Descumpriu Medida": [descumpriu_medida],
        "Tentou Suicídio": [tentou_suicidio],
        "Dificuldades Financeiras": [dificuldades_financeiras],
        "Acesso a Armas": [acesso_armas],
        "Ameaçou Outras Pessoas": [", ".join(ameaçou_outras_pessoas)],
        "Separação Recente": [separacao_recente],
        "Tem Filhos": [tem_filhos],
        "Faixa Etária dos Filhos": [", ".join(faixa_etaria) if tem_filhos != "Não" else ""],
        "Filhos com Deficiência": [filhos_deficiencia if tem_filhos != "Não" else ""],
        "Conflito de Guarda": [conflito_guarda if tem_filhos != "Não" else ""],
        "Filhos Presenciaram": [filhos_presenciaram if tem_filhos != "Não" else ""],
        "Violência Gravidez": [violencia_gravidez],
        "Novo Relacionamento": [novo_relacionamento],
        "Deficiência/Vulnerabilidade": [deficiencia_vulnerabilidade],
        "Cor/Raça": [cor_raca],
        "Bairro de Risco": [bairro_risco],
        "Dependência Financeira": [dependencia_financeira]
    }

    df = pd.DataFrame(data_dict)
    save_to_excel(df, excel_file)
    st.success("Dados salvos com sucesso!")

# Botão para download do arquivo
if os.path.exists(excel_file):
    with open(excel_file, "rb") as file:
        st.download_button(
            label="Baixar planilha Excel",
            data=file,
            file_name=excel_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
