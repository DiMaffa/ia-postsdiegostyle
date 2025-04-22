from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from crew import (
    buscar_noticia_task,
    escrever_post_task,
    refinar_copy_task,
    gerar_hashtags_task
)
import os

# Cria pasta outputs
os.makedirs("outputs", exist_ok=True)

# Pergunta o modo
print("\n📌 Como você quer rodar?\n")
print("1 - Buscar notícia automaticamente")
print("2 - Informar um link manual")
print("3 - Informar um tópico manual")

modo = input("\nDigite o número da opção desejada: ")

# Define conteúdo base
if modo == "1":
    print("\n🔍 Buscando notícia com Serper...")
    base = buscar_noticia_task.execute_sync()
elif modo == "2":
    base = input("\n📎 Cole aqui o link da notícia que deseja usar: ")
elif modo == "3":
    base = input("\n🧠 Digite aqui o tópico ou ideia para o post: ")
else:
    print("❌ Opção inválida. Saindo.")
    exit()

# Executa sequência
post = escrever_post_task.execute_sync(context=str(base))
post_otimizado = refinar_copy_task.execute_sync(context=str(post))
hashtags = gerar_hashtags_task.execute_sync(context=str(post_otimizado))

# Exibe
print("\n✍️ Post:\n", post)
print("\n🎯 Otimizado:\n", post_otimizado)
print("\n🏷️ Hashtags:\n", hashtags)

# Salva
agora = datetime.now().strftime("%Y-%m-%d_%H-%M")
path = f"outputs/post_{agora}.txt"

with open(path, "w") as f:
    f.write("🔍 Entrada:\n" + str(base) + "\n\n")
    f.write("✍️ Post:\n" + str(post) + "\n\n")
    f.write("🎯 Otimizado:\n" + str(post_otimizado) + "\n\n")
    f.write("🏷️ Hashtags:\n" + str(hashtags) + "\n")

print(f"\n✅ Conteúdo salvo em: {path}")