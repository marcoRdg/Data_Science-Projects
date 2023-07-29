import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

class Scraper:
    # Contrutor da classe
    def __init__(self):

        # esconder navegador
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--headless')
        self.navegador = webdriver.Firefox(options=firefox_options)#options=firefox_options

    def get_dados_steam(self):
        # pagina inicial
        self.navegador.get('https://steamdb.info/charts/')

        jogos_list = []

        # Recebe o Obj com todos os jogos da pagina
        jogos = self.navegador.find_elements(By.XPATH, '//tr[@class="app"]')

        # Percorre cada jogo e atribui os dados a lista de jogos
        for jogo in jogos:
            elementos = jogo.find_elements(By.XPATH, './/td')[2:6]
            dados_jogo = [elemento.text for elemento in elementos]
            jogos_list.append(dados_jogo)

        # Denomina as coluna para cada item do vetor de votores
        colunas = ['Jogo', 'jogadores_at_moment', '24h_peek', 'all-time_peak']
        df_steam = pd.DataFrame(jogos_list, columns=colunas)
        
        # retira as virgulas 
        df_steam.iloc[:, 1:] = df_steam.iloc[:, 1:].apply(lambda x: pd.to_numeric(x.str.replace(',', '')))
        # retorna a tabela com os dados
        return df_steam

    def get_dados_twitch(self):

        # Denota a pagina inicial de busca
        url = 'https://www.twitchmetrics.net/games/viewership'

        # Adquiri os dados de nome e estatus da pagina
        def get_dados(url, navegador):

            navegador.get(url)

            jogos = navegador.find_elements(By.XPATH, '//h5[@class="mr-2 mb-0"]')
            name_jogos = [jogo.text for jogo in jogos]

            stats = navegador.find_elements(By.XPATH, '//samp')
            status = [stat.text for stat in stats]

            # retorna um dicionario com chave o nome do jogo e statistica como valores
            return {name: [val] for name, val in zip(name_jogos, status)}


        # Dicionário auxiliar para os elementos name e statistica
        dicionario = get_dados(url,self.navegador)

        # URLS dos status
        urls_jogos = [
            'https://www.twitchmetrics.net/games/played',
            'https://www.twitchmetrics.net/games/peak',
            'https://www.twitchmetrics.net/games/popularity'
        ]

        # Itera pelas URLs
        for i in range(0,3):
            name_auxiliar = []
            url_jogo = urls_jogos[i]
            # Obtem as estatísticas do jogo da URL atual
            dicionario_temp = get_dados(url_jogo, self.navegador)
            #print(dicionario_temp)
            # Atualiza o dicionário principal com as novas estatísticas
            for name, valor in dicionario_temp.items():
                if name in dicionario:
                    dicionario[name].extend(dicionario_temp[name])
                else:
                    dicionario[name] = [None]*(i+1)
                    dicionario[name].extend(dicionario_temp[name])
                name_auxiliar.append(name)

            # Testa quais chaves não estão presentes no vetor x
            chaves_nao_presentes = {chave: valor for chave, valor in dicionario.items() if chave not in name_auxiliar}
            for chave in chaves_nao_presentes:
                dicionario[chave].extend([None])




        # Criar o DataFrame a partir do dicionário
        df = pd.DataFrame.from_dict(dicionario, orient='index',
                                    columns=['Viewer Hours', 'Avg Live Channels', 'Peak Viewers', 'Avg Viewers'])

        # Reseta o índice e o torna uma coluna
        df.reset_index(inplace=True)

        # Renomeia as colunas para adicionar o nome "jogo" à coluna das chaves do dicionário
        df.columns = ['Jogo', 'Viewer Hours', 'Avg Live Channels', 'Peak Viewers', 'Avg Viewers']

        df.iloc[:, 1:] = df.iloc[:, 1:5].apply(lambda x: pd.to_numeric(x.str.replace(',', '')))
        return df


    def fechar_navegador(self):
        self.navegador.quit()








