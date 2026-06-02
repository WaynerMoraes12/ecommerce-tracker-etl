import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def rastreador_furtivo(alvo: str):
    print(f"[SISTEMA] Iniciando Motor de Incursão Visível. Alvo: {alvo}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="msedge", slow_mo=50)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        url = f"https://lista.mercadolivre.com.br/{alvo.replace(' ', '-')}"
        print(f"[REDE] Infiltrando no perímetro: {url}")
        
        try:
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            
            await page.mouse.wheel(0, 1500)
            await page.wait_for_timeout(3500)
            
            locator_str = ".poly-card__content, .ui-search-layout__item"
            await page.wait_for_selector(locator_str, timeout=15000)
            elements = await page.query_selector_all(locator_str)
            
            print(f"[PROCESSAMENTO] {len(elements)} blocos isolados. Iniciando extração limpa...")
            
            raw_data = []
            for item in elements[:20]:
                try:
                    title_el = await item.query_selector("h2, h3, .poly-component__title")
                    price_el = await item.query_selector(".andes-money-amount__fraction")
                    link_el = await item.query_selector("a[href]")
                    
                    if title_el and price_el and link_el:
                        title = await title_el.inner_text()
                        price_text = await price_el.inner_text()
                        link = await link_el.get_attribute("href")
                        
                        price = float(price_text.replace(".", "").replace(",", "."))
                        
                        raw_data.append({
                            "Equipamento": title.strip(),
                            "Preço (BRL)": price,
                            "URL": link
                        })
                except Exception:
                    continue
            
            if raw_data:
                df = pd.DataFrame(raw_data)
                df.to_csv("telemetria_mercado.csv", index=False, sep=";", encoding="utf-8-sig")
                print("-" * 60)
                print(f"[SUCESSO] Operação furtiva concluída. Dataset salvo: telemetria_mercado.csv")
                print(f"[MÉTRICAS] Menor Preço Encontrado: R$ {df['Preço (BRL)'].min():.2f}")
                print("-" * 60)
            else:
                print("[ALERTA] Mutação estrutural profunda. As tags alvo não foram localizadas.")
                
        except Exception as e:
            print(f"[ERRO DE I/O] Interceptação de rede falhou: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(rastreador_furtivo("monitor 144hz"))