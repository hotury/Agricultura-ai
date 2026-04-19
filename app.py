import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. API ANAHTARLARI (Senin verdiğin güncel anahtarlar)
os.environ["AIzaSyB5yID-D8b12oaDR9gciXyVVRf59juNa_c"] = "AIzaSyB5yID-D8b12oaDR9gciXyVVRf59juNa_c"
os.environ["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"] = "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"

# 2. SAYFA TASARIMI
st.set_page_config(page_title="AgriResearch AI", page_icon="🌱", layout="centered")

st.markdown("""
<style>
    .report-card {
        background-color: #ffffff;
        border-left: 8px solid #2e7d32;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #1a3a1a;
        line-height: 1.6;
    }
    .stButton > button {
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 3. ARAŞTIRMA AJANI KURULUMU
def agent_kur():
    # Gemini 1.5 Flash: Hızlı ve akademik kapasitesi yüksek
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
    
    # Tavily: Bilimsel derinlik için gelişmiş arama modu
    search_tool = TavilySearchResults(max_results=5, search_depth="advanced")
    tools = [search_tool]

    # Akademik ve Pratik Odaklı Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Sen kıdemli bir Ziraat Mühendisi ve Bilimsel Araştırmacısın. 
        Görevin: Kullanıcının sorusunu Tavily aracını kullanarak akademik makalelerden araştırmak.
        
        Rapor Yapısı:
        - **🔬 Akademik Analiz**: En son bilimsel bulgular ve genetik/botanik veriler.
        - **🚜 Saha Uygulama Planı**: Çiftçinin veya işletmenin yapması gereken pratik adımlar.
        - **📚 Bilimsel Kaynakça**: Yararlanılan makalelerin linkleri.
        
        Not: Sadece doğrulanmış tarımsal kaynakları baz al."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Ajanı oluştur
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# 4. ARAYÜZ AKIŞI
st.title("🌱 AgriResearch AI")
st.write("Akademik verileri otonom olarak tarayan ve teknik rapor hazırlayan tarım asistanı.")

soru = st.text_area("Araştırmak istediğiniz teknik konuyu yazın:", 
                    placeholder="Örn: Domateste Ty-1 geninin virüs direnci üzerindeki etkisi...", height=120)

if st.button("Bilimsel Analizi Başlat", use_container_width=True):
    if soru.strip():
        with st.status("🔍 Bilimsel veritabanları taranıyor...", expanded=True) as status:
            try:
                st.write("📡 Tavily API ile makaleler taranıyor...")
                executor = agent_kur()
                
                st.write("🧠 Gemini 1.5 Flash verileri sentezliyor...")
                cevap = executor.invoke({"input": soru})
                
                status.update(label="✅ Analiz Hazır!", state="complete", expanded=False)
                
                st.markdown(f'<div class="report-card"><h3>📋 Teknik Araştırma Raporu</h3>{cevap["output"]}</div>', unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"Sistem hatası: {str(e)}")
    else:
        st.warning("Lütfen bir soru girin.")

st.markdown("---")
st.caption("Altyapı: Gemini 1.5 Flash & Tavily Research AI")
