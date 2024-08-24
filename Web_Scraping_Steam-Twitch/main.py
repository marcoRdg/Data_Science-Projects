"""
#DashBoard com Tkinter
from library.dashboard_Tkinter import Dashboard

dashboard = Dashboard()
dashboard.mainloop()"""


# DashBoard com Streamlit

import os
import subprocess


def run_streamlit_app(script_name):
    try:
        # Comando para rodar o streamlit
        command = f"streamlit run {script_name}"

        # Abre o streamlit no navegador padrão
        subprocess.run(command, shell=True)

    except Exception as e:
        print(f"Erro ao tentar abrir o Streamlit: {e}")


if __name__ == "__main__":
    # Caminho do arquivo do dashboard dentro da pasta 'library'
    script_name = "library/dashboard_Streamlit.py"

    # Chama a função para abrir o Streamlit
    run_streamlit_app(script_name)
