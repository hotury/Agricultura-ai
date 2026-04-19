import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. ANAHTARLARI TANIMLAYALIM (Doğrudan parametre olarak kullanacağız)
G_KEY = "AIzaSyB5yID-D8b12oaDR9gciXyVVRf59juNa_c"
T_KEY = "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"

# Tavily için çevre değişkeni yine de kalsın (bazı kütüphane içleri bunu arar)
os.environ["TAVILY_API_KEY"] = T_KEY

# 2. SAYFA TASARIMI
st.set_page_config(page_title="AgriResearch AI", page_icon="🌱")
st.title("🌱 AgriResearch AI")

st.markdown("""
<style>
    .report-card { background-color: #f8f9fa; border-left: 6px solid #2e7d32; border-radius: 10px; padding: 20px; color: #1a331a; }
</style>
""", unsafe_allow_html=True)

# 3. ARAŞTIRMA AJANI FONKSİYONU
def arastirma_yap(soru):
    # Anahtarı burada 'google_api_key' parametresi ile doğrudan veriyoruz
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        google_api_key=G_KEY,
        temperature=0.2
    )
    
    # Tavily anahtarını da buraya doğrudan ekliyoruz
    search = TavilySearchResults(
        api_key=T_KEY, 
        max_results=5, 
        search_depth="advanced"
    )
    tools = [search]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Sen kıdemli bir ziraat mühendisisin. Tavily ile akademik araştırma yap ve kaynak ver."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    return agent_executor.invoke({"input": soru})

# 4. ARAYÜZ
query = st.text_input("Araştırmak istediğiniz konuyu yazın:", placeholder="Örn: Ty-1 geni domates...")

if st.button("Analiz Et"):
    if query:
        with st.status("🔍 Bilimsel veriler taranıyor...", expanded=True) as status:
            try:
                res = arastirma_yap(query)
                status.update(label="✅ Analiz Tamamlandı!", state="complete")
                st.markdown(f'<div class="report-card"><h3>📋 Rapor</h3>{res["output"]}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Hata detayı: {str(e)}")
    else:
        st.warning("Lütfen bir soru girin.")
