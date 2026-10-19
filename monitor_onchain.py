"""
Monitor On-Chain - Base Network
Monitora um contrato e alerta quando ele compra tokens novos
"""

import requests
import json
import time
import winsound
from datetime import datetime
import os

class BaseChainMonitor:
    def __init__(self, contrato, intervalo=30):
        self.contrato = contrato.lower()
        self.intervalo = intervalo
        self.basescan_api = "https://api.basescan.org/api"
        self.ultimo_tx_hash = None
        self.tokens_conhecidos = set()
        self.arquivo_cache = "onchain_cache.json"
        self.carregar_cache()
        
    def carregar_cache(self):
        """Carrega dados salvos"""
        try:
            if os.path.exists(self.arquivo_cache):
                with open(self.arquivo_cache, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.ultimo_tx_hash = data.get('ultimo_tx_hash')
                    self.tokens_conhecidos = set(data.get('tokens_conhecidos', []))
                    print(f"[CACHE] Última TX: {self.ultimo_tx_hash}")
                    print(f"[CACHE] {len(self.tokens_conhecidos)} tokens conhecidos")
        except:
            pass
    
    def salvar_cache(self):
        """Salva dados"""
        try:
            with open(self.arquivo_cache, 'w', encoding='utf-8') as f:
                json.dump({
                    'ultimo_tx_hash': self.ultimo_tx_hash,
                    'tokens_conhecidos': list(self.tokens_conhecidos),
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
        except:
            pass
    
    def buscar_transacoes(self):
        """Busca transações do contrato"""
        try:
            # Busca últimas transações normais
            params = {
                'module': 'account',
                'action': 'txlist',
                'address': self.contrato,
                'startblock': 0,
                'endblock': 99999999,
                'page': 1,
                'offset': 10,
                'sort': 'desc'
            }
            
            response = requests.get(self.basescan_api, params=params, timeout=30)
            data = response.json()
            
            if data.get('status') == '1':
                return data.get('result', [])
            else:
                print(f" ⚠️  API retornou: {data.get('message', 'erro')}")
                return []
                
        except Exception as e:
            print(f" ⚠️  Erro ao buscar TXs: {str(e)[:50]}")
            return []
    
    def buscar_token_transfers(self):
        """Busca transfers de tokens ERC-20"""
        try:
            params = {
                'module': 'account',
                'action': 'tokentx',
                'address': self.contrato,
                'startblock': 0,
                'endblock': 99999999,
                'page': 1,
                'offset': 10,
                'sort': 'desc'
            }
            
            response = requests.get(self.basescan_api, params=params, timeout=30)
            data = response.json()
            
            if data.get('status') == '1':
                return data.get('result', [])
            else:
                return []
                
        except Exception as e:
            print(f" ⚠️  Erro ao buscar tokens: {str(e)[:50]}")
            return []
    
    def analisar_token_transfer(self, transfer):
        """Analisa se é uma compra de token"""
        # Se o contrato recebeu tokens (to == contrato), é uma compra
        if transfer['to'].lower() == self.contrato:
            token_address = transfer['contractAddress']
            token_name = transfer.get('tokenName', 'Unknown')
            token_symbol = transfer.get('tokenSymbol', '???')
            
            # Calcula quantidade (divide por decimals)
            try:
                amount = int(transfer['value']) / (10 ** int(transfer['tokenDecimal']))
            except:
                amount = 0
            
            return {
                'tipo': 'COMPRA',
                'token_address': token_address,
                'token_name': token_name,
                'token_symbol': token_symbol,
                'quantidade': amount,
                'hash': transfer['hash'],
                'timestamp': transfer['timeStamp'],
                'from': transfer['from']
            }
        
        return None
    
    def alertar_compra_nova(self, compra):
        """Alerta quando compra token novo"""
        print("\n" + "="*70)
        print("🚨🚨🚨 COMPRA DE TOKEN DETECTADA! 🚨🚨🚨")
        print("="*70)
        
        # Formata timestamp
        try:
            ts = int(compra['timestamp'])
            dt = datetime.fromtimestamp(ts)
            tempo = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            tempo = "N/A"
        
        print(f"\n💰 TOKEN: {compra['token_name']} (${compra['token_symbol']})")
        print(f"📊 QUANTIDADE: {compra['quantidade']:,.2f}")
        print(f"📍 ENDEREÇO: {compra['token_address']}")
        print(f"⏰ TIMESTAMP: {tempo}")
        print(f"🔗 TX HASH: {compra['hash']}")
        print(f"👤 FROM: {compra['from']}")
        
        # Links úteis
        print(f"\n🔍 LINKS:")
        print(f"   BaseScan TX: https://basescan.org/tx/{compra['hash']}")
        print(f"   BaseScan Token: https://basescan.org/token/{compra['token_address']}")
        print(f"   DEXScreener: https://dexscreener.com/base/{compra['token_address']}")
        
        print("\n" + "="*70)
        print("🔊🔊🔊 APITANDO 8x (888 Hz por 888 ms cada) 🔊🔊🔊")
        print("="*70 + "\n")
        
        # Apita 8x
        for i in range(8):
            print(f"🔊 Apito {i+1}/8...", end=" ", flush=True)
            try:
                winsound.Beep(888, 888)
                print("✓")
            except Exception as e:
                print(f"✗")
            time.sleep(0.1)
        
        print("\n" + "="*70)
        print("✅ ALERTA COMPLETO!")
        print("="*70 + "\n")
        
        # Salva histórico
        self.salvar_historico_compra(compra)
    
    def salvar_historico_compra(self, compra):
        """Salva compra no histórico"""
        try:
            historico_file = "historico_compras.json"
            historico = []
            
            if os.path.exists(historico_file):
                with open(historico_file, 'r', encoding='utf-8') as f:
                    historico = json.load(f)
            
            historico.append({
                **compra,
                'detectado_em': datetime.now().isoformat()
            })
            
            with open(historico_file, 'w', encoding='utf-8') as f:
                json.dump(historico, f, indent=2, ensure_ascii=False)
                
        except:
            pass
    
    def verificar(self):
        """Verifica novas compras"""
        print(" 🔍 Buscando transações...", end=" ", flush=True)
        
        # Busca token transfers
        transfers = self.buscar_token_transfers()
        
        if not transfers:
            print("❌ Nenhuma transação encontrada")
            return False
        
        print(f"✓ {len(transfers)} transfers encontrados")
        
        # Analisa cada transfer
        compras_novas = []
        
        for transfer in transfers:
            # Se já vimos essa TX, para
            if self.ultimo_tx_hash and transfer['hash'] == self.ultimo_tx_hash:
                break
            
            # Analisa se é compra
            compra = self.analisar_token_transfer(transfer)
            
            if compra:
                token_addr = compra['token_address'].lower()
                
                # Se é um token novo (não conhecíamos antes)
                if token_addr not in self.tokens_conhecidos:
                    compras_novas.append(compra)
                    self.tokens_conhecidos.add(token_addr)
        
        # Se é primeira execução, só salva
        if self.ultimo_tx_hash is None:
            if transfers:
                self.ultimo_tx_hash = transfers[0]['hash']
                # Marca todos os tokens atuais como conhecidos
                for transfer in transfers:
                    compra = self.analisar_token_transfer(transfer)
                    if compra:
                        self.tokens_conhecidos.add(compra['token_address'].lower())
                
                print(f" ✓ Inicializado com {len(transfers)} TXs e {len(self.tokens_conhecidos)} tokens")
                self.salvar_cache()
            return False
        
        # Atualiza último hash
        if transfers:
            self.ultimo_tx_hash = transfers[0]['hash']
            self.salvar_cache()
        
        # Alerta compras novas
        if compras_novas:
            for compra in compras_novas:
                self.alertar_compra_nova(compra)
            return True
        
        return False
    
    def rodar(self):
        """Loop principal"""
        print("="*70)
        print("🔗 MONITOR ON-CHAIN - BASE NETWORK")
        print("="*70)
        print(f"\n📍 Contrato: {self.contrato}")
        print(f"⏱️  Intervalo: {self.intervalo} segundos")
        print(f"🔊 Alerta: 8 apitos de 888 Hz por 888 ms")
        print(f"\nMonitorando compras de tokens ERC-20...")
        print("\nPressione Ctrl+C para parar\n")
        print("="*70)
        
        contador = 0
        
        try:
            while True:
                contador += 1
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"\n[{timestamp}] Verificação #{contador}...")
                
                tem_compra = self.verificar()
                
                if tem_compra:
                    print("🎉 COMPRA NOVA DETECTADA!")
                else:
                    print("✓ Tudo verificado - sem compras novas")
                
                print(f"\n⏳ Aguardando {self.intervalo}s até próxima verificação...")
                time.sleep(self.intervalo)
                
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("🛑 Monitor parado pelo usuário")
            print("="*70)
            print(f"\nTotal de verificações: {contador}")
            print(f"Tokens conhecidos: {len(self.tokens_conhecidos)}")
            print(f"Última TX: {self.ultimo_tx_hash}")
            
            # Mostra tokens conhecidos
            if self.tokens_conhecidos:
                print(f"\n📊 Tokens monitorados ({len(self.tokens_conhecidos)}):")
                for i, token in enumerate(list(self.tokens_conhecidos)[:10], 1):
                    print(f"   {i}. {token[:8]}...{token[-6:]}")
                if len(self.tokens_conhecidos) > 10:
                    print(f"   ... e mais {len(self.tokens_conhecidos) - 10} tokens")
            
            print()

def main():
    # Configuração
    CONTRATO = "0xFb653a4061cE35b66e2Ba090Cf1Fabe32f294079"
    INTERVALO = 30
    
    print("="*70)
    print("CONFIGURAÇÃO DO MONITOR ON-CHAIN")
    print("="*70)
    print(f"\nContrato Base: {CONTRATO}")
    print(f"Intervalo padrão: {INTERVALO} segundos")
    
    # Opção de mudar contrato
    print("\nDeseja monitorar outro contrato? (Enter para manter)")
    resposta = input("Digite o endereço do contrato (ou Enter): ").strip()
    if resposta:
        CONTRATO = resposta
        print(f"✓ Contrato alterado")
    
    # Opção de mudar intervalo
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
    monitor = BaseChainMonitor(CONTRATO, INTERVALO)
    monitor.rodar()

if __name__ == "__main__":
    main()
