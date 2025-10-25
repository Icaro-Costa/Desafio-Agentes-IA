import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import DuckDuckGoSearchRun

# --- Configuração ---

# Configura a ferramenta de busca
# DuckDuckGo não precisa de API Key
search_tool = DuckDuckGoSearchRun()

# Define o tema do vídeo aqui
inputs = {'query': 'Melhores jogos de 2020'}

# --- 1. Definição dos Agentes ---

# Agente: Roteirista de Vídeo
roteirista = Agent(
  role='Roteirista de Vídeo de Games',
  goal='Pesquisar e elaborar um roteiro detalhado e cativante para um vídeo no YouTube sobre {query}.',
  backstory=(
      "Você é um especialista em criação de conteúdo e storytelling para o YouTube, "
      "com foco profundo no nicho de games. Você sabe como prender a atenção da "
      "audiência e estruturar um vídeo (Introdução, Desenvolvimento, Conclusão com CTA)."
  ),
  verbose=True,
  allow_delegation=False,
  tools=[search_tool] # Ferramenta de busca
)

# Agente: Criador de Thumbnail
designer = Agent(
  role='Designer Gráfico de Thumbnails para YouTube',
  goal='Criar 3 descrições de thumbnails impactantes baseadas no roteiro do vídeo.',
  backstory=(
      "Você é um designer gráfico especialista em thumbnails para YouTube. "
      "Seu trabalho é analisar um roteiro e propor 3 conceitos visuais (descrições) "
      "que sejam chamativos, representem o conteúdo do vídeo e gerem cliques."
  ),
  verbose=True,
  allow_delegation=False
  # Este agente não precisa de ferramentas, pois usa o roteiro (contexto)
)

# Agente: Revisor
revisor = Agent(
  role='Revisor e Estrategista de Conteúdo',
  goal=(
      "Revisar o roteiro, analisar as 3 opções de thumbnail, escolher a melhor, "
      "e compilar o pacote final (roteiro + thumbnails)."
  ),
  backstory=(
      "Você é o editor-chefe. Sua função é garantir a qualidade final. "
      "Você revisa o roteiro para clareza e engajamento. "
      "Além disso, você avalia as opções de thumbnail e escolhe a mais estratégica "
      "para o sucesso do vídeo."
  ),
  verbose=True,
  allow_delegation=False
)

# --- 2. Definição das Tarefas ---

# Tarefa 1: Escrever Roteiro
task_roteiro = Task(
  description=(
      "1. Pesquise informações relevantes sobre o tema: '{query}'.\n"
      "2. Elabore um roteiro de vídeo completo (aprox. 8-10 minutos) para o YouTube.\n"
      "3. Estruture o roteiro com: Introdução (gancho), Desenvolvimento (lista/análise dos jogos), "
      "e Conclusão (resumo e Call-to-Action, ex: 'Comente seu jogo favorito de 2020')."
  ),
  expected_output='Um documento de texto formatado contendo o roteiro completo do vídeo.',
  agent=roteirista
)

# Tarefa 2: Criar Descrições de Thumbnails
task_thumbnail = Task(
  description=(
      "Usando o roteiro fornecido, crie 3 descrições detalhadas para thumbnails. "
      "Cada descrição deve ser um 'prompt' para um designer (ou IA de imagem), "
      "incluindo elementos visuais, textos curtos (max. 4 palavras), e estilo (cores, etc)."
  ),
  expected_output='Uma lista contendo 3 descrições (prompts) de thumbnail.',
  agent=designer,
  context=[task_roteiro] # Depende do roteiro
)

# Tarefa 3: Revisar e Compilar
task_revisao = Task(
  description=(
      "1. Revise o roteiro final para garantir clareza, coesão e engajamento.\n"
      "2. Analise as 3 descrições de thumbnail fornecidas.\n"
      "3. Escolha a melhor thumbnail (Opção 1, 2 ou 3) e justifique brevemente sua escolha.\n"
      "4. Compile o relatório final."
  ),
  expected_output=(
      "Um relatório final contendo:\n"
      "1. O Roteiro Revisado.\n"
      "2. As 3 Descrições de Thumbnail.\n"
      "3. A Recomendação da Melhor Thumbnail (com justificativa)."
  ),
  agent=revisor,
  context=[task_roteiro, task_thumbnail] # Depende de ambas
)

# --- 3. Execução da Crew ---

# Monta a 'Crew' (equipe)
crew = Crew(
  agents=[roteirista, designer, revisor],
  tasks=[task_roteiro, task_thumbnail, task_revisao],
  process=Process.sequential # Tarefas executadas em ordem
)

# Inicia o trabalho
print(f"🚀 Iniciando a Crew para o tema: {inputs['query']}")
result = crew.kickoff(inputs=inputs)

print("\n\n##################################################")
print("🏁 Resultado Final da Crew:")
print(result)
