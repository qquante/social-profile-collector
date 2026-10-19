"""
Monitor On-Chain em Tempo Real via WebSocket
Detecta compras de tokens do contrato
"""

import json
import time
import winsound
from datetime import datetime
import websocket
import threading

from config_rpc import ANKR_RPC_WSS, CONTRATO
from token_info import TokenInfo
from telegram_bot_onchain import TelegramBotOnchain
from config_telegram import ENVIAR_APITO_LOCAL

# USDC na Base
USDC_ADDRESS = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"

# Transfer event signature
TRANSFER_SIGNATURE = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

class MonitorOnchainWSS:
    def __init__(self):
        self.wss_url = ANKR_RPC_WSS
        self.contrato = CONTRATO.lower()
        self.usdc = USDC_ADDRESS.lower()
        
        self.ws = None
        self.subscription_id = None
        self.is_running = False
        
        self.token_info = TokenInfo()
        self.telegram = TelegramBotOnchain()
        
        # Para rastrear compras em andamento
        self.pending_buys = {}  # tx_hash -> info
        
        print(f"[WSS] URL: {self.wss_url[:50]}...")
        print(f"[CONTRATO] {self.contrato}")
        print(f"[USDC] {self.usdc}")
    
    def on_message(self, ws, message):
        """Processa mensagens do WebSocket"""
        try:
            data = json.loads(message)
            
            # Se é resposta da subscrição
            if 'result' in data and self.subscription_id is None:
                self.subscription_id = data['result']
                print(f"[WSS] ✅ Inscrito! Subscription ID: {self.subscription_id}")
                print(f"[WSS] 🎧 Escutando Transfer events em tempo real...")
                return
            
            # Se é um log de evento
            if 'params' in data and 'result' in data['params']:
                log = data['params']['result']
                self.processar_log(log)
                
        except Exception as e:
            print(f"[ERRO] Processando mensagem: {str(e)}")
    
    def processar_log(self, log):
        """Processa um log de Transfer event"""
        try:
            topics = log.get('topics', [])
            
            if len(topics) < 3:
                return
            
            # Extrai informações
            token_address = log.get('address', '').lower()
            from_addr = '0x' + topics[1][-40:].lower()
            to_addr = '0x' + topics[2][-40:].lower()
            
            data_hex = log.get('data', '0x0')
            try:
                value = int(data_hex, 16)
            except:
                value = 0
            
            tx_hash = log.get('transactionHash', '')
            
            # Verifica se envolve o contrato
            if from_addr != self.contrato and to_addr != self.contrato:
                return
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            # CASO 1: Contrato enviou USDC (possível início de compra)
            if token_address == self.usdc and from_addr == self.contrato:
                usdc_amount = value / 1e6  # USDC tem 6 decimais
                
                print(f"\n[{timestamp}] 📤 Contrato enviou {usdc_amount:.2f} USDC")
                print(f"            TX: {tx_hash[:16]}...")
                
                # Marca como compra pendente
                self.pending_buys[tx_hash] = {
                    'usdc_amount': usdc_amount,
                    'timestamp': timestamp
                }
            
            # CASO 2: Contrato recebeu token (compra confirmada!)
            elif token_address != self.usdc and to_addr == self.contrato:
                print(f"\n[{timestamp}] 📥 Contrato recebeu token: {token_address[:10]}...")
                print(f"            TX: {tx_hash[:16]}...")
                
                # Verifica se há compra pendente para esta TX
                usdc_amount = 100  # Default
                if tx_hash in self.pending_buys:
                    usdc_amount = self.pending_buys[tx_hash]['usdc_amount']
                    del self.pending_buys[tx_hash]
                
                # COMPRA DETECTADA!
                self.alertar_compra(
                    token_address=token_address,
                    token_amount_raw=value,
                    usdc_amount=usdc_amount,
                    tx_hash=tx_hash
                )
                
        except Exception as e:
            print(f"[ERRO] Processando log: {str(e)}")
    
    def alertar_compra(self, token_address, token_amount_raw, usdc_amount, tx_hash):
        """Alerta quando detecta compra"""
        print("\n" + "="*70)
        print("🚨🚨🚨 NOVA COMPRA DETECTADA! 🚨🚨🚨")
        print("="*70)
        
        # Busca info do token
        print(f"\n[1/3] Buscando informações do token...")
        token_info = self.token_info.get_token_info(token_address)
        
        # Formata quantidade
        token_amount_formatted = self.token_info.format_amount(
            token_amount_raw,
            token_info['decimals']
        )
        
        # Mostra no terminal
        print(f"\n💰 TOKEN COMPRADO:")
        print(f"   Nome: {token_info['name']}")
        print(f"   Símbolo: ${token_info['symbol']}")
        print(f"   CA: {token_address}")
        
        print(f"\n💵 PAGAMENTO:")
        print(f"   {usdc_amount:.2f} USDC")
        
        print(f"\n📊 RECEBEU:")
        print(f"   {token_amount_formatted}")
        
        print(f"\n🔗 TX Hash:")
        print(f"   {tx_hash}")
        
        print(f"\n🔗 Links:")
        print(f"   BaseScan: https://basescan.org/token/{token_address}")
        print(f"   DEXScreener: https://dexscreener.com/base/{token_address}")
        
        # Envia para Telegram
        print(f"\n[2/3] Enviando para Telegram...")
        try:
            sucesso, msg = self.telegram.enviar_alerta_compra(
                token_info=token_info,
                usdc_amount=f"{usdc_amount:.2f}",
                token_amount=token_amount_formatted
            )
            
            if sucesso:
                print(f"      ✅ Enviado!")
            else:
                print(f"      ❌ Erro: {msg}")
        except Exception as e:
            print(f"      ❌ Exceção: {str(e)}")
        
        # Apita
        if ENVIAR_APITO_LOCAL:
            print(f"\n[3/3] Apitando...")
            for i in range(8):
                print(f"      🔊 Apito {i+1}/8...", end=" ", flush=True)
                try:
                    winsound.Beep(888, 888)
                    print("✓")
                except:
                    print("✗")
                time.sleep(0.1)
        
        print("\n" + "="*70)
        print("✅ ALERTA COMPLETO!")
        print("="*70 + "\n")
        
        # Salva no histórico
        self.salvar_historico({
            'timestamp': datetime.now().isoformat(),
            'token_address': token_address,
            'token_name': token_info['name'],
            'token_symbol': token_info['symbol'],
            'usdc_amount': usdc_amount,
            'token_amount': token_amount_formatted,
            'tx_hash': tx_hash
        })
    
    def salvar_historico(self, compra):
        """Salva compra no histórico"""
        try:
            import os
            historico_file = "historico_compras_onchain.json"
            historico = []
            
            if os.path.exists(historico_file):
                with open(historico_file, 'r', encoding='utf-8') as f:
                    historico = json.load(f)
            
            historico.append(compra)
            
            with open(historico_file, 'w', encoding='utf-8') as f:
                json.dump(historico, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"[ERRO] Salvando histórico: {str(e)}")
    
    def on_error(self, ws, error):
        """Handler de erro"""
        print(f"\n[WSS ERRO] {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Handler de fechamento"""
        print(f"\n[WSS] Conexão fechada")
        self.is_running = False
    
    def on_open(self, ws):
        """Handler de abertura"""
        print(f"[WSS] ✅ Conectado!")
        
        # Inscreve nos Transfer events do contrato
        subscribe_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_subscribe",
            "params": [
                "logs",
                {
                    "address": self.contrato,
                    "topics": [TRANSFER_SIGNATURE]
                }
            ]
        }
        
        ws.send(json.dumps(subscribe_msg))
        print(f"[WSS] 📡 Solicitando inscrição...")
    
    def rodar(self):
        """Inicia o monitor"""
        print("="*70)
        print("🔗 MONITOR ON-CHAIN TEMPO REAL - BASE NETWORK")
        print("="*70)
        print(f"\nContrato: {self.contrato}")
        print(f"WebSocket: Ankr Base")
        print(f"Detectando: Compras de tokens (USDC → Token)")
        print(f"\nAlertas:")
        print(f"  🔊 Apito: {'✅' if ENVIAR_APITO_LOCAL else '❌'}")
        print(f"  📱 Telegram: ✅")
        print(f"\nPressione Ctrl+C para parar\n")
        print("="*70)
        
        self.is_running = True
        
        # Configura WebSocket
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            self.wss_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        
        # Roda em thread separada
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()
        
        try:
            # Mantém rodando
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("🛑 Monitor parado pelo usuário")
            print("="*70)
            self.ws.close()

def main():
    monitor = MonitorOnchainWSS()
    monitor.rodar()

if __name__ == "__main__":
    main()
