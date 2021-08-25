import statistics
import time
from random import getrandbits, randint, random, choice
from decimal import Decimal as D

# Calcula o volume total de vacinas com base nas dimensões
def calcVolVacinasTotal(vacinasQtdVolume):
    volumeTotal = 0
    for indice, valor in enumerate(vacinasQtdVolume):
        volumeTotal += (vacinasQtdVolume[indice][0] * vacinasQtdVolume[indice][1])
    return volumeTotal

# Cria um membro da população
def createIndividuo(numItens):
    return [ getrandbits(1) for x in range(numItens) ]

# Cria a população
def createPopulation(numIndividuos, numItens):    
    return [ createIndividuo(numItens) for x in range(numIndividuos) ]

# Faz avaliação do individuo
def fitness(individuo, volVacinasTotal, volCaixasTermicas):
    volumeTotal = 0
    for indice, valor in enumerate(individuo):
        volumeTotal += (individuo[indice] * volCaixasTermicas[indice])

    # Verifica se o o volume calculado é superior ao volume de vacinas
    if (volumeTotal > volVacinasTotal):
        # Validamos se o volume calculado é superior a mediana dos valores contidos no vetor que contém os volumes das caixas
        # e se o volume calculado é inferior ao maior valor contido no vetor que contém os volumes das caixas
        # quando ambas as condições são atendidas retornamos o volume total de vacinas solicitado, pois dessa trazemos a média o mais próximo possível do valor esperado. 
        if(volumeTotal > statistics.median(volCaixasTermicas) and volVacinasTotal <= max(volCaixasTermicas)):
            # Validamos se o volume calculado é superior a mediana dos valores contidos no vetor que contém os volumes das caixas
            # e se o volume de vacinas solicitado é superior ao maior valor contido no vetor que contém os volumes das caixas
            # quando ambas as condições são atendidas retornamos o volume total calculado, pois como o volume de vacinas solicitado excede o maior volume armazenado no vetor 
            # que contém os volumes das caixas implica que o volume calculado está mais próximo do resultado esperado.
            if(volumeTotal > statistics.median(volCaixasTermicas) and volVacinasTotal > max(volCaixasTermicas)):
                return volumeTotal
            return volVacinasTotal
        return -1
    return volumeTotal

# Encontra a avalicao media da populacao
def mediaFitness(populacao, volVacinasTotal, volCaixasTermicas):
    summed = sum(fitness(x, volVacinasTotal, volCaixasTermicas) for x in populacao if fitness(x, volVacinasTotal, volCaixasTermicas) >= 0)
    return summed / (len(populacao) * 1.0)

def selecaoRoleta(pais):
    # Seleciona um pai e uma mae baseado nas regras da roleta
    def sortear(fitnessTotal, pulaIndice=-1): #2 parametro garante que não vai selecionar o mesmo elemento
        # Monta roleta para realizar o sorteio
        roleta, acumulado, valorSorteado = [], 0, random()
        # Desconta do total, o valor que sera retirado da roleta
        if (pulaIndice!=-1): 
            fitnessTotal -= valores[0][pulaIndice]

        for indice, i in enumerate(valores[0]):
            if (pulaIndice==indice):
                continue
            acumulado += i
            roleta.append(acumulado/fitnessTotal)
            if (roleta[-1] >= valorSorteado):
                return indice

    # Cria 2 listas com os valores fitness e os cromossomos
    valores = list(zip(*pais)) 
    fitnessTotal = sum(valores[0])

    indicePai = sortear(fitnessTotal) 
    indiceMae = sortear(fitnessTotal, indicePai)

    pai = valores[1][indicePai]
    mae = valores[1][indiceMae]
    
    return pai, mae

def evolution(populacao, volVacinasTotal, volCaixasTermicas, numCromossomos, mutacao=0.05): 
    # Tabula cada individuo e o seu fitness
    pais = [ [fitness(x, volVacinasTotal, volCaixasTermicas), x] for x in populacao if fitness(x, volVacinasTotal, volCaixasTermicas) >= 0]
    pais.sort(reverse=True)
    
    # Realiza a reprodução
    filhos = []
    while (len(filhos) < numCromossomos):
        homem, mulher = selecaoRoleta(pais)
        meio = len(homem) // 2
        filho = homem[:meio] + mulher[meio:]
        filhos.append(filho)
    
    # Realiza a Mutação
    for individuo in filhos:
        if (mutacao > random()):
            posMutacao = randint(0, len(individuo)-1)
            if (individuo[posMutacao] == 1):
                individuo[posMutacao] = 0
            else:
                individuo[posMutacao] = 1

    return filhos