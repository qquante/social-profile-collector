"""
Configuração do Telegram Bot
"""

import os

# Token do Bot (obtido via @BotFather)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

# Chat ID para onde enviar mensagens
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Configurações opcionais
ENVIAR_APITO_LOCAL = True  # True = apita E envia telegram | False = só telegram
ENVIAR_PREVIEW_LINK = True  # True = mostra preview de links no Telegram
