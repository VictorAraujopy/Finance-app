import requests
from datetime import datetime
import pytz


def buscar_cotacoes():

    try:
        dolar = requests.get("https://economia.awesomeapi.com.br/json/USD-BRL")
        cota_dolar = dolar.json()
        valor_dolar = cota_dolar[0]["bid"]
        print(f"Dólar: R$ {float(valor_dolar):.2f}")


    except Exception as e:
        print(f"Erro ao buscar cot do dolar: {e}")

    try:
        btc = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl")
        cota_bitcoin = btc.json()
        valor_bitcoin = cota_bitcoin["bitcoin"]["brl"]
        print(f"Bitcoin: R$ {valor_bitcoin:,.2f}")

    except Exception as e:
        print(f"Erro ao buscar cot do btc: {e}")

    try:
        fuso = pytz.timezone("America/Sao_Paulo")
        hora = datetime.now(fuso).strftime("%d/%m/%Y %H:%M:%S")
        print(f"Data e Hora em Brasília: {hora}")
    except Exception as e:
        print(f"Erro ao buscar horario: {e}")


    return {
        "usd_brl": float(valor_dolar) if valor_dolar is not None else None,
        "btc_brl": valor_bitcoin if valor_bitcoin is not None else None,
        "updated_at": hora
    }

buscar_cotacoes()