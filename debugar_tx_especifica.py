"""
Debug de TX específica
"""

import requests
import json
from datetime import datetime
from config_rpc import ANKR_RPC_HTTP, CONTRATO

def rpc_call(method, params):
    """Faz chamada RPC"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        
        response = requests.post(ANKR_RPC_HTTP, json=payload, timeout=30)
        data = response.json()
        
        if 'result' in data:
            return data['result']
        
        return None
        
    except Exception as e:
        print(f"Erro: {e}")
        return None

def debug_tx(tx_hash):
    """Debug de uma TX"""
    print("="*80)
    print(f"🔍 DEBUG DA TRANSAÇÃO")
    print("="*80)
    print(f"\nTX: {tx_hash}")
    print(f"Link: https://basescan.org/tx/{tx_hash}")
    
    # Busca TX
    print("\n[1/2] Buscando transação...")
    tx = rpc_call('eth_getTransactionByHash', [tx_hash])
    
    if not tx:
        print("❌ TX não encontrada!")
        return
    
    print(f"✓ TX encontrada")
    print(f"  From: {tx.get('from')}")
    print(f"  To: {tx.get('to')}")
    print(f"  Block: {int(tx.get('blockNumber', '0x0'), 16)}")
    
    # Busca receipt
    print("\n[2/2] Buscando receipt e logs...")
    receipt = rpc_call('eth_getTransactionReceipt', [tx_hash])
    
    if not receipt:
        print("❌ Receipt não encontrado!")
        return
    
    print(f"✓ Receipt encontrado")
    
    # Analisa logs
    logs = receipt.get('logs', [])
    print(f"\nTotal de logs: {len(logs)}")
    
    transfer_sig = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
    
    print("\n" + "="*80)
    print("TRANSFER EVENTS:")
    print("="*80)
    
    contrato_lower = CONTRATO.lower()
    usdc = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
    
    for i, log in enumerate(logs, 1):
        topics = log.get('topics', [])
        
        if not topics or topics[0] != transfer_sig:
            continue
        
        token = log.get('address', '').lower()
        from_addr = '0x' + topics[1][-40:].lower()
        to_addr = '0x' + topics[2][-40:].lower()
        
        data_hex = log.get('data', '0x0')
        try:
            value = int(data_hex, 16)
        except:
            value = 0
        
        # Verifica se envolve o contrato
        envolve_contrato = from_addr == contrato_lower or to_addr == contrato_lower
        
        if envolve_contrato:
            print(f"\n[Transfer #{i}] {'✅ ENVOLVE CONTRATO' if envolve_contrato else ''}")
            print(f"  Token: {token}")
            
            if token == usdc:
                print(f"  → É USDC!")
            
            print(f"  From: {from_addr}")
            print(f"  To: {to_addr}")
            print(f"  Value: {value:,}")
            
            if from_addr == contrato_lower:
                print(f"  ⚠️  CONTRATO ENVIOU (OUT)")
            
            if to_addr == contrato_lower:
                print(f"  ✅ CONTRATO RECEBEU (IN)")
    
    # Conclusão
    print("\n" + "="*80)
    print("ANÁLISE:")
    print("="*80)
    
    # Verifica timestamp
    block_num = receipt.get('blockNumber', '0x0')
    block = rpc_call('eth_getBlockByNumber', [block_num, False])
    
    if block:
        timestamp = int(block.get('timestamp', '0x0'), 16)
        dt = datetime.fromtimestamp(timestamp)
        print(f"\nTimestamp: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Quanto tempo atrás
        agora = datetime.now()
        diff = agora - dt
        horas = diff.total_seconds() / 3600
        print(f"Há quanto tempo: {horas:.1f} horas atrás")
    
    print("\n" + "="*80)
    print("POR QUE O MONITOR NÃO CAPTUROU:")
    print("="*80)
    print("""
O WebSocket só captura eventos DEPOIS que você conecta!

Eventos PASSADOS não são enviados automaticamente.

Esta TX aconteceu ANTES do monitor iniciar, por isso não foi capturada.

SOLUÇÃO:
- Monitor está rodando AGORA
- Próximas compras serão detectadas em TEMPO REAL
- Para pegar históricas, precisa fazer scan de blocos antigos
    """)

def main():
    tx_hash = "0xb6620d356b4ad1ae5ccbfcda48cc5e877497ff1c7e60563d5e680fa7ca6fecb8"
    debug_tx(tx_hash)
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
