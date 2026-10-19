"""
Busca informações de tokens ERC-20
Nome, símbolo, decimais
"""

import requests
from config_rpc import ANKR_RPC_HTTP

class TokenInfo:
    def __init__(self):
        self.rpc_url = ANKR_RPC_HTTP
        self.cache = {}
    
    def rpc_call(self, method, params):
        """Faz chamada RPC"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": 1
            }
            
            response = requests.post(self.rpc_url, json=payload, timeout=10)
            data = response.json()
            
            if 'result' in data:
                return data['result']
            
            return None
            
        except Exception as e:
            return None
    
    def eth_call(self, to_address, data):
        """Faz eth_call"""
        return self.rpc_call('eth_call', [
            {
                'to': to_address,
                'data': data
            },
            'latest'
        ])
    
    def get_token_name(self, token_address):
        """Busca nome do token"""
        # name() = 0x06fdde03
        result = self.eth_call(token_address, '0x06fdde03')
        
        if result and result != '0x':
            try:
                # Decodifica string
                hex_str = result[2:] if result.startswith('0x') else result
                # Remove offset e length (primeiros 64 bytes)
                if len(hex_str) > 128:
                    hex_str = hex_str[128:]
                # Converte hex para string
                name = bytes.fromhex(hex_str).decode('utf-8', errors='ignore').strip('\x00')
                return name if name else None
            except:
                return None
        return None
    
    def get_token_symbol(self, token_address):
        """Busca símbolo do token"""
        # symbol() = 0x95d89b41
        result = self.eth_call(token_address, '0x95d89b41')
        
        if result and result != '0x':
            try:
                hex_str = result[2:] if result.startswith('0x') else result
                if len(hex_str) > 128:
                    hex_str = hex_str[128:]
                symbol = bytes.fromhex(hex_str).decode('utf-8', errors='ignore').strip('\x00')
                return symbol if symbol else None
            except:
                return None
        return None
    
    def get_token_decimals(self, token_address):
        """Busca decimais do token"""
        # decimals() = 0x313ce567
        result = self.eth_call(token_address, '0x313ce567')
        
        if result and result != '0x':
            try:
                return int(result, 16)
            except:
                return 18  # Default
        return 18
    
    def get_token_info(self, token_address):
        """Busca todas as informações do token"""
        token_address = token_address.lower()
        
        # Verifica cache
        if token_address in self.cache:
            return self.cache[token_address]
        
        print(f"[TOKEN INFO] Buscando info de {token_address[:10]}...")
        
        info = {
            'address': token_address,
            'name': self.get_token_name(token_address),
            'symbol': self.get_token_symbol(token_address),
            'decimals': self.get_token_decimals(token_address)
        }
        
        # Se não conseguiu pegar nome/símbolo, usa padrões
        if not info['name']:
            info['name'] = f"Token {token_address[:8]}..."
        
        if not info['symbol']:
            info['symbol'] = "???"
        
        # Cache
        self.cache[token_address] = info
        
        print(f"[TOKEN INFO] {info['name']} (${info['symbol']})")
        
        return info
    
    def format_amount(self, raw_amount, decimals):
        """Formata quantidade com decimais"""
        try:
            amount = int(raw_amount) / (10 ** decimals)
            
            # Formatação inteligente
            if amount >= 1_000_000_000_000:  # Trilhões
                return f"{amount/1_000_000_000_000:.2f} Trillion"
            elif amount >= 1_000_000_000:  # Bilhões
                return f"{amount/1_000_000_000:.2f} Billion"
            elif amount >= 1_000_000:  # Milhões
                return f"{amount/1_000_000:.2f} Million"
            elif amount >= 1_000:  # Milhares
                return f"{amount/1_000:.2f}K"
            else:
                return f"{amount:.2f}"
                
        except:
            return str(raw_amount)
