import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

class EcommerceScraper:
    def __init__(self):
        self.base_url = "https://webscraper.io/test-sites/e-commerce/allinone/computers"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.raw_data = []

    def fetch_page(self):
        print("[REDE] Redirecionando motor para ambiente de homologacao de hardware...")
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                print("[REDE] Acesso concedido sem bloqueios. Analisando DOM...")
                return response.text
            else:
                print(f"[FALHA] Codigo: {response.status_code}")
                return None
        except Exception as e:
            print(f"[ERRO DE I/O] {e}")
            return None

    def parse_html(self, html_content: str):
        soup = BeautifulSoup(html_content, "html.parser")
        products = soup.find_all("div", class_="thumbnail")

        print(f"[PROCESSAMENTO] {len(products)} blocos de hardware detectados. Iniciando sanitizacao de dados...")
        
        for item in products:
            try:
                title_node = item.find("a", class_="title")
                price_node = item.find("h4", class_="price")
                desc_node = item.find("p", class_="description")
                
                if title_node and price_node:
                    title = title_node.get("title") or title_node.text.strip()
                    raw_price = price_node.text.replace("$", "").strip()
                    price = float(raw_price)
                    desc = desc_node.text.strip() if desc_node else "N/A"
                    
                    self.raw_data.append({
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Equipamento": title,
                        "Preço (USD)": price,
                        "Especificacao": desc
                    })
            except Exception:
                continue

    def export_to_csv(self, filename: str):
        if not self.raw_data:
            print("[ALERTA] Falha na extracao de hardware.")
            return
            
        df = pd.DataFrame(self.raw_data)
        df.to_csv(filename, index=False, sep=";", encoding="utf-8-sig")
        print("-" * 60)
        print(f"[SUCESSO] Pipeline concluido. Dataset gerado: {filename}")
        print(f"[METRICAS] Total de registros higienizados: {len(df)}")
        print("-" * 60)

if __name__ == "__main__":
    scraper = EcommerceScraper()
    html = scraper.fetch_page()
    if html:
        scraper.parse_html(html)
        scraper.export_to_csv("telemetria_hardware.csv")