"""
Testa o apito de 888 Hz por 888 ms
"""

import winsound
import time

print("="*60)
print("🔊 TESTE DE APITO")
print("="*60)
print("\nApitando 8x com 888 Hz por 888 ms cada...\n")

for i in range(8):
    print(f"🔊 Apito {i+1}/8...")
    try:
        winsound.Beep(888, 888)  # 888 Hz por 888 ms
        time.sleep(0.1)  # Pequena pausa
    except Exception as e:
        print(f"ERRO: {e}")

print("\n✅ Teste concluído!")
print("="*60)
input("\nPressione Enter para sair...")
