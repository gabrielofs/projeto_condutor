from geneticFunctions import *

# Utilizamos para capturar o tempo de execução do algoritmo
start = time.time()

# Vetor que armazena os volumes(m^3) das caixas térmicas
volCaixasTermicas = [200,400,800,1600]
volCaixasTermicas.sort()

# Matriz que contêm a quantidade e volume (m^3) de cada caixa de vacina 
vacinasQtdVolume = [[4,25], [10,10], [50,10], [12,30]]

# Calcula o volume total de vacinas solicitadas
volVacinasTotal = calcVolVacinasTotal(vacinasQtdVolume)

# Definimos a quantidade de cromossomos
numCromossomos = 150

# Definimos o número de gerações
geracoes = 200

# Indentificamos a quantidade de "itens"(caixas térmicas) armazenadas no vetor volCaixasTermicas
numItens = len(volCaixasTermicas)

# Geramos a população inicial
populacao = createPopulation(numCromossomos, numItens)
# Armazenamos a primeira média no histórico de fitness para referência
historicoFitness = [mediaFitness(populacao, volVacinasTotal, volCaixasTermicas)]
# Executamos as gerações
for i in range(geracoes):
    populacao = evolution(populacao, volVacinasTotal, volCaixasTermicas, numCromossomos)
    historicoFitness.append(mediaFitness(populacao, volVacinasTotal, volCaixasTermicas))

# Utilizamos para capturar o tempo de execução do algoritmo    
end = time.time()

# Resultados
print("\nBoas Soluções: ")
for i in range(5):
    print(populacao[i])
print("\nTempo em segundos", end - start)

# Plotamos um gráfico para facilitar a vizualização da convegência para o resultado ótimo
from matplotlib import pyplot as plt
plt.plot(range(len(historicoFitness)), historicoFitness)
plt.grid(True, zorder=0)
plt.title("Problema do cálculo da quantidade de caixas")
plt.xlabel("Geração")
plt.ylabel("Volume Médio")
plt.show()