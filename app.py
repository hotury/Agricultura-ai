import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent

# 1. API ANAHTARLARI
os.environ["TAVILY_API_KEY"] = "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"
OPENROUTER_API_KEY = "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"

# 2. SAYFA TASARIMI
st.set_page_config(page_title="AgriResearch AI", page_icon="🌱")
st.title("🌱 AgriResearch AI")

# 3. ARAŞTIRMA AJANI FONKSİYONU
def arastirma_yap(soru):
    llm = ChatOpenAI(
        model="mistralai/mistral-7b-instruct:free",
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.2
    )

    search = TavilySearchResults(max_results=3)
    tools = [search]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Sen uzman bir ziraat mühendisisin. Tavily ile araştırma yap ve kaynak ver."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
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
                st.error(f"Hata detayı: {str(e)}")
    else:
        st.warning("Lütfen bir soru girin.")
