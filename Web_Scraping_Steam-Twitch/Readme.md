# Web Scraping para análise de dados da Steam e Twitch
## Projeto obtendo dados das páginas web Stem.DB, TwitchMetric.net e efetuando análise.
> For studiyng
## Motivação
Otimizar um projeto antigo de análise de dados no qual os dados foram obtidos de forma manual e, gerar uma interface amigável de visualização. Motivação do projeto antigo: 
Analisar a relação entre categorias de streaming da Twitch e sua repercusão nos jogos mais acessados pela plataforma Steam; 

## Desafio e Etapas
Nessa aplicação o desafio foi desenvolver uma aplicação visual e semi-interativa em Python, além obter os dados por meio de um processo de automação

Bibliotecas: 
- NumPy (Manipulação dos dados)
- Pandas (Manipulação de planilhas)
- Tkinter (DashBoard)
- Selenium (Automação)

O projeto é estruturado em um conjunto de classes e arquivos que trabalham em conjunto para realizar análises e exibir gráficos relacionados a métricas da plataforma Steam e Twitch. 
Possuindo duas classes de suporte.
- Conexão:
Classe responsável por se conectar aos repectivos sites de métricas Steam e Twitch para obter os dados de métricas relevantes utiliando Selenium. 

- DashBoard:
A classe Dash é responsável por criar e abrir um dashboard (painel de controle) que irá exibir os gráficos e visualizações das análises realizadas. 
Ela utiliza a biblioteca Tkinter, interface gráfica de usuário (GUI) que permite interações com o usuário

Análises com NumPy e Pandas:
Após a obtenção dos dados, o projeto utiliza a biblioteca NumPy para realizar manipulações dos dados brutos. 
O Pandas é utilizado para a análise e tratamento desses dados em formato de tabelas.

Análise mais minuciosa no Jupyter Lab:
O projeto também inclui arquivos de análise mais detalhada usando o ambiente Jupyter Lab. 
Esses arquivos contêm explicações mais detalhadas e passo a passo da análise realizada, permitindo uma exploração mais profunda dos dados.

Projeto obtém dados de métricas da Steam e Twitch por meio da Classe de Conexão, 
realiza análises e manipulações desses dados com NumPy e Pandas, e exibe os resultados através de um dashboard, uma interface gráfica de usuário usando Tkinter. 
Além disso, fornece análises mais detalhadas através de um arquivo Markdown, 
que facilitam o entendimento e exploração dos dados.

![Alt Text](Web_Scraping_Steam-Twitch/library/prints/dash.png)
