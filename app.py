import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. API ANAHTARLARI
G_KEY = "AIzaSyB5yID-D8b12oaDR9gciXyVVRf59juNa_c"
T_KEY = "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"

# 2. SAYFA TASARIMI
st.set_page_config(page_title="AgriResearch AI", page_icon="🌱")
st.title("🌱 AgriResearch AI")

# 3. ARAŞTIRMA AJANI FONKSİYONU
def arastirma_yap(soru):
    # Model ismini 'gemini-1.5-flash' yerine 'models/gemini-1.5-flash' 
    # veya sadece 'gemini-1.5-flash' olarak kütüphanenin en güncel haliyle deniyoruz.
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        google_api_key=G_KEY,
        temperature=0.2
    )
    
    search = TavilySearchResults(api_key=T_KEY, max_results=3)
    tools = [search]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Sen uzman bir ziraat mühendisisin. Tavily ile araştırma yap ve kaynak ver."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    return agent_executor.invoke({"input": soru})

# 4. ARAYÜZ
query = st.text_input("Araştırmak istediğiniz konu:")

if st.button("Analiz Et"):
    if query:
        with st.status("🔍 İşleniyor...", expanded=True):
            try:
                res = arastirma_yap(query)
                st.markdown(f"### Rapor\n{res['output']}")
            except Exception as e:
                # Eğer hala 404 verirse, model ismini otomatik düzelten bir hata mesajı gösterelim
                st.error(f"Hata detayı: {str(e)}")
    else:
        st.warning("Lütfen bir soru girin.")
