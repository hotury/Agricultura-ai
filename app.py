import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. API ANAHTARLARI (Senin paylaştığın güncel anahtarlar)
os.environ["GOOGLE_API_KEY"] = "AIzaSyB5yID-D8b12oaDR9gciXyVVRf59juNa_c"
os.environ["TAVILY_API_KEY"] = "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"

# 2. SAYFA AYARLARI VE GÖRSEL TASARIM
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
        line-height: 1.6;
    }
    .stButton > button {
        background-color: #2e7d32;
        color: white;
        height: 3em;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. ARAŞTIRMACI AJAN KURULUMU
def asistan_hazirla():
    # Gemini 1.5 Flash: Hızlı ve cömert ücretsiz kota kullanımı
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
    
    # Tavily Search: Gelişmiş akademik arama modu
    search_tool = TavilySearchResults(max_results=5, search_depth="advanced")
    tools = [search_tool]

    # Sistem Talimatı (Prompt)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Sen kıdemli bir Ziraat Mühendisi ve Akademik Araştırmacısın. 
        Görevin: Kullanıcının sorusunu bilimsel makaleler ve güncel tarım raporları üzerinden taramak.
        
        Yanıt Yapısı:
        - **🔬 Bilimsel Analiz**: Konuyla ilgili akademik bulgular.
        - **🚜 Saha Önerileri**: Çiftçiler için pratik uygulama adımları.
        - **📚 Kaynakça**: Yararlanılan makale linkleri.
        
        Dilin profesyonel, güvenilir ve anlaşılır olsun."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Ajanı oluşturma
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# 4. KULLANICI ARAYÜZÜ
st.title("🌱 AgriResearch AI")
st.write("Akademik verileri tarla pratiklerine dönüştüren otonom araştırma sistemi.")

user_input = st.text_area("Araştırmak istediğiniz tarımsal konuyu yazın:", 
                          placeholder="Örn: Domateste Ty-1 geninin virüs direncine etkisi...", height=120)

if st.button("Analizi Başlat", use_container_width=True):
    if user_input.strip():
        with st.status("🔍 Veriler işleniyor...", expanded=True) as status:
            try:
                st.write("📡 Akademik kaynaklar taranıyor (Tavily)...")
                agent_executor = asistan_hazirla()
                
                st.write("🧠 Gemini 1.5 Flash verileri analiz ediyor...")
                response = agent_executor.invoke({"input": user_input})
                
                status.update(label="✅ Analiz Tamamlandı!", state="complete", expanded=False)
                
                # Şık rapor çıktısı
                st.markdown(f'<div class="report-card"><h3>📋 Araştırma Raporu</h3>{response["output"]}</div>', unsafe_allow_html=True)
            
            except Exception as e:
                status.update(label="❌ Hata oluştu", state="error")
                st.error(f"Sistem bir hata ile karşılaştı: {str(e)}")
    else:
        st.warning("Lütfen bir soru veya konu başlığı girin.")

st.markdown("---")
st.caption("Bu sistem Gemini 1.5 Flash ve Tavily AI altyapısını kullanmaktadır.")
