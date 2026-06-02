# ⚡ High-Frequency E-Commerce Tracker (Real-Time ETL)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

Um motor de Extração, Transformação e Carregamento (ETL) construído para inteligência de mercado no setor de e-commerce. Esta aplicação realiza varreduras em tempo real em catálogos de varejo, contornando firewalls avançados (WAFs) para fornecer metrologia financeira e precificação competitiva de forma automatizada.

## 🎯 Visão Estratégica

No mercado de tecnologia e e-commerce corporativo, a flutuação de preço é agressiva e a margem de lucro depende do tempo de reação. Projetos de raspagem tradicionais falham devido a bloqueios militares (como Datadome e Cloudflare). 

Este produto resolve esse problema implementando uma arquitetura **Nível 3 (Headful Browser Automation)**, sequestrando o binário nativo do Microsoft Edge via Playwright para simular latência humana, burlar inteligências artificiais de defesa e extrair dados de altíssima liquidez (como periféricos de alta performance e monitores).

## ⚙️ Arquitetura do Sistema

O pipeline opera em três frentes assíncronas:

1. **Extract (Motor Furtivo):** Utiliza `Playwright Async` para forjar a assinatura criptográfica de um navegador humano (SSL Handshake), rolagem autônoma de página e extração limpa da árvore DOM.
2. **Transform (Higienização):** Sanitização de anomalias HTML, tratamento de strings e conversão algorítmica de moeda bruta para matriz de pontos flutuantes em Reais (BRL) usando `Pandas`.
3. **Load (Dashboard Render):** Carregamento em memória e renderização instantânea via `Streamlit`, plotando flutuação de mercado, cálculos de preço médio e links de prateleira diretos.

## 🚀 Instalação e Execução

### Pré-requisitos
* Python 3.10 ou superior.
* Navegador Microsoft Edge nativo instalado no sistema operacional.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/ecommerce-tracker-etl.git](https://github.com/SEU_USUARIO/ecommerce-tracker-etl.git)
   cd ecommerce-tracker-etl
