# -*- coding: utf-8 -*-
"""Lab2-LucasDeLimaDaSilva-NotebookDadosTurma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FGrxp9pXmk49-H0peZ0mLlh5fpUmREco
"""

!pip install pandas numpy matplotlib seaborn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/content/dataset-turma.csv', sep=';')

print(df)

print(df.columns)

# PROJETO 1

df.columns = df.columns.str.strip()

linguagens = df['Marque as linguagens de programação que você já teve algum contato prático:'].str.split(',', expand=True).stack().reset_index(drop=True)
frequencia_linguagens = linguagens.value_counts()

print(frequencia_linguagens)

frequencia_linguagens_ordenada = frequencia_linguagens.sort_values(ascending=False)

df_frequencia = frequencia_linguagens_ordenada.reset_index()
df_frequencia.columns = ['Linguagem', 'Frequência']

plt.figure(figsize=(10, 6))
sns.barplot(x='Linguagem', y='Frequência', data=df_frequencia, color='skyblue', width=0.8)

plt.title('Distribuição das Linguagens de Programação Conhecidas pela Turma')
plt.ylabel('Número de Alunos')
plt.xlabel('Linguagens de Programação')

plt.show()

# PROJETO 2

df['Qtd_Linguagens'] = df['Marque as linguagens de programação que você já teve algum contato prático:'].apply(lambda x: len(x.split(',')))

df['Participacao_PD'] = df['Você já teve experiência de participação em projetos de Pesquisa e Desenvolvimento?'].apply(lambda x: 1 if x == 'Sim' else 0)

print(df[['Quantos semestres faltam para você se formar?', 'Qtd_Linguagens', 'Participacao_PD']].head())

import matplotlib.patches as mpatches

df_sorted = df.sort_values(by='Quantos semestres faltam para você se formar?', ascending=False)

colors = ['green' if p == 1 else 'blue' for p in df_sorted['Participacao_PD'].astype(int)]

bubble_size = df_sorted.groupby(['Quantos semestres faltam para você se formar?', 'Qtd_Linguagens']).transform('count')['Participacao_PD'] * 200 # Multiplicador para ajustar o tamanho

plt.figure(figsize=(10, 6))

plt.scatter(
    df_sorted['Quantos semestres faltam para você se formar?'],
    df_sorted['Qtd_Linguagens'],
    s=bubble_size,
    alpha=0.8,
    c=colors
)

plt.title('Correlação entre Semestres, Quantidade de Linguagens e Participação em P&D')
plt.xlabel('Semestres para Formar (Ordenado do maior para o menor)')
plt.ylabel('Quantidade de Linguagens de Programação')

plt.grid(True)

participou_patch = mpatches.Patch(color='green', label='Participou em P&D')
nao_participou_patch = mpatches.Patch(color='blue', label='Não Participou em P&D')

plt.legend(handles=[participou_patch, nao_participou_patch])

plt.show()

# PROJETO 3

conectividade_contagem = df['Selecione o seu Perfil de Conectividade neste semestre, dentre as opções a seguir:'].value_counts()

print(conectividade_contagem)

plt.figure(figsize=(8, 8))
plt.pie(conectividade_contagem, labels=conectividade_contagem.index, autopct='%1.1f%%', startangle=140)

plt.title('Distribuição do Perfil de Conectividade da Turma')

plt.show()