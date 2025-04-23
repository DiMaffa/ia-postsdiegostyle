import gradio as gr
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

def gerar_conteudo(modo, entrada=""):
    try:
        if modo == "Buscar notícia automaticamente":
            base = buscar_noticia_task.execute_sync()
        else:
            base = entrada.strip()

        if not base:
            return "⚠️ Entrada inválida."

        post = escrever_post_task.execute_sync(context=str(base))
        post_otimizado = refinar_copy_task.execute_sync(context=str(post))
        hashtags = gerar_hashtags_task.execute_sync(context=str(post_otimizado))

        # Salva como txt
        agora = datetime.now().strftime("%Y-%m-%d_%H-%M")
        os.makedirs("outputs", exist_ok=True)
        path = f"outputs/post_{agora}.txt"
        with open(path, "w") as f:
            f.write("🔍 Entrada:\n" + str(base) + "\n\n")
            f.write("✍️ Post:\n" + str(post) + "\n\n")
            f.write("🎯 Otimizado:\n" + str(post_otimizado) + "\n\n")
            f.write("🏷️ Hashtags:\n" + str(hashtags) + "\n")

        return post, post_otimizado, hashtags, f"✅ Conteúdo salvo em: {path}"

    except Exception as e:
        return str(e), "", "", ""

# Interface
gr.Interface(
    fn=gerar_conteudo,
    inputs=[
        gr.Radio(["Buscar notícia automaticamente", "Informar link", "Informar tópico"], label="Modo de Geração"),
        gr.Textbox(lines=3, placeholder="Cole aqui o link da notícia ou digite um tópico...", label="Entrada")
    ],
    outputs=[
        gr.Textbox(label="✍️ Post original"),
        gr.Textbox(label="🎯 Post otimizado"),
        gr.Textbox(label="🏷️ Hashtags"),
        gr.Textbox(label="📁 Status de salvamento")
    ],
    title="🧠 DiegoStyle IA: Gerador de Posts com Botão",
    description="Gere posts de LinkedIn a partir de notícias, links ou ideias, com estilo e inteligência"
).launch(share=True)