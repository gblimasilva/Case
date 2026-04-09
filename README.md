# Case Analista de Dados: Análise de Acidentes de Trabalho

## 📌 Proposta do Case
Este projeto tem como objetivo analisar o cenário nacional de acidentes de trabalho a partir de dados abertos do INSS, transformando informações brutas em insights estratégicos para a prevenção de riscos e tomada de decisão. 

O pipeline completo integra um processo robusto de Engenharia e Análise de Dados:
1. **Extração Automatizada (API):** Consumo direto do portal de dados abertos do governo via script Python, com resiliência para lidar com múltiplos formatos (.zip, .csv, .xlsx) em memória.
2. **Qualidade e Governança:** Limpeza, padronização (Regex) e geração automática de relatórios de *Data Quality*.
3. **Visualização Analítica:** Modelagem e criação de dashboard interativo no Power BI com DAX, explorando indicadores como volume de ocorrências, perfil das lesões e impacto em setores econômicos específicos (CNAE).

O resultado final é uma ferramenta focada em *data storytelling*, projetada para identificar padrões e direcionar ações de segurança do trabalho de forma assertiva.

## 🛠️ Tecnologias Utilizadas
* **Python (Pandas, Requests, OS):** Extração via API, tratamento em lote, validação de tipos e higienização.
* **Power BI:** Modelagem de dados, tratamento dinâmico via Power Query (Linguagem M) e criação de métricas (DAX).
* **Dados Abertos (INSS):** Fontes de dados públicas reais (recorte temporal 2024-2025).

## 📂 Estrutura de Arquivos

Abaixo está a organização dos diretórios para o funcionamento correto da automação e do dashboard:

/Case/

│

├── 📄 Case.pbit                        # Template dinâmico do Power BI (Dashboard para avaliação)

├── 📄 case_apresentacao.pptx           # Apresentação executiva dos resultados

├── 📄 padronizacao_cnae.py             # Script de limpeza da base CNAE

├── 📄 python coletar_acidentes.py      # Pipeline ETL de consumo da API do INSS

├── 📄 CNAE20_EstruturaDetalhada.xls    # Base bruta CNAE

├── 📄 CNAE20_Padronizado.xlsx          # Base limpa gerada pelo Python

├── 📄 design.png                  # Elementos visuais e backgrounds do dashboard

│

└── /resultados/

    ├── 📄 acidentes_trabalho_tratado.csv # Base de acidentes processada e consolidada
    
    └── 📄 relatorio_qualidade.csv        # Log automático de qualidade dos dados (Nulos, Tipos)

## 🚀 Como Executar o Projeto

Este projeto foi construído com uma **arquitetura de dados dinâmica**, garantindo que o dashboard funcione em qualquer computador local sem apresentar erros de diretório (*FileNotFound*).

### 1. Preparação do Ambiente e ETL (Opcional)
Os dados consolidados já se encontram na pasta `/resultados/`. Caso deseje testar os pipelines construídos do zero:

1. Certifique-se de ter o Python 3 instalado.
2. Instale as bibliotecas dependentes executando no terminal:
   ```bash
   pip install pandas requests xlrd openpyxl
Extração de Acidentes: Execute python coletar_acidentes.py. O script conectará à API do INSS, fará o download em memória dos recursos, tratará os dados e gerará o CSV final e o relatório de qualidade.

Padronização CNAE: Execute padronizacao_cnae.py para gerar a tabela de dimensão limpa a partir da estrutura detalhada.

2. Acessando o Dashboard Interativo
Para garantir a melhor experiência de avaliação, o arquivo do Power BI principal para envio foi salvo como um Modelo (.pbit).

Extraia a pasta completa deste projeto para o seu computador.

Copie o caminho absoluto da pasta raiz (Ex: C:\Usuarios\SeuNome\Downloads\Case).

Dê um duplo clique no arquivo Case.pbit.

Uma janela do Power BI será aberta imediatamente solicitando o caminho da pasta. Cole o caminho copiado e clique em Carregar.

O Power Query atualizará automaticamente as fontes de todas as consultas baseadas neste único parâmetro raiz.

📊 Principais Insights
Mitigação de Multas e Treinamento: O monitoramento do percentual de CATs emitidas com atraso revelou oportunidades críticas para a melhoria de processos internos e treinamento, mitigando diretamente o risco de passivos trabalhistas.

Direcionamento Estratégico de Recursos: O cruzamento de dados entre acidentes com afastamento, partes do corpo mais atingidas e os setores econômicos (CNAE) permite direcionar campanhas de prevenção e aquisição de EPIs de forma muito mais eficiente e menos generalista.

Visão Macro para Micro: A arquitetura do modelo permitiu construir uma visão estratégica que parte do panorama nacional e chega até a granularidade necessária para tomadas de decisões cirúrgicas e embasadas.

Desenvolvido por Gabriel Lima Silva.
