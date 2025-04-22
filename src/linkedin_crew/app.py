import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
from src.linkedin_crew.crew import (
    buscar_noticia_task,
    escrever_post_task,
    refinar_copy_task,
    gerar_hashtags_task
)

load_dotenv()
st.set_page_config(page_title="IA DiegoStyle", layout="wide")
st.title("🧠 IA para gerar posts estilo Diego Maffazzioli")

# Escolha do modo
modo = st.radio("Como você quer gerar o conteúdo?", [
    "1 - Buscar notícia automaticamente",
    "2 - Informar um link manual",
    "3 - Informar um tópico manual"
])

entrada = ""

if modo == "2 - Informar um link manual":
    entrada = st.text_input("Cole aqui o link da notícia")
elif modo == "3 - Informar um tópico manual":
    entrada = st.text_input("Digite o tópico ou ideia para o post")

if st.button("🚀 Gerar conteúdo"):
    with st.spinner("Executando sua crew..."):

        if modo == "1 - Buscar notícia automaticamente":
            base = buscar_noticia_task.execute_sync()
        else:
            base = entrada

        post = escrever_post_task.execute_sync(context=str(base))
        post_otimizado = refinar_copy_task.execute_sync(context=str(post))
        hashtags = gerar_hashtags_task.execute_sync(context=str(post_otimizado))

        st.success("✅ Post gerado com sucesso!")

        st.subheader("🔍 Entrada")
        st.code(str(base), language="text")

        st.subheader("✍️ Post original")
        st.write(post)

        st.subheader("🎯 Post otimizado")
        st.write(post_otimizado)

        st.subheader("🏷️ Hashtags")
        st.code(str(hashtags), language="text")

        # Salva como txt
        agora = datetime.now().strftime("%Y-%m-%d_%H-%M")
        path = f"outputs/post_{agora}.txt"
        os.makedirs("outputs", exist_ok=True)

        with open(path, "w") as f:
            f.write("🔍 Entrada:\n" + str(base) + "\n\n")
            f.write("✍️ Post:\n" + str(post) + "\n\n")
            f.write("🎯 Otimizado:\n" + str(post_otimizado) + "\n\n")
            f.write("🏷️ Hashtags:\n" + str(hashtags) + "\n")

        st.info(f"📄 Conteúdo salvo em: {path}")