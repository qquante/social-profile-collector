"""
Decodificador avançado de Input Data
Extrai parâmetros de funções conhecidas
"""

def hex_to_address(hex_str):
    """Converte hex para endereço"""
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]
    # Endereço são os últimos 40 caracteres
    return '0x' + hex_str[-40:]

def hex_to_int(hex_str):
    """Converte hex para int"""
    try:
        return int(hex_str, 16)
    except:
        return 0

def decodificar_swap_params(input_data):
    """
    Decodifica parâmetros de funções swap comuns
    swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] path, address to, uint deadline)
    """
    if len(input_data) < 10:
        return None
    
    method_id = input_data[:10]
    params_hex = input_data[10:]
    
    resultado = {
        'method_id': method_id,
        'params_raw': params_hex
    }
    
    # Tenta decodificar baseado no método
    if method_id in ['0x38ed1739', '0x791ac947']:  # swapExactTokensForTokens variants
        try:
            # Cada parâmetro é 32 bytes (64 hex chars)
            chunks = [params_hex[i:i+64] for i in range(0, len(params_hex), 64)]
            
            if len(chunks) >= 5:
                amount_in = hex_to_int('0x' + chunks[0])
                amount_out_min = hex_to_int('0x' + chunks[1])
                
                # Path offset geralmente é chunks[2]
                path_offset = hex_to_int('0x' + chunks[2]) // 32
                
                # To address
                to_address = hex_to_address('0x' + chunks[3])
                
                # Deadline
                deadline = hex_to_int('0x' + chunks[4])
                
                # Path array - começa no offset
                if path_offset < len(chunks):
                    path_length = hex_to_int('0x' + chunks[path_offset])
                    path_addresses = []
                    
                    for i in range(path_length):
                        addr_idx = path_offset + 1 + i
                        if addr_idx < len(chunks):
                            addr = hex_to_address('0x' + chunks[addr_idx])
                            path_addresses.append(addr)
                    
                    resultado['decoded'] = {
                        'amountIn': amount_in,
                        'amountOutMin': amount_out_min,
                        'path': path_addresses,
                        'to': to_address,
                        'deadline': deadline,
                        'token_from': path_addresses[0] if path_addresses else None,
                        'token_to': path_addresses[-1] if path_addresses else None
                    }
        except Exception as e:
            resultado['decode_error'] = str(e)
    
    elif method_id == '0xa9059cbb':  # transfer(address,uint256)
        try:
            chunks = [params_hex[i:i+64] for i in range(0, len(params_hex), 64)]
            
            if len(chunks) >= 2:
                to_address = hex_to_address('0x' + chunks[0])
                amount = hex_to_int('0x' + chunks[1])
                
                resultado['decoded'] = {
                    'to': to_address,
                    'amount': amount
                }
        except Exception as e:
            resultado['decode_error'] = str(e)
    
    elif method_id == '0x095ea7b3':  # approve(address,uint256)
        try:
            chunks = [params_hex[i:i+64] for i in range(0, len(params_hex), 64)]
            
            if len(chunks) >= 2:
                spender = hex_to_address('0x' + chunks[0])
                amount = hex_to_int('0x' + chunks[1])
                
                resultado['decoded'] = {
                    'spender': spender,
                    'amount': amount
                }
        except Exception as e:
            resultado['decode_error'] = str(e)
    
    return resultado

def formatar_decoded(decoded_data):
    """Formata dados decodificados de forma legível"""
    if not decoded_data or 'decoded' not in decoded_data:
        return None
    
    decoded = decoded_data['decoded']
    linhas = []
    
    if 'path' in decoded:
        # É um swap
        linhas.append("\n🔄 SWAP DETECTADO:")
        linhas.append(f"   Token From: {decoded.get('token_from', 'N/A')}")
        linhas.append(f"   Token To: {decoded.get('token_to', 'N/A')}")
        
        if decoded.get('amountIn'):
            linhas.append(f"   Amount In (raw): {decoded['amountIn']:,}")
        
        if decoded.get('amountOutMin'):
            linhas.append(f"   Amount Out Min (raw): {decoded['amountOutMin']:,}")
        
        linhas.append(f"   Recipient: {decoded.get('to', 'N/A')}")
        
        if decoded.get('path') and len(decoded['path']) > 2:
            linhas.append(f"\n   Path completo ({len(decoded['path'])} hops):")
            for i, addr in enumerate(decoded['path']):
                linhas.append(f"     {i+1}. {addr}")
    
    elif 'to' in decoded and 'amount' in decoded:
        # É um transfer
        linhas.append("\n💸 TRANSFER DETECTADO:")
        linhas.append(f"   To: {decoded['to']}")
        linhas.append(f"   Amount (raw): {decoded['amount']:,}")
    
    elif 'spender' in decoded:
        # É um approve
        linhas.append("\n✅ APPROVE DETECTADO:")
        linhas.append(f"   Spender: {decoded['spender']}")
        linhas.append(f"   Amount (raw): {decoded['amount']:,}")
    
    return '\n'.join(linhas) if linhas else None
