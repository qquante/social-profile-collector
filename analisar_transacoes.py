"""
Análise Forense de Transações - Base Network
Debug completo de cada TX usando RPC direto
"""

import requests
import json
from datetime import datetime
from config_rpc import ANKR_RPC_HTTP, CONTRATO
from decodificar_input import decodificar_swap_params, formatar_decoded

class AnalisadorTX:
    def __init__(self):
        self.rpc_url = ANKR_RPC_HTTP
        self.contrato = CONTRATO.lower()
        print(f"[RPC] Usando: {self.rpc_url[:50]}...")
        print(f"[CONTRATO] {self.contrato}")
    
    def rpc_call(self, method, params):
        """Faz chamada RPC"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": 1
            }
            
            response = requests.post(self.rpc_url, json=payload, timeout=30)
            data = response.json()
            
            if 'result' in data:
                return data['result']
            elif 'error' in data:
                print(f"RPC Error: {data['error']}")
            
            return None
            
        except Exception as e:
            print(f"Erro na chamada RPC: {e}")
            return None
    
    def buscar_tx(self, tx_hash):
        """Busca informações básicas da TX via RPC"""
        return self.rpc_call('eth_getTransactionByHash', [tx_hash])
    
    def buscar_receipt(self, tx_hash):
        """Busca receipt da TX (logs, status, etc) via RPC"""
        return self.rpc_call('eth_getTransactionReceipt', [tx_hash])
    
    def buscar_block(self, block_number):
        """Busca informações do bloco"""
        return self.rpc_call('eth_getBlockByNumber', [block_number, True])
    
    def trace_transaction(self, tx_hash):
        """Tenta fazer trace da transação para ver internal calls"""
        # Alguns RPCs suportam debug_traceTransaction
        try:
            result = self.rpc_call('debug_traceTransaction', [tx_hash, {"tracer": "callTracer"}])
            return result
        except:
            # Se não suportar, retorna None
            return None
    
    def decodificar_input(self, input_data):
        """Tenta decodificar o input data"""
        if not input_data or input_data == '0x':
            return "Sem input data"
        
        # Pega method ID (primeiros 10 caracteres: 0x + 8 hex)
        method_id = input_data[:10]
        
        # Method IDs conhecidos de DEXs
        methods = {
            '0x38ed1739': 'swapExactTokensForTokens',
            '0x8803dbee': 'swapTokensForExactTokens',
            '0x7ff36ab5': 'swapExactETHForTokens',
            '0x18cbafe5': 'swapExactTokensForETH',
            '0x791ac947': 'swapExactTokensForTokensSupportingFeeOnTransferTokens',
            '0xb6f9de95': 'swapExactETHForTokensSupportingFeeOnTransferTokens',
            '0xa9059cbb': 'transfer (ERC20)',
            '0x23b872dd': 'transferFrom (ERC20)',
            '0x095ea7b3': 'approve (ERC20)',
            '0x022c0d9f': 'swap (Uniswap V2 Pair)',
            '0x128acb08': 'swap (Uniswap V3)',
            '0x414bf389': 'exactInputSingle (Uniswap V3)',
            '0xc04b8d59': 'exactInput (Uniswap V3)',
        }
        
        method_name = methods.get(method_id, f"Unknown ({method_id})")
        
        return {
            'method_id': method_id,
            'method_name': method_name,
            'raw_input': input_data
        }
    
    def analisar_logs(self, logs):
        """Analisa logs da TX para encontrar transfers e eventos"""
        eventos = []
        
        # Event signatures conhecidos
        transfer_signature = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'  # Transfer(address,address,uint256)
        swap_signature = '0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822'  # Swap(...)
        
        for log in logs:
            topics = log.get('topics', [])
            
            if not topics:
                continue
            
            event_sig = topics[0]
            
            if event_sig == transfer_signature:
                # Transfer event
                if len(topics) >= 3:
                    from_addr = '0x' + topics[1][-40:]
                    to_addr = '0x' + topics[2][-40:]
                    token_addr = log.get('address', '')
                    
                    # Converte value (em hex)
                    value_hex = log.get('data', '0x0')
                    try:
                        value = int(value_hex, 16)
                    except:
                        value = 0
                    
                    eventos.append({
                        'tipo': 'Transfer',
                        'token': token_addr,
                        'from': from_addr,
                        'to': to_addr,
                        'value_raw': value,
                        'envolvido': from_addr.lower() == self.contrato.lower() or to_addr.lower() == self.contrato.lower()
                    })
            
            elif event_sig == swap_signature:
                eventos.append({
                    'tipo': 'Swap',
                    'data': log.get('data', '')
                })
        
        return eventos
    
    def analisar_tx_completa(self, tx_hash):
        """Análise completa de uma transação"""
        print("\n" + "="*80)
        print(f"🔍 ANÁLISE FORENSE DA TRANSAÇÃO")
        print("="*80)
        print(f"\nTX Hash: {tx_hash}")
        print(f"Link: https://basescan.org/tx/{tx_hash}")
        
        # 1. Busca TX básica
        print("\n" + "-"*80)
        print("📊 DADOS BÁSICOS DA TRANSAÇÃO")
        print("-"*80)
        
        tx = self.buscar_tx(tx_hash)
        
        if not tx:
            print("❌ Não foi possível buscar a transação")
            return None
        
        print(f"\nFrom: {tx.get('from', 'N/A')}")
        print(f"To: {tx.get('to', 'N/A')}")
        
        # Value em ETH
        value_wei = int(tx.get('value', '0x0'), 16)
        value_eth = value_wei / 1e18
        print(f"Value: {value_eth:.6f} ETH")
        
        # Gas
        gas_price_wei = int(tx.get('gasPrice', '0x0'), 16)
        gas_price_gwei = gas_price_wei / 1e9
        print(f"Gas Price: {gas_price_gwei:.4f} Gwei")
        
        # Block
        block = int(tx.get('blockNumber', '0x0'), 16)
        print(f"Block: {block}")
        
        # 2. Decodifica Input
        print("\n" + "-"*80)
        print("🔓 INPUT DATA DECODIFICADO")
        print("-"*80)
        
        input_decoded = self.decodificar_input(tx.get('input', '0x'))
        
        if isinstance(input_decoded, dict):
            print(f"\nMethod ID: {input_decoded['method_id']}")
            print(f"Method Name: {input_decoded['method_name']}")
            print(f"\nRaw Input Length: {len(input_decoded['raw_input'])} caracteres")
            
            # Mostra primeiros bytes
            raw = input_decoded['raw_input']
            if len(raw) > 200:
                print(f"Primeiros bytes: {raw[:200]}...")
            else:
                print(f"Input completo: {raw}")
            
            # Tenta decodificar parâmetros
            print("\n🔓 DECODIFICANDO PARÂMETROS...")
            decoded_params = decodificar_swap_params(raw)
            
            if decoded_params:
                formatted = formatar_decoded(decoded_params)
                if formatted:
                    print(formatted)
                else:
                    print("   Parâmetros não decodificados completamente")
                    if 'decoded' in decoded_params:
                        print(f"   Dados parciais: {decoded_params['decoded']}")
        else:
            print(input_decoded)
        
        # 3. Busca Receipt (logs)
        print("\n" + "-"*80)
        print("📜 LOGS E EVENTOS")
        print("-"*80)
        
        receipt = self.buscar_receipt(tx_hash)
        
        if receipt:
            status = receipt.get('status', '0x0')
            print(f"\nStatus: {'✅ SUCCESS' if status == '0x1' else '❌ FAILED'}")
            
            gas_used = int(receipt.get('gasUsed', '0x0'), 16)
            print(f"Gas Used: {gas_used:,}")
            
            logs = receipt.get('logs', [])
            print(f"\nTotal de Logs: {len(logs)}")
            
            # Analisa eventos
            eventos = self.analisar_logs(logs)
            
            if eventos:
                print(f"\n🔍 EVENTOS DETECTADOS ({len(eventos)}):")
                
                transfers = [e for e in eventos if e['tipo'] == 'Transfer']
                swaps = [e for e in eventos if e['tipo'] == 'Swap']
                
                print(f"\n   Transfer events: {len(transfers)}")
                print(f"   Swap events: {len(swaps)}")
                
                # Mostra transfers envolvendo o contrato
                print("\n   💸 TRANSFERS ENVOLVENDO O CONTRATO:")
                for i, t in enumerate([e for e in transfers if e.get('envolvido')], 1):
                    direcao = "📥 RECEBEU" if t['to'].lower() == self.contrato.lower() else "📤 ENVIOU"
                    print(f"\n   [{i}] {direcao}")
                    print(f"       Token: {t['token']}")
                    print(f"       From: {t['from'][:10]}...{t['from'][-8:]}")
                    print(f"       To: {t['to'][:10]}...{t['to'][-8:]}")
                    print(f"       Value (raw): {t['value_raw']:,}")
        
        # 4. Informações do Bloco
        print("\n" + "-"*80)
        print("⛓️  INFORMAÇÕES DO BLOCO")
        print("-"*80)
        
        if receipt:
            block_number = receipt.get('blockNumber', '0x0')
            block_info = self.buscar_block(block_number)
            
            if block_info:
                timestamp = int(block_info.get('timestamp', '0x0'), 16)
                dt = datetime.fromtimestamp(timestamp)
                print(f"\nBlock: {int(block_number, 16)}")
                print(f"Timestamp: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Total TXs no bloco: {len(block_info.get('transactions', []))}")
        
        # 5. Trace (se disponível)
        print("\n" + "-"*80)
        print("🔍 TRACE DA TRANSAÇÃO")
        print("-"*80)
        
        print("\nTentando fazer trace...")
        trace = self.trace_transaction(tx_hash)
        
        if trace:
            print("✅ Trace obtido com sucesso!")
            # Analisa trace para ver chamadas internas
            if isinstance(trace, dict):
                print(f"\nTipo: {trace.get('type', 'N/A')}")
                if 'calls' in trace:
                    calls = trace['calls']
                    print(f"Chamadas internas: {len(calls)}")
                    for i, call in enumerate(calls[:5], 1):
                        print(f"\n  [{i}] {call.get('type', 'CALL')}")
                        print(f"      From: {call.get('from', 'N/A')[:10]}...")
                        print(f"      To: {call.get('to', 'N/A')[:10]}...")
                        if call.get('value'):
                            val = int(call['value'], 16) / 1e18
                            print(f"      Value: {val:.6f} ETH")
        else:
            print("⚠️  Trace não disponível (RPC pode não suportar)")
        
        # 5. Conclusão
        print("\n" + "="*80)
        print("🎯 CONCLUSÃO DA ANÁLISE")
        print("="*80)
        
        if receipt and eventos:
            # Analisa o que aconteceu
            transfers_recebidos = [e for e in eventos if e['tipo'] == 'Transfer' and e.get('envolvido') and e['to'].lower() == self.contrato.lower()]
            transfers_enviados = [e for e in eventos if e['tipo'] == 'Transfer' and e.get('envolvido') and e['from'].lower() == self.contrato.lower()]
            
            if transfers_recebidos:
                print(f"\n✅ CONTRATO RECEBEU {len(transfers_recebidos)} token(s) - POSSÍVEL COMPRA")
                for t in transfers_recebidos:
                    print(f"   📍 Token: {t['token']}")
                    print(f"      Link: https://basescan.org/token/{t['token']}")
            
            if transfers_enviados:
                print(f"\n📤 CONTRATO ENVIOU {len(transfers_enviados)} token(s) - POSSÍVEL VENDA/PAGAMENTO")
                for t in transfers_enviados:
                    print(f"   📍 Token: {t['token']}")
            
            # Identifica padrão
            if input_decoded and isinstance(input_decoded, dict):
                method = input_decoded['method_name']
                if 'swap' in method.lower():
                    print(f"\n💱 TIPO: SWAP detectado ({method})")
                    print(f"   Contrato chamou função de swap em DEX")
                elif 'transfer' in method.lower():
                    print(f"\n💸 TIPO: TRANSFER direto ({method})")
        
        print("\n" + "="*80)
        
        return {
            'tx': tx,
            'receipt': receipt,
            'input_decoded': input_decoded,
            'eventos': eventos
        }

def main():
    print("="*80)
    print("🔍 ANÁLISE FORENSE DE TRANSAÇÕES - BASE NETWORK")
    print("="*80)
    print("\nContrato analisado:")
    print("0xFb653a4061cE35b66e2Ba090Cf1Fabe32f294079")
    
    # TXs para analisar
    txs = [
        "0xd6c8f9bcc57c501ef070d86ea43d700ec32804961adb23abd330d52a466db496",
        "0xe6b9640ad77eeead3240f5cae6d61be8501607f8a7839811ac8808e276d83fce",
        "0xe5a74df5c5e526182f0aec7ca286e2e24dd0043266d0d77981bfa141d73e7076"
    ]
    
    analisador = AnalisadorTX()
    resultados = []
    
    for i, tx_hash in enumerate(txs, 1):
        print(f"\n\n{'#'*80}")
        print(f"TRANSAÇÃO {i}/3")
        print(f"{'#'*80}")
        
        resultado = analisador.analisar_tx_completa(tx_hash)
        resultados.append(resultado)
        
        input("\nPressione Enter para analisar próxima TX...")
    
    # Resumo final
    print("\n\n" + "="*80)
    print("📊 RESUMO GERAL DAS 3 TRANSAÇÕES")
    print("="*80)
    
    print("\n🎯 PADRÕES IDENTIFICADOS:")
    print("\nTodos os métodos usados:")
    for i, r in enumerate(resultados, 1):
        if r and r.get('input_decoded'):
            decoded = r['input_decoded']
            if isinstance(decoded, dict):
                print(f"  TX {i}: {decoded.get('method_name', 'N/A')}")
    
    print("\n\n✅ Análise completa! Verifique os detalhes acima.")
    print("\nAgora posso criar um monitor baseado nos padrões identificados!")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
