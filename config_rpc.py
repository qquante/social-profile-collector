import os
"""
Configuração do RPC - Ankr Base Network
"""

# RPC Endpoints
ANKR_RPC_HTTP = os.environ.get("ANKR_RPC_HTTP", "")
ANKR_RPC_WSS = os.environ.get("ANKR_RPC_WSS", "")

# Contrato a monitorar
CONTRATO = "0xFb653a4061cE35b66e2Ba090Cf1Fabe32f294079"
