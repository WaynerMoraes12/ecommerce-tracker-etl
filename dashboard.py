import streamlit as st
import asyncio
import pandas as pd
from playwright.async_api import async_playwright

st.set_page_config(page_title="High-Frequency E-Commerce Tracker", layout="wide", initial_sidebar_state="collapsed")

async def rastreador_furtivo(alvo: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="msedge", slow_mo=50)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        url = f"https://lista.mercadolivre.com.br/{alvo.replace(' ', '-')}"
        
        try:
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            await page.mouse.wheel(0, 1500)
            await page.wait_for_timeout(3500)
            
            locator_str = ".poly-card__content, .ui-search-layout__item"
            await page.wait_for_selector(locator_str, timeout=15000)
            elements = await page.query_selector_all(locator_str)
            
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
                return pd.DataFrame(raw_data)
            return None
        except Exception:
            return None
        finally:
            await browser.close()

st.title("⚡ Data Intelligence: E-Commerce Tracker (Real-Time MVP)")
st.markdown("Motor ETL Híbrido (Playwright + Streamlit) com evasão de firewall e metrologia de prateleira em tempo real.")
st.markdown("---")

search_query = st.text_input("Defina o Alvo de Busca Tática (Ex: iPhone 15, RTX 4060, Violão Tagima):", "monitor 144hz")

if st.button("Iniciar Varredura Tática"):
    with st.spinner("Infiltrando no perímetro e processando matriz de metrologia..."):
        try:
            df = asyncio.run(rastreador_furtivo(search_query))
            
            if df is not None and not df.empty:
                col1, col2, col3 = st.columns(3)
                col1.metric("Ativos Mapeados", len(df))
                col2.metric("Menor Preço", f"R$ {df['Preço (BRL)'].min():.2f}")
                col3.metric("Preço Médio", f"R$ {df['Preço (BRL)'].mean():.2f}")
                
                st.markdown("### Flutuação de Valores do Mercado (BRL)")
                st.bar_chart(df.set_index("Equipamento")["Preço (BRL)"])
                
                st.markdown("### Matriz de Dados Higienizada (Exportável)")
                st.dataframe(df, use_container_width=True, column_config={
                    "URL": st.column_config.LinkColumn("Link de Compra")
                })
            else:
                st.warning("Escudo ativo, anomalia de input ou mutação estrutural. Nenhum dado higienizado.")
        except Exception as e:
            st.error(f"Erro Crítico de Execução Assíncrona: {e}")