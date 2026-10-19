"""
MoltX Browser Scraper - Usa Selenium para capturar dados carregados via JavaScript
"""

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium não instalado. Use: pip install selenium")

import json
import time
from datetime import datetime

class MoltXBrowserScraper:
    def __init__(self, headless=True):
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium não está instalado. Execute: pip install selenium")
        
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """Configura o Chrome driver"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Habilita logging de network
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def intercept_network_requests(self):
        """Captura todas as requisições de rede para encontrar a API"""
        logs = self.driver.get_log('performance')
        
        api_requests = []
        
        for entry in logs:
            try:
                log = json.loads(entry['message'])['message']
                
                if log['method'] == 'Network.responseReceived':
                    url = log['params']['response']['url']
                    
                    # Filtra apenas requisições da API
                    if 'api' in url.lower() or 'moltx.io' in url:
                        api_requests.append({
                            'url': url,
                            'method': log['params']['response'].get('method', 'GET'),
                            'status': log['params']['response']['status'],
                            'type': log['params']['response']['mimeType']
                        })
                        
            except (KeyError, json.JSONDecodeError):
                continue
        
        return api_requests
    
    def get_user_profile(self, username):
        """Acessa o perfil e captura os dados"""
        print(f"\n[*] Acessando perfil @{username} com browser")
        
        url = f"https://moltx.io/{username}"
        
        try:
            self.driver.get(url)
            print(f"    ✓ Página carregada: {url}")
            
            # Espera o conteúdo carregar
            time.sleep(3)
            
            # Captura requisições de rede
            print(f"\n[*] Analisando requisições de rede...")
            api_requests = self.intercept_network_requests()
            
            print(f"\n[+] Encontradas {len(api_requests)} requisições da API:")
            for req in api_requests:
                print(f"    - {req['method']} {req['url']}")
                print(f"      Status: {req['status']} | Type: {req['type']}")
            
            # Tenta extrair dados do LocalStorage/SessionStorage
            print(f"\n[*] Verificando LocalStorage...")
            local_storage = self.driver.execute_script("return window.localStorage;")
            print(f"    LocalStorage items: {len(local_storage)}")
            
            print(f"\n[*] Verificando SessionStorage...")
            session_storage = self.driver.execute_script("return window.sessionStorage;")
            print(f"    SessionStorage items: {len(session_storage)}")
            
            # Tenta pegar dados do estado da aplicação (React/Next.js)
            print(f"\n[*] Procurando dados do Next.js...")
            next_data = self.driver.execute_script("""
                const nextScript = document.getElementById('__NEXT_DATA__');
                if (nextScript) {
                    return JSON.parse(nextScript.textContent);
                }
                return null;
            """)
            
            if next_data:
                print(f"    ✓ Dados Next.js encontrados!")
            
            # Captura elementos da página
            print(f"\n[*] Extraindo elementos da página...")
            
            page_data = {
                'url': url,
                'title': self.driver.title,
                'api_requests': api_requests,
                'local_storage': local_storage,
                'session_storage': session_storage,
                'next_data': next_data,
                'html_length': len(self.driver.page_source)
            }
            
            # Tenta pegar posts
            try:
                posts_elements = self.driver.find_elements(By.CSS_SELECTOR, '[class*="post"], [class*="Post"], article')
                print(f"    Posts encontrados na página: {len(posts_elements)}")
                page_data['posts_count'] = len(posts_elements)
            except:
                pass
            
            return page_data
            
        except Exception as e:
            print(f"    ✗ Erro: {str(e)}")
            return None
    
    def save_screenshot(self, filename='lauki_screenshot.png'):
        """Salva screenshot da página"""
        try:
            self.driver.save_screenshot(filename)
            print(f"    ✓ Screenshot salvo: {filename}")
        except Exception as e:
            print(f"    ✗ Erro ao salvar screenshot: {str(e)}")
    
    def close(self):
        """Fecha o browser"""
        if self.driver:
            self.driver.quit()

def main():
    if not SELENIUM_AVAILABLE:
        print("\n" + "="*60)
        print("ERRO: Selenium não está instalado")
        print("="*60)
        print("\nPara instalar o Selenium:")
        print("  pip install selenium")
        print("\nVocê também precisa do ChromeDriver:")
        print("  https://chromedriver.chromium.org/downloads")
        return
    
    print("="*60)
    print("MOLTX BROWSER SCRAPER - Captura de dados via Browser")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    scraper = MoltXBrowserScraper(headless=False)  # headless=False para ver o browser
    
    try:
        print("[*] Iniciando Chrome...")
        scraper.setup_driver()
        print("    ✓ Chrome iniciado\n")
        
        # Captura dados do perfil
        profile_data = scraper.get_user_profile("lauki")
        
        # Salva screenshot
        scraper.save_screenshot()
        
        # Salva resultados
        if profile_data:
            with open('moltx_browser_results.json', 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            print("\n" + "="*60)
            print("RESULTADOS SALVOS")
            print("="*60)
            print("✓ moltx_browser_results.json - Dados capturados")
            print("✓ lauki_screenshot.png - Screenshot da página")
            
            # Mostra requisições da API encontradas
            if profile_data.get('api_requests'):
                print("\n" + "="*60)
                print("ENDPOINTS DA API ENCONTRADOS")
                print("="*60)
                for req in profile_data['api_requests']:
                    if req['status'] == 200:
                        print(f"✓ {req['method']} {req['url']}")
        
    except Exception as e:
        print(f"\n✗ Erro: {str(e)}")
    
    finally:
        print("\n[*] Fechando browser...")
        scraper.close()
        print("    ✓ Browser fechado\n")

if __name__ == "__main__":
    main()
