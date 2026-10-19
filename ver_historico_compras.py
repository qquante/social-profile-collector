"""
Visualiza o histórico de compras detectadas
"""

import json
import os
from datetime import datetime

def main():
    print("="*70)
    print("📊 HISTÓRICO DE COMPRAS - BASE NETWORK")
    print("="*70)
    print()
    
    historico_file = "historico_compras.json"
    
    if not os.path.exists(historico_file):
        print("❌ Nenhum histórico encontrado ainda")
        print("\nO histórico será criado quando o monitor detectar a primeira compra.")
        input("\nPressione Enter para sair...")
        return
    
    # Lê histórico
    with open(historico_file, 'r', encoding='utf-8') as f:
        compras = json.load(f)
    
    if not compras:
        print("❌ Histórico vazio")
        input("\nPressione Enter para sair...")
        return
    
    print(f"📦 Total de compras detectadas: {len(compras)}\n")
    print("="*70)
    
    # Mostra cada compra
    for i, compra in enumerate(reversed(compras), 1):
        print(f"\n[COMPRA #{i}]")
        print("-" * 70)
        
        print(f"💰 Token: {compra['token_name']} (${compra['token_symbol']})")
        print(f"📊 Quantidade: {compra['quantidade']:,.2f}")
        print(f"📍 Endereço: {compra['token_address']}")
        
        # Timestamp
        try:
            ts = int(compra['timestamp'])
            dt = datetime.fromtimestamp(ts)
            tempo = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            tempo = "N/A"
        
        print(f"⏰ Quando: {tempo}")
        print(f"🔗 TX: {compra['hash'][:16]}...{compra['hash'][-8:]}")
        
        # Quando foi detectado
        if 'detectado_em' in compra:
            try:
                detectado = datetime.fromisoformat(compra['detectado_em'])
                print(f"🔔 Detectado: {detectado.strftime('%Y-%m-%d %H:%M:%S')}")
            except:
                pass
        
        # Links
        print(f"\n🔍 Ver no BaseScan:")
        print(f"   https://basescan.org/tx/{compra['hash']}")
        print(f"   https://basescan.org/token/{compra['token_address']}")
        print(f"\n📈 Ver no DEXScreener:")
        print(f"   https://dexscreener.com/base/{compra['token_address']}")
        
        print("-" * 70)
    
    # Estatísticas
    print("\n" + "="*70)
    print("📊 ESTATÍSTICAS")
    print("="*70)
    
    tokens_unicos = set(c['token_address'] for c in compras)
    print(f"\n✓ Total de compras: {len(compras)}")
    print(f"✓ Tokens únicos: {len(tokens_unicos)}")
    
    # Token mais comprado
    from collections import Counter
    token_counts = Counter(c['token_symbol'] for c in compras)
    if token_counts:
        mais_comprado = token_counts.most_common(1)[0]
        print(f"✓ Token mais comprado: ${mais_comprado[0]} ({mais_comprado[1]}x)")
    
    print("\n" + "="*70)
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
