import requests
import json
from datetime import datetime

class MoltXScraper:
    def __init__(self):
        self.base_url = "https://moltx.io"
        self.api_base = "https://api.moltx.io"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://moltx.io/',
            'Origin': 'https://moltx.io'
        }
    
    def get_user_profile(self, username):
        """Tenta pegar o perfil do usuário via API"""
        print(f"\n[*] Tentando buscar perfil: @{username}")
        
        # Tentativa 1: API direta
        endpoints = [
            f"{self.api_base}/users/{username}",
            f"{self.api_base}/api/users/{username}",
            f"{self.api_base}/v1/users/{username}",
            f"{self.api_base}/profile/{username}",
            f"{self.base_url}/api/users/{username}",
        ]
        
        for endpoint in endpoints:
            try:
                print(f"\n[+] Tentando endpoint: {endpoint}")
                response = requests.get(endpoint, headers=self.headers, timeout=10)
                print(f"    Status Code: {response.status_code}")
                print(f"    Content-Type: {response.headers.get('Content-Type', 'N/A')}")
                
                if response.status_code == 200:
                    # Tenta parsear como JSON
                    try:
                        data = response.json()
                        print(f"    ✓ JSON válido recebido!")
                        return {'endpoint': endpoint, 'data': data, 'type': 'json'}
                    except json.JSONDecodeError:
                        print(f"    ! Resposta não é JSON")
                        return {'endpoint': endpoint, 'data': response.text[:500], 'type': 'html'}
                        
            except requests.exceptions.RequestException as e:
                print(f"    ✗ Erro: {str(e)}")
        
        return None
    
    def get_user_posts(self, username, limit=20):
        """Tenta pegar os posts do usuário"""
        print(f"\n[*] Tentando buscar posts de @{username}")
        
        endpoints = [
            f"{self.api_base}/users/{username}/posts",
            f"{self.api_base}/api/users/{username}/posts?limit={limit}",
            f"{self.api_base}/posts?username={username}&limit={limit}",
            f"{self.base_url}/api/users/{username}/posts",
        ]
        
        for endpoint in endpoints:
            try:
                print(f"\n[+] Tentando endpoint: {endpoint}")
                response = requests.get(endpoint, headers=self.headers, timeout=10)
                print(f"    Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"    ✓ JSON válido recebido! ({len(data) if isinstance(data, list) else 'dict'} items)")
                        return {'endpoint': endpoint, 'data': data, 'type': 'json'}
                    except json.JSONDecodeError:
                        print(f"    ! Resposta não é JSON")
                        
            except requests.exceptions.RequestException as e:
                print(f"    ✗ Erro: {str(e)}")
        
        return None
    
    def scrape_html_page(self, username):
        """Faz scraping da página HTML e tenta extrair dados"""
        print(f"\n[*] Fazendo scraping da página HTML")
        
        url = f"{self.base_url}/{username}"
        
        try:
            print(f"[+] Acessando: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            print(f"    Status Code: {response.status_code}")
            print(f"    Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"    Tamanho da resposta: {len(response.text)} bytes")
            
            # Salva o HTML para análise
            with open('lauki_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"    ✓ HTML salvo em 'lauki_page.html'")
            
            # Procura por dados JSON embutidos no HTML
            if 'application/json' in response.text or '__NEXT_DATA__' in response.text:
                print(f"    ! Encontrado possível JSON embutido no HTML")
                
                # Tenta extrair JSON do Next.js
                import re
                json_pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
                matches = re.findall(json_pattern, response.text, re.DOTALL)
                
                if matches:
                    try:
                        next_data = json.loads(matches[0])
                        print(f"    ✓ Dados Next.js extraídos!")
                        return {'source': 'html_next_data', 'data': next_data, 'type': 'json'}
                    except json.JSONDecodeError:
                        print(f"    ✗ Erro ao parsear Next.js data")
            
            return {'source': 'html', 'data': response.text[:1000], 'type': 'html'}
            
        except requests.exceptions.RequestException as e:
            print(f"    ✗ Erro: {str(e)}")
            return None
    
    def analyze_network_requests(self):
        """Mostra informações sobre possíveis endpoints da API"""
        print("\n" + "="*60)
        print("ANÁLISE DE POSSÍVEIS ENDPOINTS DA API MOLTX")
        print("="*60)
        
        print("""
Baseado na estrutura comum de APIs de redes sociais, os endpoints
prováveis da MoltX podem ser:

1. Perfil do usuário:
   - GET /api/users/{username}
   - GET /api/profile/{username}
   
2. Posts do usuário:
   - GET /api/users/{username}/posts
   - GET /api/posts?author={username}
   
3. Seguindo/Seguidores:
   - GET /api/users/{username}/following
   - GET /api/users/{username}/followers
   
4. Stats de atividade:
   - GET /api/users/{username}/stats
   
5. Posts específicos:
   - GET /api/posts/{post_id}
        """)

def main():
    print("="*60)
    print("MOLTX SCRAPER - Análise de API e Dados")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    scraper = MoltXScraper()
    
    username = "lauki"
    
    # Tenta diferentes métodos
    print("\n\n### MÉTODO 1: API Endpoints ###")
    profile_data = scraper.get_user_profile(username)
    
    print("\n\n### MÉTODO 2: Posts via API ###")
    posts_data = scraper.get_user_posts(username)
    
    print("\n\n### MÉTODO 3: Scraping HTML ###")
    html_data = scraper.scrape_html_page(username)
    
    # Mostra análise de endpoints
    scraper.analyze_network_requests()
    
    # Salva resultados em arquivo
    results = {
        'timestamp': datetime.now().isoformat(),
        'username': username,
        'profile_data': profile_data,
        'posts_data': posts_data,
        'html_data': html_data if html_data and html_data.get('type') == 'json' else None
    }
    
    with open('moltx_scraper_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n\n" + "="*60)
    print("RESULTADOS SALVOS")
    print("="*60)
    print("✓ moltx_scraper_results.json - Dados em JSON")
    print("✓ lauki_page.html - Página HTML completa")
    print("\n")

if __name__ == "__main__":
    main()
