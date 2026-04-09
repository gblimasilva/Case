import pandas as pd
import os

# Captura o diretório onde o script está sendo executado
diretorio_atual = os.getcwd()

# Define apenas os nomes dos arquivos
nome_arquivo_entrada = "CNAE20_EstruturaDetalhada.xlsx"
nome_arquivo_saida = "CNAE20_Padronizado.xlsx"

# Cria os caminhos dinâmicos unindo a pasta atual com o nome do arquivo
file_path = os.path.join(diretorio_atual, nome_arquivo_entrada)
output_path = os.path.join(diretorio_atual, nome_arquivo_saida)

print(f"Buscando arquivo em: {file_path}")

# Ler o arquivo
df = pd.read_excel(file_path)

# Selecionar apenas as colunas relevantes
df_limpo = df[['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']].copy()
df_limpo.columns = ['Grupo', 'Classe', 'Descricao']

# Criar uma coluna unificada de código
df_limpo['CNAE'] = df_limpo['Grupo'].fillna(df_limpo['Classe'])

# Remover linhas sem código
df_limpo = df_limpo[df_limpo['CNAE'].notna()]

# Limpar espaços e caracteres estranhos
df_limpo['CNAE'] = df_limpo['CNAE'].astype(str).str.strip()
df_limpo['Descricao'] = df_limpo['Descricao'].astype(str).str.strip()

# Filtrar apenas códigos de 3 e 4 dígitos (padrões CNAE)
df_limpo = df_limpo[
    df_limpo['CNAE'].str.match(r'^\d{2}\.\d{1,2}$') | 
    df_limpo['CNAE'].str.match(r'^\d{2}\.\d{1,2}-\d$')
]

# Selecionar e renomear colunas finais
df_final = df_limpo[['CNAE', 'Descricao']].drop_duplicates().reset_index(drop=True)

# Exportar resultado
df_final.to_excel(output_path, index=False)

print("Base CNAE limpa gerada com sucesso em:", output_path)