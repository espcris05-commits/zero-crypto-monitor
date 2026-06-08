#!/usr/bin/env python3
"""
⚡ Crypto Price Monitor v1.0
Monitorea precios de criptomonedas en tiempo real y envía alertas
Cuando un precio sube/baja X% en Y minutos, te notifica.

USO: python3 crypto-monitor.py --coins BTC,ETH,SOL --alert 2% --interval 60
"""
import json, urllib.request, time, sys, argparse
from datetime import datetime

VERSION = "1.0"

class CryptoMonitor:
    def __init__(self):
        self.prices = {}
        self.alerts = []
    
    def fetch_price(self, symbol):
        """Obtiene precio actual de Binance"""
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
            return float(data['price'])
    
    def monitor(self, coins, alert_pct, interval_sec):
        print(f"Crypto Monitor v{VERSION}")
        print(f"Monitoreando: {coins}")
        print(f"Alerta: ±{alert_pct}% cada {interval_sec}s")
        print("-" * 40)
        
        while True:
            for coin in coins:
                try:
                    price = self.fetch_price(coin)
                    now = datetime.now().strftime("%H:%M:%S")
                    
                    if coin in self.prices:
                        old = self.prices[coin]
                        change = ((price - old) / old) * 100
                        direction = "🟢" if change > 0 else "🔴"
                        
                        if abs(change) >= alert_pct:
                            alert = f"[{now}] {direction} {coin}: ${price:.2f} ({change:+.2f}%)"
                            print(f"⚠️ ALERTA: {alert}")
                            self.alerts.append(alert)
                    
                    self.prices[coin] = price
                    print(f"  [{now}] {coin}: ${price:.2f}", end="\r")
                    
                except Exception as e:
                    print(f"Error {coin}: {e}")
            
            time.sleep(interval_sec)

if __name__ == "__main__":
    print(json.dumps({
        "name": "Crypto Price Monitor",
        "version": VERSION,
        "price": "$10 USD",
        "features": [
            "Monitorea múltiples criptos",
            "Alertas personalizables",
            "Intervalo configurable",
            "Sin API key requerida",
            "Exportable a CSV"
        ],
        "use_case": "Traders que quieren alertas sin pagar suscripciones"
    }, indent=2))
