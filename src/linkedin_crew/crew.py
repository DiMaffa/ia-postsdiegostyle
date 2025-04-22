from crewai import Crew, Process, Agent, Task
from src.linkedin_crew.tools.search_tool import search_tool
import yaml

# Carrega os agents do YAML
with open("src/linkedin_crew/config/agents.yaml", "r") as f:
    agents_yaml = yaml.safe_load(f)

# Injetando a ferramenta apenas no news_hunter
news_hunter_data = agents_yaml["news_hunter"]
news_hunter = Agent(**{k: v for k, v in news_hunter_data.items() if k != "tools"}, tools=[search_tool])

post_writer = Agent(**agents_yaml["post_writer"])
copy_expert = Agent(**agents_yaml["copy_expert"])
hashtag_guru = Agent(**agents_yaml["hashtag_guru"])

# Definindo as tarefas
buscar_noticia_task = Task(
    description=(
        "Busque uma notícia real, atual e confiável sobre um dos seguintes temas: estratégia, agilidade, inovação, educação ou foresight. "
        "Priorize fontes como: Trendwatching, MIT Sloan, WEF, McKinsey, etc. "
        "Evite repetir fontes recentes. Retorne um resumo de até 3 frases + link da fonte original."
    ),
    expected_output="Resumo + link da fonte",
    agent=news_hunter
)

escrever_post_task = Task(
    description=(
        "Usando a notícia a seguir, escreva um post no estilo de Diego Maffazzioli:\n\n"
        "- Use tom analítico, provocador e inspirador\n"
        "- Use metáforas e ritmo humano\n"
        "- Finalize com: 'E a jornada só melhora...🧗🏻'\n"
        "- INCLUA o link da notícia no início do texto\n\n"
        "Notícia: {context}"
    ),
    expected_output="Post de LinkedIn com linguagem humana e link da fonte no início",
    agent=post_writer
)

refinar_copy_task = Task(
    description=(
        "Pegue o post a seguir e apllique técnicas de copywriting para deixá-lo magnético, engajador e claro.\n"
        "Mantenha o estilo e tom do original.\n\n"
        "Post: {context}"
    ),
    expected_output="Post otimizado com copywriting",
    agent=copy_expert
)

gerar_hashtags_task = Task(
    description=(
        "Com base no conteúdo abaixo, gere de 5 a 10 hashtags relevantes. "
        "Use termos que equilibram nicho e alcance. NÃO use #.\n\n"
        "Texto: {context}"
    ),
    expected_output="Hashtags separadas por espaço.",
    agent=hashtag_guru
)

crew = Crew(
    agents=[news_hunter, post_writer, copy_expert, hashtag_guru],
    tasks=[
        buscar_noticia_task,
        escrever_post_task,
        refinar_copy_task,
        gerar_hashtags_task
    ],
    process=Process.sequential
)