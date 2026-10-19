"""
Teste completo da integração com Telegram
"""

from telegram_bot import TelegramBot

def main():
    print("="*70)
    print("📱 TESTE COMPLETO - TELEGRAM BOT")
    print("="*70)
    print()
    
    bot = TelegramBot()
    
    # Teste 1: Verificar bot
    print("[1/3] Testando bot...")
    sucesso, msg = bot.testar_bot()
    print(f"    {'✅' if sucesso else '❌'} {msg}")
    
    if not sucesso:
        print("\n❌ Bot não está funcionando!")
        print("   Verifique o token em config_telegram.py")
        input("\nPressione Enter para sair...")
        return
    
    # Teste 2: Testar chat
    print("\n[2/3] Testando envio para chat...")
    sucesso, msg = bot.testar_chat()
    print(f"    {'✅' if sucesso else '❌'} {msg}")
    
    if not sucesso:
        print("\n❌ Não conseguiu enviar para o chat!")
        print("   Verifique o CHAT_ID em config_telegram.py")
        print("   Certifique-se de que o bot foi adicionado ao grupo/canal")
        input("\nPressione Enter para sair...")
        return
    
    # Teste 3: Simular post
    print("\n[3/3] Testando formatação de post...")
    
    post_teste = {
        'id': 'test-123-abc',
        'tempo': '2m',
        'url': 'https://moltx.io/post/test-123-abc',
        'conteudo': '''just bought $AGENT at 0x1234567890123456789012345678901234567890

trading with 50k usdc. moon or zero. no in between.

also watching 0xabcdefabcdefabcdefabcdefabcdefabcdefabcd'''
    }
    
    mensagem = bot.formatar_post_novo(post_teste)
    sucesso, resultado = bot.enviar_mensagem(mensagem)
    
    print(f"    {'✅' if sucesso else '❌'} {resultado}")
    
    if sucesso:
        print("\n" + "="*70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("="*70)
        print("\n🎯 O bot está funcionando perfeitamente!")
        print("\nVocê deve ter recebido 2 mensagens no Telegram:")
        print("  1. Mensagem de teste")
        print("  2. Post simulado com 2 contract addresses")
        print("\nAgora você pode usar:")
        print("  python monitor.py - Para monitorar posts do @lauki")
    else:
        print("\n⚠️  Houve um problema no envio do post")
        print(f"   Erro: {resultado}")
    
    print("\n" + "="*70)
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
