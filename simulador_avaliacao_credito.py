##################################
#                                #
#   rodar venv\Scripts\activate  #
#                                #
##################################

import streamlit as st
import pandas as pd
from joblib import load
from utils import Transformador

st.markdown('<style>div[role="listbox"] ul{background-color: #5E0A8A};</style>', unsafe_allow_html=True)

def carregar_dados():    
    #Carregando dados
    modelo = load('objetos/pipeline.joblib')
    features = load('objetos/features.joblib')
    return modelo, features

def avaliar_mau(dict_respostas):
    modelo, features = carregar_dados()
    if dict_respostas['Anos_desempregado'] > 0:
        dict_respostas['Anos_empregado'] = dict_respostas['Anos_desempregado'] * -1
    respostas = []
    for coluna in features:
        respostas.append(dict_respostas[coluna])
    df_novo_cliente = pd.DataFrame(data=[respostas],columns=features)
    #print(df_novo_cliente)
    mau = modelo.predict(df_novo_cliente)[0]
    return mau

st.image('img/LogoNakedBank.png')
st.markdown('<h1 style="text-align: center;">Simulador de Avaliação de Crédito</h1>', unsafe_allow_html = True)
st.markdown('<h3 style="text-align: center;">Bem vindo à nossa Avaliação de Crédito Online</h3>', unsafe_allow_html = True)
st.markdown(' ')
st.markdown('Seu uso é bem simples. Basta preencher seus dados nos campos abaixo e clicar no botão de **Avaliar Crédito** que você terá a resposta prévia, de acordo com seu perfil.')
st.markdown('Obrigado por escolher o nosso banco! Conte com a gente para realizar seus projetos pessoais!!!')

quadro_1 = st.beta_expander('🚶 Dados Pessoais 🚶')
quadro_2 = st.beta_expander('🏭 Dados Profissionais 🏭')
quadro_3  =st.beta_expander('👪 Dados Familiares 👪')
quadro_4 = st.beta_expander('💲 Dados Patrimoniais 💲')

lista_campos = load('objetos/lista_campos.joblib')

dict_respostas = {}

with quadro_1:
    col1_form, col2_form = st.beta_columns(2)
    dict_respostas['Idade'] = col1_form.slider('Idade', min_value = 0, max_value = 100, step = 1)
    dict_respostas['Grau_Escolaridade'] = col1_form.selectbox('Qual seu Grau de Escolaridade ?',
        lista_campos['Grau_Escolaridade'])
    dict_respostas['Tem_email'] = 1 if col2_form.radio('Tem email ?',  ['Sim','Não']) == 'Sim' else 0
    dict_respostas['Moradia'] = col2_form.selectbox('Qual o Tipo de Sua Moradia ?', lista_campos['Moradia'])

with quadro_2:
    col3_form, col4_form = st.beta_columns(2)
    dict_respostas['Categoria_de_renda'] = col3_form.selectbox('Categoria de Renda', lista_campos['Categoria_de_renda'])
    dict_respostas['Ocupacao'] = col3_form.selectbox('Ocupação', lista_campos['Ocupacao'])
    dict_respostas['Rendimento_Anual'] = col3_form.slider('Rendimento Mensal',
        min_value=0, max_value=35000, step=500) * 12
    dict_respostas['Tem_telefone_trabalho'] = 1 if col4_form.radio('Tem Telefone Comercial ?',
        ['Sim','Não']) == 'Sim' else 0
    dict_respostas['Anos_empregado'] = col4_form.slider('Anos no Emprego Atual',
        min_value=0, max_value=50, step=1)
    dict_respostas['Anos_desempregado'] = col4_form.slider('Anos Atualmente Desempregado',
        min_value=0, max_value=50, step=1)


with quadro_3:
    col5_form, col6_form = st.beta_columns(2)
    dict_respostas['Estado_Civil'] = col5_form.selectbox('Qual seu Estado Civil ?', lista_campos['Estado_Civil'])
    dict_respostas['Qtd_Filhos'] = col5_form.slider('Quantidade de Filhos', min_value=0, max_value=15, step=1)
    dict_respostas['Tamanho_Familia'] = col6_form.slider('Tamanho da Família', min_value=0, max_value=15, step=1)

with quadro_4:
    col7_form, col8_form = st.beta_columns(2)
    dict_respostas['Tem_Carro'] = 1 if col7_form.radio('Tem Carro ?', ['Sim','Não']) == 'Sim' else 0
    dict_respostas['Tem_Casa_Propria'] = 1 if col7_form.radio('Tem Casa Própria ?', ['Sim','Não']) == 'Sim' else 0
    dict_respostas['Tem_telefone_fixo'] = 1 if col8_form.radio('Tem Telefone Fixo ?', ['Sim','Não']) == 'Sim' else 0

if st.button('Avaliar Crédito'):
    if avaliar_mau(dict_respostas) == 1:
        st.error('Crédito Recusado :stop_sign: Mas não desanime! Entre em contato para analisarmos melhor seu caso!')
    else:
        st.success("Crédito Aprovado :handshake: Envie sua documentação em nossa página!")
        st.balloons()

st.caption('**OBS.:** Isso é apenas um simulador, a concessão de crédito depende da comprovação documental dos dados informados.')
st.caption('**OBS.2:** Detalhes desse projeto podem ser encontrados [aqui](https://github.com/gcochlar/Avaliacao_Credito).')