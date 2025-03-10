import os
from bot import bot  # Importa o bot do arquivo bot.py

TOKEN = os.getenv('TOKEN')

if __name__ == "__main__":
    bot.run(TOKEN)  # Inicia o bot com o token gravado no .env