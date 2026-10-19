"""
Extrai dados estruturados do HTML do MoltX
"""

import json
import re
from datetime import datetime

def extrair_perfil(html):
    """Extrai informações do perfil"""
    perfil = {}
    
    # Nome
    match = re.search(r'<div class="profile-name">(.*?)<span class="verified-badge">', html, re.DOTALL)
    if match:
        perfil['nome'] = match.group(1).strip()
    
    # Handle
    match = re.search(r'<div class="profile-handle">@(\w+)</div>', html)
    if match:
        perfil['handle'] = match.group(1)
    
    # Bio
    match = re.search(r'<div class="profile-bio">(.*?)</div>', html, re.DOTALL)
    if match:
        perfil['bio'] = match.group(1).strip()
    
    # Joined
    match = re.search(r'Joined (\d+\w+)</span>', html)
    if match:
        perfil['criado'] = match.group(1)
    
    # Twitter
    match = re.search(r'<a href="https://x\.com/(\w+)"', html)
    if match:
        perfil['twitter'] = match.group(1)
    
    # Following/Followers
    match = re.search(r'<span class="profile-stat-num">(\d+)</span><span class="profile-stat-label">Following</span>', html)
    if match:
        perfil['seguindo'] = int(match.group(1))
    
    match = re.search(r'<span class="profile-stat-num">(\d+)</span><span class="profile-stat-label">Followers</span>', html)
    if match:
        perfil['seguidores'] = int(match.group(1))
    
    # Total de posts
    match = re.search(r'<div style="font-size:13px;.*?>(\d+) posts</div>', html)
    if match:
        perfil['total_posts'] = int(match.group(1))
    
    return perfil

def extrair_posts(html):
    """Extrai todos os posts"""
    posts = []
    
    # Encontra todos os artigos de post
    pattern = r'<article class="post" data-post-href="(/post/[^"]+)">(.*?)</article>'
    matches = re.finditer(pattern, html, re.DOTALL)
    
    for match in matches:
        post_url = match.group(1)
        post_html = match.group(2)
        
        post = {
            'id': post_url.split('/')[-1],
            'url': f'https://moltx.io{post_url}'
        }
        
        # Autor
        autor_match = re.search(r'<a class="display-name" href="/(\w+)"[^>]*>(.*?)</a>', post_html)
        if autor_match:
            post['autor_handle'] = autor_match.group(1)
            post['autor_nome'] = autor_match.group(2)
        
        # Tempo
        tempo_match = re.search(r'<span class="timestamp"[^>]*>(.*?)</span>', post_html)
        if tempo_match:
            post['tempo'] = tempo_match.group(1)
        
        # Conteúdo (pega o content-full se existir, senão pega content)
        content_match = re.search(r'<div class="content content-full">(.*?)</div>', post_html, re.DOTALL)
        if not content_match:
            content_match = re.search(r'<div class="content(?:\s+content-preview)?">(.*?)</div>', post_html, re.DOTALL)
        
        if content_match:
            content = content_match.group(1)
            # Remove tags HTML básicas mas mantém o texto
            content = re.sub(r'<a href="[^"]*"[^>]*>', '', content)
            content = re.sub(r'</a>', '', content)
            content = re.sub(r'<br\s*/?>', '\n', content)
            content = re.sub(r'&#039;', "'", content)
            content = re.sub(r'&quot;', '"', content)
            content = re.sub(r'&lt;', '<', content)
            content = re.sub(r'&gt;', '>', content)
            content = re.sub(r'&amp;', '&', content)
            post['conteudo'] = content.strip()
        
        # Hashtags
        hashtags = re.findall(r'#(\w+)', post_html)
        if hashtags:
            post['hashtags'] = list(set(hashtags))
        
        # Estatísticas
        replies_match = re.search(r'title="View replies"[^>]*>\s*<span[^>]*>.*?</span>\s*<span>(\d+)</span>', post_html, re.DOTALL)
        if replies_match:
            post['respostas'] = int(replies_match.group(1))
        
        likes_match = re.search(r'title="View likes"[^>]*>\s*<span[^>]*>.*?</span>\s*<span>(\d+)</span>', post_html, re.DOTALL)
        if likes_match:
            post['curtidas'] = int(likes_match.group(1))
        
        views_match = re.search(r'title="Views"[^>]*>\s*<span[^>]*>.*?</span>\s*<span>([\d,]+)</span>', post_html, re.DOTALL)
        if views_match:
            views = views_match.group(1).replace(',', '')
            post['visualizacoes'] = int(views)
        
        # Reposts
        reposts_match = re.search(r'class="action-btn repost"[^>]*>\s*<span[^>]*>.*?</span>\s*<span>(\d+)</span>', post_html, re.DOTALL)
        if reposts_match:
            post['reposts'] = int(reposts_match.group(1))
        
        # Imagem (se tiver)
        img_match = re.search(r'<img[^>]+src="(https://cdn\.moltx\.io/[^"]+)"', post_html)
        if img_match:
            post['imagem'] = img_match.group(1)
        
        posts.append(post)
    
    return posts

def main():
    print("="*60)
    print("EXTRAÇÃO DE DADOS - MoltX @lauki")
    print("="*60)
    print()
    
    # Lê o arquivo HTML
    print("[1/3] Lendo HTML...")
    try:
        with open('lauki_page_test.html', 'r', encoding='utf-8') as f:
            html = f.read()
        print(f"    ✓ HTML lido ({len(html)} bytes)")
    except FileNotFoundError:
        print("    ✗ Arquivo lauki_page_test.html não encontrado!")
        print("      Execute primeiro: py quick_test.py")
        return
    
    # Extrai perfil
    print("\n[2/3] Extraindo dados do perfil...")
    perfil = extrair_perfil(html)
    print(f"    ✓ Perfil extraído:")
    print(f"      - Nome: {perfil.get('nome', 'N/A')}")
    print(f"      - Handle: @{perfil.get('handle', 'N/A')}")
    print(f"      - Seguidores: {perfil.get('seguidores', 0)}")
    print(f"      - Seguindo: {perfil.get('seguindo', 0)}")
    print(f"      - Total de posts: {perfil.get('total_posts', 0)}")
    
    # Extrai posts
    print("\n[3/3] Extraindo posts...")
    posts = extrair_posts(html)
    print(f"    ✓ {len(posts)} posts extraídos")
    
    # Estatísticas dos posts
    total_curtidas = sum(p.get('curtidas', 0) for p in posts)
    total_views = sum(p.get('visualizacoes', 0) for p in posts)
    total_respostas = sum(p.get('respostas', 0) for p in posts)
    
    print(f"\n    Estatísticas totais:")
    print(f"      - Curtidas: {total_curtidas}")
    print(f"      - Visualizações: {total_views:,}")
    print(f"      - Respostas: {total_respostas}")
    
    # Mostra preview de alguns posts
    print(f"\n    Preview dos 3 últimos posts:")
    for i, post in enumerate(posts[:3], 1):
        conteudo = post.get('conteudo', '')[:80] + '...' if len(post.get('conteudo', '')) > 80 else post.get('conteudo', '')
        print(f"\n    [{i}] {post.get('tempo', 'N/A')}")
        print(f"        {conteudo}")
        print(f"        💬 {post.get('respostas', 0)}  ❤️ {post.get('curtidas', 0)}  👁️ {post.get('visualizacoes', 0)}")
    
    # Monta estrutura final
    dados = {
        'extraido_em': datetime.now().isoformat(),
        'perfil': perfil,
        'posts': posts,
        'estatisticas': {
            'total_posts': len(posts),
            'total_curtidas': total_curtidas,
            'total_visualizacoes': total_views,
            'total_respostas': total_respostas
        }
    }
    
    # Salva em JSON
    print(f"\n{'='*60}")
    print("SALVANDO DADOS...")
    print("="*60)
    
    filename = 'lauki_dados.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Dados salvos em: {filename}")
    print(f"✓ Total de posts: {len(posts)}")
    print(f"✓ Tamanho do arquivo: {len(json.dumps(dados, ensure_ascii=False)) // 1024}KB")
    
    # Também salva uma versão bonita só com os posts
    filename_posts = 'lauki_posts_simples.json'
    with open(filename_posts, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Posts salvos separadamente em: {filename_posts}")
    
    print(f"\n{'='*60}")
    print("PRONTO! Dados extraídos com sucesso!")
    print("="*60)
    print(f"\nVocê pode:")
    print(f"  1. Abrir {filename} para ver todos os dados")
    print(f"  2. Abrir {filename_posts} para ver só os posts")
    print(f"  3. Usar esses dados em outros scripts Python")
    print()

if __name__ == "__main__":
    main()
