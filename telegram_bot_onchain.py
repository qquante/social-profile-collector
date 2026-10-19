"""
Bot Telegram específico para alertas on-chain
Com botões inline
"""

import requests
from config_telegram import BOT_TOKEN, CHAT_ID

class TelegramBotOnchain:
    def __init__(self):
        self.token = BOT_TOKEN
        self.chat_id = CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.token}"
    
    def enviar_alerta_compra(self, token_info, usdc_amount, token_amount):
        """
        Envia alerta de compra com botões inline
        
        token_info = {
            'address': '0x...',
            'name': 'Based Pepe',
            'symbol': 'BPEPE',
            'decimals': 18
        }
        """
        ca = token_info['address']
        nome = token_info['name']
        symbol = token_info['symbol']
        
        # Monta mensagem
        msg = "🚨 *NOVA COMPRA CONTRACT MOLTX*\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # CA (em código para fácil copiar)
        msg += f"📍 *CA:*\n"
        msg += f"`{ca}`\n\n"
        
        # Token info
        msg += f"🏷️ *TOKEN:*\n"
        msg += f"{nome} \\(${symbol}\\)\n\n"
        
        # Pagamento
        msg += f"💰 *PAGAMENTO:*\n"
        msg += f"{usdc_amount} USDC\n\n"
        
        # Recebeu
        msg += f"📊 *RECEBEU:*\n"
        msg += f"{token_amount}\n\n"
        
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Botões inline
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Sigma", "url": f"https://t.me/SigmaTrading9_bot?start=xqquante-{ca}"},
                    {"text": "GMGN", "url": f"https://gmgn.ai/base/token/qquante_{ca}"}
                ],
                [
                    {"text": "VIP", "url": f"https://t.me/SigmaTradingVIP_bot?start=xqquante-{ca}"},
                    {"text": "Clanker", "url": f"https://www.clanker.world/clanker/{ca}"}
                ]
            ]
        }
        
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': msg,
                'parse_mode': 'MarkdownV2',
                'reply_markup': keyboard,
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                return True, "Enviado!"
            else:
                return False, f"Erro {response.status_code}"
                
        except Exception as e:
            return False, f"Exceção: {str(e)}"
