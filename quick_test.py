"""
Script rápido para testar diferentes métodos de captura de dados do MoltX
"""

import requests
import json

def test_direct_api():
    """Testa acesso direto à API"""
    print("\n" + "="*60)
    print("TESTE 1: Acesso direto à API")
    print("="*60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    
    # Tenta diferentes endpoints comuns
    endpoints = [
        "https://api.moltx.io/users/lauki",
        "https://api.moltx.io/api/users/lauki",
        "https://moltx.io/api/users/lauki",
        "https://api.moltx.io/v1/users/lauki",
        "https://api.moltx.io/profiles/lauki",
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\n[*] Testando: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=5)
            print(f"    Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"    ✓ SUCESSO!")
                try:
                    data = response.json()
                    print(f"    Tipo: JSON")
                    print(f"    Keys: {list(data.keys()) if isinstance(data, dict) else 'lista'}")
                    return endpoint, data
                except:
                    print(f"    Tipo: {response.headers.get('Content-Type')}")
                    print(f"    Tamanho: {len(response.text)} bytes")
            
        except Exception as e:
            print(f"    ✗ Erro: {str(e)}")
    
    return None, None

def test_html_page():
    """Testa acesso à página HTML"""
    print("\n" + "="*60)
    print("TESTE 2: Página HTML")
    print("="*60)
    
    url = "https://moltx.io/lauki"
    
    try:
        print(f"\n[*] Acessando: {url}")
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, timeout=10)
        
        print(f"    Status: {response.status_code}")
        print(f"    Content-Type: {response.headers.get('Content-Type')}")
        print(f"    Tamanho: {len(response.text)} bytes")
        
        # Procura por indicadores de dados JSON no HTML
        indicators = {
            '__NEXT_DATA__': '__NEXT_DATA__' in response.text,
            'application/json': 'application/json' in response.text,
            'window.__INITIAL_STATE__': 'window.__INITIAL_STATE__' in response.text,
            'window.__DATA__': 'window.__DATA__' in response.text,
        }
        
        print(f"\n    Indicadores encontrados:")
        for indicator, found in indicators.items():
            status = "✓" if found else "✗"
            print(f"    {status} {indicator}")
        
        # Salva para análise manual
        with open('lauki_page_test.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\n    ✓ Página salva em: lauki_page_test.html")
        
        return response.text
        
    except Exception as e:
        print(f"    ✗ Erro: {str(e)}")
        return None

def test_graphql():
    """Testa se a API usa GraphQL"""
    print("\n" + "="*60)
    print("TESTE 3: GraphQL")
    print("="*60)
    
    graphql_endpoints = [
        "https://api.moltx.io/graphql",
        "https://moltx.io/api/graphql",
        "https://api.moltx.io/query",
    ]
    
    query = """
    query {
        user(username: "lauki") {
            username
            displayName
            followers
            following
            posts {
                id
                content
                createdAt
            }
        }
    }
    """
    
    for endpoint in graphql_endpoints:
        try:
            print(f"\n[*] Testando GraphQL: {endpoint}")
            response = requests.post(
                endpoint,
                json={'query': query},
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0'
                },
                timeout=5
            )
            print(f"    Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"    ✓ GraphQL encontrado!")
                return endpoint, response.json()
                
        except Exception as e:
            print(f"    ✗ Erro: {str(e)}")
    
    return None, None

def main():
    print("="*60)
    print("MOLTX - TESTE RÁPIDO DE CAPTURA DE DADOS")
    print("="*60)
    print("\nTestando diferentes métodos para acessar dados do @lauki\n")
    
    # Teste 1: API REST
    api_endpoint, api_data = test_direct_api()
    
    # Teste 2: HTML
    html_content = test_html_page()
    
    # Teste 3: GraphQL
    graphql_endpoint, graphql_data = test_graphql()
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    if api_endpoint:
        print(f"\n✓ API REST encontrada: {api_endpoint}")
        print(f"  Use este endpoint para capturar dados em JSON")
    else:
        print(f"\n✗ API REST não encontrada")
        print(f"  Os dados podem estar embutidos no HTML ou carregados via JS")
    
    if graphql_endpoint:
        print(f"\n✓ GraphQL encontrado: {graphql_endpoint}")
    else:
        print(f"\n✗ GraphQL não encontrado")
    
    if html_content:
        print(f"\n✓ Página HTML capturada")
        print(f"  Analise o arquivo 'lauki_page_test.html' para encontrar os dados")
    
    print("\n" + "="*60)
    print("PRÓXIMOS PASSOS")
    print("="*60)
    print("""
1. Analise os resultados acima
2. Se encontrou API REST, use o moltx_scraper.py
3. Se não encontrou API, use o moltx_browser_scraper.py
4. Ou analise manualmente o arquivo lauki_page_test.html
    """)

if __name__ == "__main__":
    main()
