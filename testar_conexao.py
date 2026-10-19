"""
Testa a conexão com o MoltX antes de rodar o monitor
"""

import requests
import time

def testar_conexao():
    print("="*60)
    print("🔍 TESTE DE CONEXÃO - MoltX")
    print("="*60)
    print()
    
    url = "https://moltx.io/lauki"
    
    # Teste 1: Ping básico
    print("[1/3] Testando conexão básica...")
    try:
        inicio = time.time()
        response = requests.get(url, timeout=30)
        tempo = time.time() - inicio
        
        print(f"    ✓ Conectado!")
        print(f"    Status: {response.status_code}")
        print(f"    Tempo: {tempo:.2f} segundos")
        print(f"    Tamanho: {len(response.text):,} bytes")
        
    except requests.exceptions.Timeout:
        print(f"    ✗ TIMEOUT - Site demorou mais de 30 segundos")
        print(f"    Sua internet pode estar lenta")
        return False
        
    except requests.exceptions.ConnectionError:
        print(f"    ✗ ERRO DE CONEXÃO")
        print(f"    Verifique sua internet")
        return False
        
    except Exception as e:
        print(f"    ✗ ERRO: {str(e)}")
        return False
    
    # Teste 2: Velocidade
    print("\n[2/3] Testando velocidade (3 requests)...")
    tempos = []
    
    for i in range(3):
        try:
            print(f"    Request {i+1}/3...", end=" ", flush=True)
            inicio = time.time()
            response = requests.get(url, timeout=30)
            tempo = time.time() - inicio
            tempos.append(tempo)
            print(f"{tempo:.2f}s")
            time.sleep(1)
        except Exception as e:
            print(f"ERRO: {str(e)[:30]}")
    
    if tempos:
        media = sum(tempos) / len(tempos)
        print(f"\n    Tempo médio: {media:.2f}s")
        
        if media < 2:
            print(f"    ✓ RÁPIDO - Perfeito para o monitor!")
        elif media < 5:
            print(f"    ⚠️  NORMAL - Monitor vai funcionar")
        elif media < 10:
            print(f"    ⚠️  LENTO - Pode ter timeouts ocasionais")
        else:
            print(f"    ✗ MUITO LENTO - Monitor pode falhar")
    
    # Teste 3: Extração de dados
    print("\n[3/3] Testando extração de posts...")
    try:
        import re
        pattern = r'<article class="post" data-post-href="(/post/[^"]+)">'
        posts = re.findall(pattern, response.text)
        
        print(f"    ✓ Posts encontrados: {len(posts)}")
        
        if posts:
            print(f"    Último post: {posts[0]}")
        
    except Exception as e:
        print(f"    ✗ Erro na extração: {str(e)}")
        return False
    
    # Resultado final
    print("\n" + "="*60)
    if tempos and sum(tempos)/len(tempos) < 10 and posts:
        print("✅ TUDO OK! Pode usar o monitor sem problemas")
        print("="*60)
        print("\nPara iniciar o monitor, execute:")
        print("  py monitor.py")
        print("  ou")
        print("  MONITOR.bat")
        return True
    else:
        print("⚠️  ATENÇÃO: Conexão com problemas")
        print("="*60)
        print("\nRecomendações:")
        print("  1. Verifique sua conexão de internet")
        print("  2. Tente novamente em alguns minutos")
        print("  3. O site moltx.io pode estar sobrecarregado")
        print("\nVocê ainda pode tentar rodar o monitor,")
        print("mas pode ter timeouts frequentes.")
        return False
    
    print()

if __name__ == "__main__":
    testar_conexao()
    input("\nPressione Enter para sair...")
