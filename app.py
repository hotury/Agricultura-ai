import streamlit as st
import os
from groq import Groq
from langchain_tavily import TavilySearch

# 1. API ANAHTARLARI
os.environ["TAVILY_API_KEY"] = "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"
GROQ_API_KEY = "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"

# 2. SAYFA TASARIMI
st.set_page_config(page_title="AgriResearch AI", page_icon="🌱")
st.title("🌱 AgriResearch AI")

# 3. ARAŞTIRMA FONKSİYONU
def arastirma_yap(soru):
    # Tavily ile ara
    search = TavilySearch(max_results=3)
    arama_sonucu = search.invoke(soru)

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

    # Groq ile yanıt üret
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

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
