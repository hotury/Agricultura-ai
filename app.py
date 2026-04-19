import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. API ANAHTARLARI
os.environ["AIzaSyB5yID-D8b12oaDR9gciXyVVRf59juNa_c"] = "AIzaSyB5yID-D8b12oaDR9gciXyVVRf59juNa_c"
os.environ["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"] = "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"

# 2. SAYFA TASARIMI
st.set_page_config(page_title="AgriResearch AI", page_icon="🌱")
st.title("🌱 AgriResearch AI")

st.markdown("""
<style>
    .report-box {
        background-color: #f0f4f0;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #2e7d32;
        color: #1b301b;
    }
</style>
""", unsafe_allow_html=True)

# 3. ARAŞTIRMA AJANI FONKSİYONU
def arastirma_yap(soru):
    # Model: Gemini 1.5 Flash (Tool Calling desteği olan sürüm)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=0,
        convert_system_message_to_human=True # Bazı sürümlerde uyumluluk için gerekebilir
    )
    
    # Araç: Tavily Gelişmiş Arama
    search = TavilySearchResults(max_results=3, search_depth="advanced")
    tools = [search]

    # Akademik Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Sen kıdemli bir ziraat uzmanısın. Tavily aracını kullanarak akademik araştırma yap ve kaynak ver."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Ajanı Oluştur (Hata veren kısım burasıydı, sürümlerle düzelecek)
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    return agent_executor.invoke({"input": soru})

# 4. ARAYÜZ AKIŞI
user_query = st.text_input("Araştırmak istediğiniz tarım konusunu yazın:", placeholder="Örn: Ty-1 geni domates...")

if st.button("🔍 Analizi Başlat"):
    if user_query:
        with st.status("📡 Veriler taranıyor...", expanded=True) as status:
            try:
                response = arastirma_yap(user_query)
                status.update(label="✅ Tamamlandı", state="complete")
                st.markdown(f'<div class="report-box">{response["output"]}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Hata detayı: {str(e)}")
    else:
        st.warning("Lütfen bir soru girin.")
