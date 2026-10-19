"""
Monitor de posts novos do @lauki
Apita 8x com 888 Hz por 888 ms quando detectar post novo
E envia notificação para o Telegram
"""

import requests
import json
import time
import winsound
from datetime import datetime
import re
import os

# Importa Telegram Bot
try:
    from telegram_bot import TelegramBot
    from config_telegram import ENVIAR_APITO_LOCAL
    TELEGRAM_HABILITADO = True
except ImportError:
    TELEGRAM_HABILITADO = False
    ENVIAR_APITO_LOCAL = True
    print("⚠️  Telegram não configurado - usando apenas apitos")

class MoltXMonitor:
    def __init__(self, username="lauki", intervalo=30):
        self.username = username
        self.url = f"https://moltx.io/{username}"
        self.intervalo = intervalo  # segundos entre cada verificação
        self.ultimo_post_id = None
        self.arquivo_cache = "ultimo_post.json"
        self.telegram_bot = TelegramBot() if TELEGRAM_HABILITADO else None
        self.carregar_ultimo_post()
        
    def carregar_ultimo_post(self):
        """Carrega o ID do último post visto"""
        try:
            if os.path.exists(self.arquivo_cache):
                with open(self.arquivo_cache, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.ultimo_post_id = data.get('ultimo_post_id')
                    print(f"[CACHE] Último post conhecido: {self.ultimo_post_id}")
        except:
            pass
    
    def salvar_ultimo_post(self, post_id):
        """Salva o ID do último post visto"""
        self.ultimo_post_id = post_id
        try:
            with open(self.arquivo_cache, 'w', encoding='utf-8') as f:
                json.dump({
                    'ultimo_post_id': post_id,
                    'timestamp': datetime.now().isoformat()
                }, f)
        except:
            pass
    
    def buscar_posts(self):
        """Busca posts do usuário com retry"""
        tentativas = 3
        
        for tentativa in range(1, tentativas + 1):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                }
                
                # Timeout maior: 30 segundos
                response = requests.get(self.url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    return self.extrair_posts(response.text)
                else:
                    print(f"[ERRO] Status {response.status_code}", end="")
                    if tentativa < tentativas:
                        print(f" - Tentando novamente ({tentativa}/{tentativas})...")
                        time.sleep(2)
                    else:
                        print()
                    
            except requests.exceptions.Timeout:
                print(f"[TIMEOUT]", end="")
                if tentativa < tentativas:
                    print(f" Tentativa {tentativa}/{tentativas} - Aguarde...")
                    time.sleep(3)
                else:
                    print(f" Falhou após {tentativas} tentativas")
                    
            except requests.exceptions.ConnectionError:
                print(f"[SEM CONEXÃO]", end="")
                if tentativa < tentativas:
                    print(f" Tentando novamente ({tentativa}/{tentativas})...")
                    time.sleep(5)
                else:
                    print(f" Sem internet?")
                    
            except Exception as e:
                erro_msg = str(e)
                # Simplifica mensagem de erro
                if "Read timed out" in erro_msg:
                    print(f"[TIMEOUT] Site muito lento", end="")
                elif "Connection" in erro_msg:
                    print(f"[CONEXÃO] Erro de rede", end="")
                else:
                    print(f"[ERRO] {erro_msg[:50]}", end="")
                
                if tentativa < tentativas:
                    print(f" - Retry {tentativa}/{tentativas}...")
                    time.sleep(2)
                else:
                    print()
        
        return []
    
    def extrair_posts(self, html):
        """Extrai posts básicos do HTML"""
        posts = []
        pattern = r'<article class="post" data-post-href="(/post/([^"]+))">(.*?)</article>'
        matches = re.finditer(pattern, html, re.DOTALL)
        
        for match in matches:
            post_url = match.group(1)
            post_id = match.group(2)
            post_html = match.group(3)
            
            # Extrai conteúdo - tenta múltiplos métodos
            conteudo = ""
            
            # Método 1: content-full
            content_match = re.search(r'<div class="content content-full">(.*?)</div>', post_html, re.DOTALL)
            if content_match:
                conteudo = content_match.group(1)
            
            # Método 2: content sem full
            if not conteudo:
                content_match = re.search(r'<div class="content"[^>]*>(.*?)</div>', post_html, re.DOTALL)
                if content_match:
                    conteudo = content_match.group(1)
            
            # Método 3: content-preview
            if not conteudo:
                content_match = re.search(r'<div class="content content-preview">(.*?)</div>', post_html, re.DOTALL)
                if content_match:
                    conteudo = content_match.group(1)
            
            # Limpa HTML do conteúdo
            if conteudo:
                # Preserva quebras de linha
                conteudo = re.sub(r'<br\s*/?>', '\n', conteudo)
                # Remove outras tags mas mantém o texto
                conteudo = re.sub(r'<a[^>]*>', '', conteudo)
                conteudo = re.sub(r'</a>', '', conteudo)
                conteudo = re.sub(r'<[^>]+>', '', conteudo)
                # Decodifica HTML entities
                conteudo = re.sub(r'&#039;', "'", conteudo)
                conteudo = re.sub(r'&quot;', '"', conteudo)
                conteudo = re.sub(r'&lt;', '<', conteudo)
                conteudo = re.sub(r'&gt;', '>', conteudo)
                conteudo = re.sub(r'&amp;', '&', conteudo)
                # Limpa espaços extras mas preserva quebras de linha
                conteudo = '\n'.join(line.strip() for line in conteudo.split('\n') if line.strip())
            
            # Extrai tempo
            tempo_match = re.search(r'<span class="timestamp"[^>]*>(.*?)</span>', post_html)
            tempo = tempo_match.group(1) if tempo_match else "agora"
            
            # Se não conseguiu pegar conteúdo, tenta pegar pelo menos algum texto
            if not conteudo:
                # Procura qualquer texto dentro do post
                texto_bruto = re.sub(r'<[^>]+>', ' ', post_html)
                texto_bruto = re.sub(r'\s+', ' ', texto_bruto).strip()
                # Pega os primeiros 200 caracteres
                if len(texto_bruto) > 50:
                    conteudo = texto_bruto[:200] + "..."
            
            posts.append({
                'id': post_id,
                'url': f'https://moltx.io{post_url}',
                'conteudo': conteudo if conteudo else "[Conteúdo não extraído - verifique a URL]",
                'tempo': tempo
            })
        
        return posts
    
    def alertar_post_novo(self, post):
        """Apita 8x com 888 Hz por 888 ms E envia para Telegram"""
        print("\n" + "="*70)
        print("🚨🚨🚨 POST NOVO DETECTADO! 🚨🚨🚨")
        print("="*70)
        print(f"\n📝 ID: {post['id']}")
        print(f"⏰ Tempo: {post['tempo']}")
        print(f"🔗 URL: {post['url']}")
        print(f"\n📄 CONTEÚDO:")
        print("-" * 70)
        
        # Mostra conteúdo completo (máximo 500 caracteres)
        conteudo = post['conteudo']
        if len(conteudo) > 500:
            print(conteudo[:500])
            print(f"\n... (conteúdo truncado, {len(conteudo)} caracteres no total)")
        else:
            print(conteudo)
        
        print("-" * 70)
        
        # Envia para Telegram
        if self.telegram_bot:
            print("\n📱 Enviando para Telegram...", end=" ", flush=True)
            try:
                mensagem = self.telegram_bot.formatar_post_novo(post)
                sucesso, resultado = self.telegram_bot.enviar_mensagem(mensagem)
                
                if sucesso:
                    print("✅ Enviado!")
                else:
                    print(f"❌ Erro: {resultado}")
            except Exception as e:
                print(f"❌ Exceção: {str(e)}")
        
        # Apita (se habilitado)
        if ENVIAR_APITO_LOCAL:
            print("\n" + "="*70)
            print("🔊🔊🔊 APITANDO 8x (888 Hz por 888 ms cada) 🔊🔊🔊")
            print("="*70 + "\n")
            
            # Apita 8x
            for i in range(1):
                print(f"🔊 Apito {i+1}/8...", end=" ", flush=True)
                try:
                    winsound.Beep(888, 888)  # 888 Hz por 888 ms
                    print("✓")
                except Exception as e:
                    print(f"✗")
                time.sleep(0.1)  # Pequena pausa entre apitos
        
        print("\n" + "="*70)
        print("✅ ALERTA COMPLETO!")
        print("="*70 + "\n")
    
    def verificar(self):
        """Verifica se há posts novos"""
        posts = self.buscar_posts()
        
        if not posts:
            print(" ⚠️  Não conseguiu buscar posts")
            return False
        
        # Pega o post mais recente
        post_mais_recente = posts[0]
        
        # Se é a primeira execução, só salva
        if self.ultimo_post_id is None:
            print(f" ✓ Primeiro post: {post_mais_recente['id'][:8]}...")
            print(f"    Preview: {post_mais_recente['conteudo'][:50]}...")
            self.salvar_ultimo_post(post_mais_recente['id'])
            return False
        
        # Verifica se é um post novo
        if post_mais_recente['id'] != self.ultimo_post_id:
            self.alertar_post_novo(post_mais_recente)
            self.salvar_ultimo_post(post_mais_recente['id'])
            return True
        
        return False
    
    def rodar(self):
        """Loop principal do monitor"""
        print("="*60)
        print("🎯 MOLTX MONITOR - @lauki")
        print("="*60)
        print(f"\nMonitorando: https://moltx.io/{self.username}")
        print(f"Intervalo: {self.intervalo} segundos")
        
        # Mostra status do Telegram
        if self.telegram_bot:
            print(f"📱 Telegram: ✅ HABILITADO")
            # Testa bot
            sucesso, msg = self.telegram_bot.testar_bot()
            if sucesso:
                print(f"   Bot: {msg}")
            else:
                print(f"   ⚠️  Erro no bot: {msg}")
        else:
            print(f"📱 Telegram: ❌ DESABILITADO")
        
        if ENVIAR_APITO_LOCAL:
            print(f"🔊 Apito local: ✅ HABILITADO")
        else:
            print(f"🔊 Apito local: ❌ DESABILITADO")
        
        print("\nPressione Ctrl+C para parar\n")
        print("="*60)
        
        contador = 0
        
        try:
            while True:
                contador += 1
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"\n[{timestamp}] Verificação #{contador}...")
                
                tem_novo = self.verificar()
                
                if tem_novo:
                    print("🎉 POST NOVO DETECTADO!")
                else:
                    print("✓ Tudo verificado - sem posts novos")
                
                # Aguarda próxima verificação com countdown
                print(f"\n⏳ Aguardando {self.intervalo}s até próxima verificação...", flush=True)
                time.sleep(self.intervalo)
                
        except KeyboardInterrupt:
            print("\n\n" + "="*60)
            print("🛑 Monitor parado pelo usuário")
            print("="*60)
            print(f"\nTotal de verificações: {contador}")
            print(f"Último post conhecido: {self.ultimo_post_id}")
            print()

def main():
    # Configuração
    USUARIO = "lauki"
    INTERVALO = 30  # segundos (30s = verificar a cada 30 segundos)
    
    # Mostra menu de configuração
    print("="*60)
    print("CONFIGURAÇÃO DO MONITOR")
    print("="*60)
    print(f"\nUsuário: @{USUARIO}")
    print(f"Intervalo padrão: {INTERVALO} segundos")
    print("\nDeseja mudar o intervalo? (Enter para manter padrão)")
    
    try:
        resposta = input("Digite o intervalo em segundos (ou Enter): ").strip()
        if resposta:
            INTERVALO = int(resposta)
            print(f"✓ Intervalo alterado para {INTERVALO} segundos")
    except:
        print("✓ Usando intervalo padrão")
    
    print()
    
    # Inicia monitor
    monitor = MoltXMonitor(USUARIO, INTERVALO)
    monitor.rodar()

if __name__ == "__main__":
    main()
