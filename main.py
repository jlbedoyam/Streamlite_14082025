import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_community.tools.google_search import GoogleSearchResults
from langchain_community.tools.google_search import GoogleSearchAPIWrapper
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage

# --- Configuración de la página de Streamlit ---
st.set_page_config(
    page_title="Agente con Groq y LangChain",
    page_icon="🤖",
    layout="wide",
)

# --- Título y descripción ---
st.title("🤖 Agente de Lenguaje con Groq (Llama 3)")
st.markdown("""
Este agente utiliza la API de Groq con el modelo Llama 3 - 8B para responder a tus preguntas.
Puedes hacer preguntas generales o pedirle que busque información en la web.
""")
st.write('---')

# --- Obtener las claves de la API de Streamlit Secrets ---
# Asegúrate de tener un archivo secrets.toml en la carpeta .streamlit con las claves.
# Ejemplo:
# GROQ_API_KEY = "tu_clave_de_groq"
# GOOGLE_API_KEY = "tu_clave_de_google"
# GOOGLE_CSE_ID = "tu_id_de_motor_de_busqueda"
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    google_cse_id = st.secrets["GOOGLE_CSE_ID"]
    
    os.environ["GOOGLE_API_KEY"] = google_api_key
    os.environ["GOOGLE_CSE_ID"] = google_cse_id

except KeyError as e:
    st.error(f"Error: La clave '{e.args[0]}' no se encuentra en el archivo `secrets.toml`. "
             f"Por favor, crea un archivo `.streamlit/secrets.toml` con las claves necesarias.")
    st.stop()

# --- Definición de herramientas ---
@tool
def google_search_tool(query: str):
    """
    Herramienta que realiza una búsqueda en Google. 
    Útil para obtener información actualizada sobre cualquier tema.
    """
    search_wrapper = GoogleSearchAPIWrapper()
    tool = GoogleSearchResults(api_wrapper=search_wrapper)
    return tool.run(query)

tools = [google_search_tool]

# --- Inicialización del modelo y el agente ---
chat_model = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-8b-8192")

system_prompt = (
    "Eres un agente de lenguaje amigable y útil. "
    "Responde a todas las preguntas de la mejor manera posible. "
    "Si se te solicita información que no conoces, utiliza las herramientas disponibles. "
    "Tu objetivo es ser lo más útil posible para el usuario."
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(chat_model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Inicialización del historial de chat ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        AIMessage(content="Hola, soy un agente. ¿En qué puedo ayudarte?")
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Lógica de la interfaz de chat ---
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

if user_query := st.chat_input("Escribe tu pregunta aquí..."):
    st.session_state.messages.append(HumanMessage(content=user_query))
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.spinner("Pensando..."):
        response = agent_executor.invoke(
            {"input": user_query, "chat_history": st.session_state.chat_history}
        )
        st.session_state.chat_history.extend([
            HumanMessage(content=user_query),
            AIMessage(content=response["output"])
        ])

    st.session_state.messages.append(AIMessage(content=response["output"]))
    with st.chat_message("assistant"):
        st.markdown(response["output"])
