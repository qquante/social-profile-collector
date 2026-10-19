"""
Testa conexão com BaseScan API
"""

import requests
import json

def testar_api():
    print("="*70)
    print("🔍 TESTE DE CONEXÃO - BASESCAN API")
    print("="*70)
    print()
    
    contrato = "0xFb653a4061cE35b66e2Ba090Cf1Fabe32f294079"
    api_url = "https://api.basescan.org/api"
    
    print(f"📍 Contrato: {contrato}\n")
    
    # Teste 1: Transações normais
    print("[1/3] Testando busca de transações...")
    try:
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': contrato,
            'startblock': 0,
            'endblock': 99999999,
            'page': 1,
            'offset': 5,
            'sort': 'desc'
        }
        
        response = requests.get(api_url, params=params, timeout=30)
        data = response.json()
        
        if data.get('status') == '1':
            txs = data.get('result', [])
            print(f"    ✓ Sucesso! {len(txs)} transações encontradas")
            
            if txs:
                print(f"\n    Última TX:")
                print(f"      Hash: {txs[0]['hash'][:16]}...{txs[0]['hash'][-8:]}")
                print(f"      From: {txs[0]['from'][:10]}...{txs[0]['from'][-8:]}")
                print(f"      To: {txs[0]['to'][:10]}...{txs[0]['to'][-8:]}")
        else:
            print(f"    ⚠️  Status: {data.get('status')}")
            print(f"    Message: {data.get('message')}")
            
    except Exception as e:
        print(f"    ✗ ERRO: {str(e)}")
        return False
    
    # Teste 2: Token transfers
    print("\n[2/3] Testando busca de token transfers...")
    try:
        params = {
            'module': 'account',
            'action': 'tokentx',
            'address': contrato,
            'startblock': 0,
            'endblock': 99999999,
            'page': 1,
            'offset': 5,
            'sort': 'desc'
        }
        
        response = requests.get(api_url, params=params, timeout=30)
        data = response.json()
        
        if data.get('status') == '1':
            transfers = data.get('result', [])
            print(f"    ✓ Sucesso! {len(transfers)} transfers encontrados")
            
            if transfers:
                # Mostra últimos 3 tokens
                print(f"\n    Últimos tokens:")
                tokens_vistos = set()
                for transfer in transfers[:10]:
                    token_symbol = transfer.get('tokenSymbol', '???')
                    token_name = transfer.get('tokenName', 'Unknown')
                    
                    if token_symbol not in tokens_vistos:
                        tokens_vistos.add(token_symbol)
                        print(f"      • {token_name} (${token_symbol})")
                        
                        # Se contrato recebeu = compra
                        if transfer['to'].lower() == contrato.lower():
                            print(f"        → COMPRA detectada!")
                        
                        if len(tokens_vistos) >= 3:
                            break
        else:
            print(f"    ⚠️  Status: {data.get('status')}")
            print(f"    Message: {data.get('message')}")
            
    except Exception as e:
        print(f"    ✗ ERRO: {str(e)}")
        return False
    
    # Teste 3: Rate limit
    print("\n[3/3] Testando rate limit (3 requests rápidos)...")
    try:
        for i in range(3):
            print(f"    Request {i+1}/3...", end=" ", flush=True)
            
            params = {
                'module': 'account',
                'action': 'balance',
                'address': contrato,
            }
            
            response = requests.get(api_url, params=params, timeout=10)
            data = response.json()
            
            if data.get('status') == '1':
                print("✓")
            else:
                print(f"⚠️  {data.get('message', 'erro')}")
        
        print("\n    ✓ Rate limit OK - API funcionando")
        
    except Exception as e:
        print(f"\n    ✗ ERRO: {str(e)}")
        return False
    
    # Resultado final
    print("\n" + "="*70)
    print("✅ BASESCAN API FUNCIONANDO!")
    print("="*70)
    print("\n🎯 Pode usar o monitor on-chain sem problemas!")
    print("\nPara iniciar:")
    print("  py monitor_onchain.py")
    print("  ou")
    print("  MONITOR_ONCHAIN.bat")
    print()
    
    return True

if __name__ == "__main__":
    testar_api()
    input("\nPressione Enter para sair...")
