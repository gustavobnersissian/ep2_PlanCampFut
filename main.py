from satisfacao_restricoes import Restricao, SatisfacaoRestricoes

equipe = {
  "Campos FC": {"cidade": "Campos", "torcedores": 23},
  "Guardiões FC": {"cidade": "Guardião", "torcedores": 40},
  "CA Protetores": {"cidade": "Guardião", "torcedores": 20},
  "SE Leões": {"cidade": "Leão", "torcedores": 40},
  "Simba FC": {"cidade": "Leão", "torcedores": 15},
  "SE Granada": {"cidade": "Granada", "torcedores": 10},
  "CA Lagos": {"cidade": "Lagos", "torcedores": 20},
  "Solaris RC": {"cidade": "Ponte-do-Sol", "torcedores": 30},
  "Porto EC": {"cidade": "Porto", "torcedores": 45},
  "Ferroviária EC": {"cidade": "Campos", "torcedores": 38},
  "Portuários AA": {"cidade": "Porto", "torcedores": 12},
  "CA Azedos": {"cidade": "Limões", "torcedores": 18},
  "SE Escondidos": {"cidade": "Escondidos", "torcedores": 50},
  "Secretos FC": {"cidade": "Escondidos", "torcedores": 25},
}

RODADAS = (len(equipe)-1) * 2
JOGOS = int(len(equipe)/2)

# gera combinação de todos os jogos

combinacao_de_todos_jogos = []
for e1 in equipe.keys():
  for e2 in equipe.keys():
    # # remove jogos com o mesmo time
    if e1 != e2:
      combinacao_de_todos_jogos.append((e1, e2))

# Dica 1: Fazer Restrições Genéricas
class UmClassicoPorRodada(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)
  def esta_satisfeita(self, atribuicao):
    rodada = list(atribuicao.keys())[-1]
    rodada = rodada[0:2]
    jogosRodada = [x for x in list(atribuicao.keys()) if x.__contains__(rodada)]
    eClassico = 0
    
    for variavel in jogosRodada:
      times = atribuicao[variavel]
      if times is not None:
        time1 = times[0]
        time2 = times[1]
      if (equipe[time1]["torcedores"] >= 38 and equipe[time2]["torcedores"] >= 38):
        eClassico += 1
    if eClassico >= 2:
      return False
    else:
      return True
    
class UmTimePorRodadaRestricao(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    rodadas = {}
    for i in range(RODADAS): # rodadas
      rodadas["R" + str(i)] = []

    for variavel in atribuicao.keys():      
      rodada = variavel[0:2]

      times = atribuicao[variavel]
      if times is not None:
        time1 = times[0]
        time2 = times[1]
        if time1 in rodadas[rodada] or time2 in rodadas[rodada]:
          return False
        else:
          rodadas[rodada].append(time1)
          rodadas[rodada].append(time2)
    return True

class RodadasSemRepetir(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    rodadas = []

    for variavel in atribuicao.keys():
      jogos = atribuicao[variavel]
      if jogos is not None:
        if jogos in rodadas:
          return False
        else:
          rodadas.append(jogos)
    return True

class CidadesSemRepetir(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)
  def esta_satisfeita(self, atribuicao):
    rodada = list(atribuicao.keys())[-1]
    rodada = rodada[0:2]
    jogosRodada = [x for x in list(atribuicao.keys()) if x.__contains__(rodada)]
    eCidade1 = 0
    eCidade2 = 0
    eCidade3 = 0
    eCidade4 = 0
    eCidade5 = 0
    eCidade6 = 0
    eCidade7 = 0
    eCidade8 = 0
    eCidade9 = 0
    
    for variavel in jogosRodada:
      times = atribuicao[variavel]
      if times is not None:
        time1 = times[0]
      if (equipe[time1]["cidade"] == "Campos"):
        eCidade1 += 1
      elif (equipe[time1]["cidade"] == "Guardião"):
        eCidade2 += 1
      elif (equipe[time1]["cidade"] == "Leão"):
        eCidade3 += 1
      elif (equipe[time1]["cidade"] == "Ponte-do-Sol"):
        eCidade4 += 1 
      elif (equipe[time1]["cidade"] == "Porto"):
        eCidade5 += 1
      elif (equipe[time1]["cidade"] == "Granada"):
        eCidade6 += 1
      elif (equipe[time1]["cidade"] == "Lagos"):
        eCidade7 += 1
      elif (equipe[time1]["cidade"] == "Limões"):
        eCidade8 += 1
      elif (equipe[time1]["cidade"] == "Escondidos"):
        eCidade9 += 1
      
    if eCidade1 >= 2 or eCidade2 >= 2 or eCidade3 >= 2 or eCidade4 >= 2 or eCidade5 >= 2 or eCidade6 >= 2 or eCidade7 >= 2 or eCidade8 >= 2 or eCidade9 >= 2:
      return False
    else:
      return True

  

if __name__ == "__main__":
    variaveis = []
    for i in range(RODADAS): # rodadas
      for j in range(JOGOS): # jogos
        # Variável RnJm, tal que n é o número da rodada e m é o jogo da rodada
        variaveis.append("R" + str(i) + "J" + str(j))
      
    dominios = {}
    for variavel in variaveis:
        # o domínio são as combinações de todos os possívels jogos
        dominios[variavel] = combinacao_de_todos_jogos
    
    problema = SatisfacaoRestricoes(variaveis, dominios)
    problema.adicionar_restricao(UmTimePorRodadaRestricao(variaveis))
    problema.adicionar_restricao(UmClassicoPorRodada(variaveis))
    problema.adicionar_restricao(RodadasSemRepetir(variaveis))
    problema.adicionar_restricao(CidadesSemRepetir(variaveis))
    
    resposta = problema.busca_backtracking()
    if resposta is None:
      print("Nenhuma resposta encontrada")
    else:
      print("cabou")
      for i in range(RODADAS): # rodadas
        print("\n---------- Rodada " + str(i+1) + " ----------\n")
        for j in range(JOGOS): # jogos
          jogo = resposta["R" + str(i) + "J" + str(j)]
          print("Jogo " + str(j+1) + ": " + jogo[0] + " x " + jogo[1] + "\tCidade: " + equipe[jogo[0]]["cidade"])
          