import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage

# 1. API ANAHTARLARI
os.environ["TAVILY_API_KEY"] = "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"
OPENROUTER_API_KEY = "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"

# 2. SAYFA TASARIMI
st.set_page_config(page_title="AgriResearch AI", page_icon="🌱")
st.title("🌱 AgriResearch AI")

# 3. ARAŞTIRMA FONKSİYONU
def arastirma_yap(soru):
    llm = ChatOpenAI(
        model="mistralai/mistral-7b-instruct:free",
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.2
    )

    search = TavilySearch(max_results=3)
    arama_sonucu = search.invoke(soru)

    # Sonuç string mi liste mi kontrol et
    if isinstance(arama_sonucu, str):
        context = arama_sonucu
    elif isinstance(arama_sonucu, list):
        context = "\n\n".join([
            f"Kaynak: {r.get('url','')}\n{r.get('content','')}"
            if isinstance(r, dict) else str(r)
            for r in arama_sonucu
        ])
    else:
        context = str(arama_sonucu)

    prompt = f"""Sen uzman bir ziraat mühendisisin.
Aşağıdaki araştırma sonuçlarını kullanarak soruyu Türkçe yanıtla ve kaynak ver.

Soru: {soru}

Araştırma Sonuçları:
{context}

Yanıt:"""

    yanit = llm.invoke([HumanMessage(content=prompt)])
    return yanit.content

# 4. ARAYÜZ
query = st.text_input("Araştırmak istediğiniz konu:")

if st.button("Analiz Et"):
    if query:
        with st.status("🔍 İşleniyor...", expanded=True):
            try:
                sonuc = arastirma_yap(query)
                st.markdown(f"### Rapor\n{sonuc}")
            except Exception as e:
                st.error(f"Hata detayı: {str(e)}")
    else:
        st.warning("Lütfen bir soru girin.")
