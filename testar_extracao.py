"""
Testa a extração de posts do HTML salvo
"""

import re

def extrair_posts(html):
    """Extrai posts do HTML"""
    posts = []
    pattern = r'<article class="post" data-post-href="(/post/([^"]+))">(.*?)</article>'
    matches = re.finditer(pattern, html, re.DOTALL)
    
    for match in matches:
        post_url = match.group(1)
        post_id = match.group(2)
        post_html = match.group(3)
        
        # Extrai conteúdo - tenta múltiplos métodos
        conteudo = ""
        
        # Método 1: content-full
        content_match = re.search(r'<div class="content content-full">(.*?)</div>', post_html, re.DOTALL)
        if content_match:
            conteudo = content_match.group(1)
        
        # Método 2: content sem full
        if not conteudo:
            content_match = re.search(r'<div class="content"[^>]*>(.*?)</div>', post_html, re.DOTALL)
            if content_match:
                conteudo = content_match.group(1)
        
        # Método 3: content-preview
        if not conteudo:
            content_match = re.search(r'<div class="content content-preview">(.*?)</div>', post_html, re.DOTALL)
            if content_match:
                conteudo = content_match.group(1)
        
        # Limpa HTML do conteúdo
        if conteudo:
            conteudo = re.sub(r'<br\s*/?>', '\n', conteudo)
            conteudo = re.sub(r'<a[^>]*>', '', conteudo)
            conteudo = re.sub(r'</a>', '', conteudo)
            conteudo = re.sub(r'<[^>]+>', '', conteudo)
            conteudo = re.sub(r'&#039;', "'", conteudo)
            conteudo = re.sub(r'&quot;', '"', conteudo)
            conteudo = re.sub(r'&lt;', '<', conteudo)
            conteudo = re.sub(r'&gt;', '>', conteudo)
            conteudo = re.sub(r'&amp;', '&', conteudo)
            conteudo = '\n'.join(line.strip() for line in conteudo.split('\n') if line.strip())
        
        # Extrai tempo
        tempo_match = re.search(r'<span class="timestamp"[^>]*>(.*?)</span>', post_html)
        tempo = tempo_match.group(1) if tempo_match else "agora"
        
        posts.append({
            'id': post_id,
            'url': f'https://moltx.io{post_url}',
            'conteudo': conteudo if conteudo else "[Conteúdo vazio]",
            'tempo': tempo
        })
    
    return posts

def main():
    print("="*70)
    print("TESTE DE EXTRAÇÃO DE POSTS")
    print("="*70)
    print()
    
    # Lê HTML
    try:
        print("[1/2] Lendo HTML...")
        with open('lauki_page_test.html', 'r', encoding='utf-8') as f:
            html = f.read()
        print(f"    ✓ HTML lido ({len(html):,} bytes)")
    except FileNotFoundError:
        print("    ✗ Arquivo lauki_page_test.html não encontrado!")
        print("      Execute primeiro: py quick_test.py")
        input("\nPressione Enter para sair...")
        return
    
    # Extrai posts
    print("\n[2/2] Extraindo posts...")
    posts = extrair_posts(html)
    print(f"    ✓ {len(posts)} posts extraídos")
    
    # Mostra os 5 primeiros
    print("\n" + "="*70)
    print(f"ÚLTIMOS 5 POSTS EXTRAÍDOS:")
    print("="*70)
    
    for i, post in enumerate(posts[:5], 1):
        print(f"\n[POST #{i}]")
        print(f"ID: {post['id']}")
        print(f"Tempo: {post['tempo']}")
        print(f"URL: {post['url']}")
        print(f"\nConteúdo ({len(post['conteudo'])} caracteres):")
        print("-" * 70)
        
        # Mostra preview
        preview = post['conteudo'][:200]
        if len(post['conteudo']) > 200:
            preview += "..."
        print(preview)
        print("-" * 70)
    
    # Estatísticas
    print("\n" + "="*70)
    print("ESTATÍSTICAS:")
    print("="*70)
    
    posts_com_conteudo = sum(1 for p in posts if p['conteudo'] and p['conteudo'] != "[Conteúdo vazio]")
    posts_vazios = len(posts) - posts_com_conteudo
    
    print(f"\nTotal de posts: {len(posts)}")
    print(f"Com conteúdo: {posts_com_conteudo} ({posts_com_conteudo/len(posts)*100:.1f}%)")
    print(f"Vazios: {posts_vazios} ({posts_vazios/len(posts)*100:.1f}%)")
    
    tamanho_medio = sum(len(p['conteudo']) for p in posts) / len(posts) if posts else 0
    print(f"Tamanho médio: {tamanho_medio:.0f} caracteres")
    
    if posts_vazios > 0:
        print(f"\n⚠️  ATENÇÃO: {posts_vazios} posts sem conteúdo extraído")
        print("   Isso pode afetar o monitor de posts novos")
    else:
        print(f"\n✅ PERFEITO! Todos os posts foram extraídos com sucesso")
    
    print("\n" + "="*70)
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
