import os
from dotenv import load_dotenv
from bot import bot  # Importa o bot do arquivo bot.py

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

TOKEN = os.getenv('TOKEN')

if __name__ == "__main__":
    bot.run(TOKEN)  # Inicia o bot com o token gravado no .env