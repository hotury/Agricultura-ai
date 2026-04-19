import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. API ANAHTARLARI (Senin verdiğin anahtarlar eklendi)
os.environ["GOOGLE_API_KEY"] = "AIzaSyB5yID-D8b12oaDR9gciXyVVRf59juNa_c"
os.environ["TAVILY_API_KEY"] = "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"

# 2. SAYFA TASARIMI VE STİL
st.set_page_config(page_title="AgriResearch AI", page_icon="🌱", layout="centered")

st.markdown("""
<style>
    .report-card {
        background-color: #ffffff;
        border-left: 6px solid #2e7d32;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# 3. YAPAY ZEKA VE AJAN KURULUMU
def asistan_olustur():
    # Gemini 1.5 Flash: Cömert kota ve yüksek hız
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
    
    # Tavily Research Modu: Akademik odaklı arama
    search_tool = TavilySearchResults(max_results=5, search_depth="advanced")
    tools = [search_tool]

    # Akademik ve Pratik Odaklı Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Sen uzman bir tarım bilimcisi ve akademik araştırmacısın. 
        Görevin: Kullanıcının sorusunu bilimsel kaynaklar üzerinden tarayıp analiz etmek.
        Yapı:
        1. Bilimsel Özet: Konuyla ilgili en son akademik bulgular.
        2. Pratik Öneri: Çiftçinin sahada uygulayabileceği net tavsiyeler.
        3. Kaynaklar: Yararlandığın makalelerin linkleri.
        Not: Sadece doğrulanmış ve bilimsel kaynakları ciddiye al."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# 4. ARAYÜZ AKIŞI
st.title("🌱 AgriResearch AI")
st.caption("Akademik Bilgi ile Tarla Arasındaki Bilgi Köprüsü")

soru = st.text_area("Hangi tarımsal konuyu araştırmamı istersiniz?", 
                    placeholder="Örn: Domateste Ty-1 geni ve virüs direnci...", height=100)

if st.button("Analizi Başlat", use_container_width=True):
    if soru:
        with st.status("🔍 Bilimsel veriler taranıyor...", expanded=True) as status:
            st.write("📡 Akademik veritabanlarına bağlanılıyor (Tavily)...")
            executor = asistan_olustur()
            
            st.write("🧠 Gemini 1.5 Flash verileri analiz ediyor...")
            cevap = executor.invoke({"input": soru})
            
            status.update(label="✅ Araştırma Tamamlandı!", state="complete", expanded=False)
        
        st.markdown(f'<div class="report-card">{cevap["output"]}</div>', unsafe_allow_html=True)
    else:
        st.warning("Lütfen bir soru girin.")
