import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from library.conexao import Scraper

class Dashboard(tk.Tk):
    def __init__(self):  # Cconstrutor
        super().__init__()
        self.title("Dashboard")
        self.state('zoomed')
        self.create_widgets()
        self.update_graficos()

    def create_widgets(self):  # Define o layout e elementos da pagina

        # Define a paleta de cores
        self.cores = ["#8179AF","#38A3A5","#255056","#2F4858","#A3586D"]
        plt.rcParams["axes.prop_cycle"] = plt.cycler(color=self.cores)

        # Criando Frames
        # Grame lateral esquerda //menu
        side_frame = tk.Frame(self, bg="#4C2A85")
        side_frame.pack(side="left", fill="y")

        # Frame lateral direta para graficos
        frame_graficos = tk.Frame(self)
        frame_graficos.pack()

        # frame para graficos superior
        upper_frame = tk.Frame(frame_graficos)
        upper_frame.pack(fill="both", expand=True)

        # frame para graficos inferio
        lower_frame = tk.Frame(frame_graficos)
        lower_frame.pack(fill="both", expand=True)

        # Criação dos figuras (atributos da classe)
        self.fig1, self.ax1 = plt.subplots(figsize=(10, 5))
        self.fig2, self.ax2 = plt.subplots()
        self.fig3, self.ax3 = plt.subplots()
        self.fig4, self.ax4 = plt.subplots()

        # quadro 1
        self.canvas1 = FigureCanvasTkAgg(self.fig1, upper_frame)
        self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

        # quadro 2
        self.canvas2 = FigureCanvasTkAgg(self.fig2, upper_frame)
        self.canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

        # quadro 3
        self.canvas3 = FigureCanvasTkAgg(self.fig3, lower_frame)
        self.canvas3.get_tk_widget().pack(side="left", fill="both", expand=True)

        #quadro 4
        self.canvas4 = FigureCanvasTkAgg(self.fig4, lower_frame)
        self.canvas4.get_tk_widget().pack(side="left", fill="both", expand=True)

        # Label menu
        label = tk.Label(side_frame, text="Dashboard", bg="#4C2A85", fg="#FFF", font=25)
        label.pack(pady=50, padx=20)

        # Botão para atualizar o canvas
        button = tk.Button(side_frame, text="Atualizar Dados", command=self.update_graficos)
        button.pack(fill=tk.X)

    def update_graficos(self):

        obj = Scraper()

        # Obtendo dados Twitch e Steam
        df_steam = obj.get_dados_steam()
        df_twitch = obj.get_dados_twitch()
        obj.fechar_navegador()

        # DF da união das duas tabelas
        df_merge = df_twitch.merge(df_steam, on='Jogo', how='inner')
        x = df_merge['jogadores_at_moment']
        y = df_merge['Viewer Hours']

        # Atualizacao dos graficos
        # Barras
        df = df_steam.sort_values(by="jogadores_at_moment", ascending=False)
        self.ax1.clear()
        self.ax1.bar(df['Jogo'].head(5), df['jogadores_at_moment'].head(5), color=self.cores)
        self.ax1.set_title("Jogadores no momento - Steam (Descrescente)")
        self.ax1.set_xlabel("Product")
        self.ax1.set_ylabel("Sales")

        # barras horizontais
        self.ax2.clear()
        self.ax2.barh(df_twitch['Jogo'].head(5), df_twitch['Viewer Hours'].head(5), color=self.cores)
        self.ax2.set_title("Categorias mais assistidas - Twitch")
        self.ax2.set_xlabel("Viewer/h")
        self.ax2.set_ylabel("Categoria")
        self.canvas2.draw()

        # pizza
        self.ax3.clear()
        self.ax3.pie(df_steam['all-time_peak'].head(5), labels=df_steam['Jogo'].head(5), autopct='%1.1f%%')
        self.ax3.set_title("Game \n all time peak \n Steam")
        self.canvas3.draw()

        # Pontos
        self.ax4.clear()
        self.ax4.plot(x.astype(float), y.astype(float), '.')
        self.ax4.set_title("Mais jogados por Mais assistidos")
        self.ax4.set_xlabel("Jogadores no Momento")
        self.ax4.set_ylabel("Views per Hours")
        self.canvas4.draw()

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
