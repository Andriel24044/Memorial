import random
import matplotlib.pyplot as plt

###############################################################################
#                                   Palindromo                                #
###############################################################################

def gera_candidato(letras_possiveis):
    """ Gera candidatos a partir de um sorteio aleatório

        Args:
            letras_possiveis: uma lista contendo as letras do alfabeto em lowercase
    """

    palavra = ''
    for i in range(5):
        palavra += random.choice(letras_possiveis)
    
    return palavra


def populacao_palindromo(tamanho_populacao, letras_possiveis):
    """ Gera a população de candidatos a palindromo

        Args:
            tamanho_populacao: um inteiro com o tamanho determinado para a população
            letras_possiveis: uma lista contendo as letras do alfabeto em lowercase
    """
    
    populacao = []

    for _ in range(tamanho_populacao):
        populacao.append(gera_candidato(letras_possiveis))

    return populacao

def funcao_objetivo_palindromo(candidato):
    """Computa a funcao objetivo de um candidato a palindromo e retorna a distancia entre o candidato e seu inverso

    Args:
      candidato: uma string contendo letras sorteadas aleatoriamente

    """
    distancia = 0
    substring = ['a','e','i','o','u']

    for i in candidato:
        if any (sub in candidato for sub in substring):
            for letra_candidato, letra_inversa in zip(candidato, candidato[::-1]):
                num_letra_candidato = ord(letra_candidato)
                num_letra_inversa = ord(letra_inversa)
                distancia += abs(num_letra_candidato - num_letra_inversa)

            return distancia 
        else:
            return float("inf")

def funcao_objetivo_palindromo_pop(populacao):
    """Computa a funcao objetivo da população de candidatos

    Args:
      populacao: uma lista contendo várias strings (candidatos)
    """

    fitness = []

    for individuo in populacao:
        fitness.append(funcao_objetivo_palindromo(individuo))

    return fitness

def funcao_cruzamento(pai, mae, chance_de_cruzamento):
    """Realiza cruzamento uniforme

    Args:
      pai: lista representando um individuo
      mae: lista representando um individuo
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento

    """
    if random.random() < chance_de_cruzamento:
        filho1 = ''
        filho2 = ''

        for gene_pai, gene_mae in zip(pai, mae):
            if random.choice([True, False]):
                filho1 += gene_pai
                filho2 += gene_mae
            else:
                filho1 += gene_mae
                filho2 += gene_pai

        return filho1, filho2
    else:
        return pai, mae
    
def funcao_mutacao1(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação simples

    Args:
    populacao: lista contendo os indivíduos do problema
    chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
    valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            valores_sorteio = set(valores_possiveis) - set([valor_gene])
            individuo.replace(valor_gene, random.choice(list(valores_sorteio)), 1)


def funcao_mutacao2(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação de salto

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            indice_letra = valores_possiveis.index(valor_gene)
            indice_letra += random.choice([1, -1])
            indice_letra %= len(valores_possiveis)
            individuo.replace(valor_gene, valores_possiveis[indice_letra], 1)


def selecao_torneio_min(populacao, fitness, tamanho_torneio):
    """Faz a seleção de uma população usando torneio.

    Nota: da forma que está implementada, só funciona em problemas de
    minimização.

    Args:
      populacao: lista contendo os individuos do problema
      fitness: lista contendo os valores computados da funcao objetivo
      tamanho_torneio: quantidade de invíduos que batalham entre si

    """
    selecionados = []

    for _ in range(len(populacao)):
        sorteados = random.sample(populacao, tamanho_torneio)

        fitness_sorteados = []
        for individuo in sorteados:
            indice_individuo = populacao.index(individuo)
            fitness_sorteados.append(fitness[indice_individuo])

        min_fitness = min(fitness_sorteados)
        indice_min_fitness = fitness_sorteados.index(min_fitness)
        individuo_selecionado = sorteados[indice_min_fitness]

        selecionados.append(individuo_selecionado)

    return selecionados


