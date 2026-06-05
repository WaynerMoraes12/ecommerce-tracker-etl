import streamlit as st
import asyncio
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from playwright.async_api import async_playwright

st.set_page_config(page_title="High-Frequency E-Commerce Tracker", layout="wide", initial_sidebar_state="collapsed")

DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "123"
DB_NAME = "ecommerce_db"
DB_PORT = "5432"

def injetar_no_banco(df):
    try:
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, port=DB_PORT)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
        cursor.close()
        conn.close()

        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, port=DB_PORT)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetria_mercado (
                id SERIAL PRIMARY KEY,
                equipamento TEXT,
                preco NUMERIC(10, 2),
                url TEXT,
                data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        dados = [(row['Equipamento'], row['Preço (BRL)'], row['URL']) for _, row in df.iterrows()]
        query = "INSERT INTO telemetria_mercado (equipamento, preco, url) VALUES %s"
        execute_values(cursor, query, dados)
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro de persistência SQL: {e}")
        return False

async def rastreador_furtivo(alvo: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, 
            channel="msedge", 
            slow_mo=50,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        url = f"https://lista.mercadolivre.com.br/{alvo.replace(' ', '-')}"
        
        try:
            await page.goto(url, timeout=90000, wait_until="domcontentloaded")
            
            locator_str = ".poly-card__content, .ui-search-layout__item"
            
            try:
                await page.wait_for_selector(locator_str, timeout=10000)
            except Exception:
                st.warning("⚠️ Escudo Detectado! O sistema entrou em suspensão tática. Resolva o CAPTCHA manualmente no navegador agora.")
                await page.wait_for_selector(locator_str, timeout=90000)
            
            await page.mouse.wheel(0, 1500)
            await page.wait_for_timeout(3500)
            
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

st.title("⚡ Data Intelligence: E-Commerce Tracker (Enterprise Mode)")
st.markdown("Motor ETL Híbrido com automação Playwright e persistência relacional estrita em PostgreSQL.")
st.markdown("---")

search_query = st.text_input("Defina o Alvo de Busca Tática:", "monitor 144hz")

if st.button("Iniciar Varredura Tática"):
    with st.spinner("Infiltrando no perímetro e processando matriz de dados..."):
        try:
            df = asyncio.run(rastreador_furtivo(search_query))
            
            if df is not None and not df.empty:
                if injetar_no_banco(df):
                    st.success("Matriz de dados integrada ao PostgreSQL com sucesso!")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Ativos Mapeados", len(df))
                col2.metric("Menor Preço", f"R$ {df['Preço (BRL)'].min():.2f}")
                col3.metric("Preço Médio", f"R$ {df['Preço (BRL)'].mean():.2f}")
                
                st.markdown("### Flutuação de Valores do Mercado (BRL)")
                st.bar_chart(df.set_index("Equipamento")["Preço (BRL)"])
                
                st.markdown("### Matriz de Dados Higienizada (Visualização Local)")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Nenhum dado pôde ser higienizado nesta varredura.")
        except Exception as e:
            st.error(f"Erro Crítico de Execução: {e}")