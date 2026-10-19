"""
Funções para enviar mensagens para o Telegram
"""

import requests
import re
from config_telegram import BOT_TOKEN, CHAT_ID, ENVIAR_PREVIEW_LINK

class TelegramBot:
    def __init__(self):
        self.token = BOT_TOKEN
        self.chat_id = CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.token}"
    
    def enviar_mensagem(self, texto, parse_mode="Markdown"):
        """Envia mensagem para o Telegram"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': texto,
                'parse_mode': parse_mode,
                'disable_web_page_preview': not ENVIAR_PREVIEW_LINK
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                return True, "Enviado!"
            else:
                return False, f"Erro {response.status_code}: {response.text[:100]}"
                
        except Exception as e:
            return False, f"Exceção: {str(e)}"
    
    def detectar_contract_addresses(self, texto):
        """Detecta endereços de contratos (0x...) no texto"""
        # Padrão: 0x seguido de 40 caracteres hexadecimais
        pattern = r'0x[a-fA-F0-9]{40}'
        matches = re.findall(pattern, texto)
        
        # Remove duplicatas mantendo ordem
        seen = set()
        unique_addresses = []
        for addr in matches:
            addr_lower = addr.lower()
            if addr_lower not in seen:
                seen.add(addr_lower)
                unique_addresses.append(addr)
        
        return unique_addresses
    
    def formatar_post_novo(self, post):
        """Formata post para enviar no Telegram"""
        
        # Cabeçalho
        msg = "🚨 *NOVO POST \\- @lauki*\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        # Conteúdo do post
        msg += "📄 *CONTEÚDO:*\n\n"
        
        # Escapa caracteres especiais do Markdown do Telegram
        conteudo = post.get('conteudo', '[Sem conteúdo]')
        conteudo_escaped = self.escapar_markdown(conteudo)
        
        msg += f"{conteudo_escaped}\n\n"
        
        # Detecta Contract Addresses
        addresses = self.detectar_contract_addresses(conteudo)
        
        if addresses:
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            msg += "🔗 *CONTRACT ADDRESS DETECTADO:*\n\n"
            
            for i, addr in enumerate(addresses, 1):
                # Mostra endereço
                if len(addresses) > 1:
                    msg += f"*\\#{i}*\n"
                
                msg += f"📍 `{addr}`\n\n"
                
                # Links
                msg += "🔍 *Ver no BaseScan:*\n"
                msg += f"→ [https://basescan\\.org/address/{addr}](https://basescan.org/address/{addr})\n\n"
                
                msg += "📈 *Ver no DEXScreener:*\n"
                msg += f"→ [https://dexscreener\\.com/base/{addr}](https://dexscreener.com/base/{addr})\n\n"
        
        # Rodapé
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        # Tempo
        tempo = post.get('tempo', 'agora')
        msg += f"⏰ *Postado há:* {self.escapar_markdown(tempo)}\n"
        
        # Link do post
        url_post = post.get('url', '')
        if url_post:
            msg += f"🔗 *Ver post:* [MoltX]({url_post})\n"
        
        return msg
    
    def escapar_markdown(self, texto):
        """Escapa caracteres especiais do Markdown do Telegram"""
        # Caracteres que precisam ser escapados no MarkdownV2
        caracteres_especiais = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        for char in caracteres_especiais:
            texto = texto.replace(char, f'\\{char}')
        
        return texto
    
    def testar_bot(self):
        """Testa se o bot está funcionando"""
        try:
            # Testa com getMe
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data.get('result', {})
                    return True, f"Bot OK: @{bot_info.get('username', 'unknown')}"
            
            return False, f"Erro: {response.text[:100]}"
            
        except Exception as e:
            return False, f"Exceção: {str(e)}"
    
    def testar_chat(self):
        """Testa se consegue enviar mensagem para o chat"""
        msg = "✅ *Teste de Conexão*\n\nBot conectado com sucesso\\!"
        return self.enviar_mensagem(msg)

if __name__ == "__main__":
    # Teste rápido
    bot = TelegramBot()
    
    print("Testando bot...")
    sucesso, msg = bot.testar_bot()
    print(f"  {'✓' if sucesso else '✗'} {msg}")
    
    print("\nTestando envio...")
    sucesso, msg = bot.testar_chat()
    print(f"  {'✓' if sucesso else '✗'} {msg}")
