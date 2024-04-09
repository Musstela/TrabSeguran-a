def ler_arquivo(caminho):
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def calcular_ic(texto):
    n = len(texto)
    frequencias = {}
    for letra in texto:
        if letra.isalpha():
            letra = letra.lower()
            if letra in frequencias:
                frequencias[letra] += 1
            else:
                frequencias[letra] = 1

    ic = sum(f * (f - 1) for f in frequencias.values()) / (n * (n - 1))
    return ic

def estimar_tamanho_chave(ciphertext):
    ics = []
    for tamanho_chave in range(1, 21):  # Testa tamanhos de chave de 1 a 20
        segmentos = [''.join(ciphertext[i::tamanho_chave]) for i in range(tamanho_chave)]
        for segmento in segmentos:
            ics.append(((tamanho_chave),(calcular_ic(segmento))))

    # Considera-se o tamanho de chave que mais se aproxima do IC de uma linguagem natural
    # IC para inglês: ~0.067, para português: ~0.072
    tamanho_chave_estimado = numero_mais_proximo(ics, 0.067)[0]
    
    print(f"Tamanho estimado da chave: {tamanho_chave_estimado}")
    return tamanho_chave_estimado

def numero_mais_proximo(array, alvo):
    # Inicializa a variável para armazenar o número mais próximo encontrado
    mais_proximo = None

    # Inicializa a variável para armazenar a menor diferença encontrada até o momento
    menor_diferenca = float('inf')

    # Percorre todos os elementos do array
    i = 0
    for valor, numero in array:
        # Calcula a diferença absoluta entre o número atual e o alvo
        diferenca = abs(numero - alvo)

        # Verifica se a diferença atual é menor que a menor diferença encontrada até o momento
        if diferenca < menor_diferenca:
            # Atualiza o número mais próximo e a menor diferença encontrada até o momento
            mais_proximo = array[i]
            menor_diferenca = diferenca

        i += 1

    return mais_proximo

def extrair_substrings_de_arquivo(cifra,tamanho_chave):

    cifra = cifra.replace('\n', ' ').replace('\r', '')

    # Variável para armazenar as substrings
    matriz = [[] for _ in range(tamanho_chave)]
    indexLocal = 0
    
    for i in range(len(cifra)):
        if(indexLocal == tamanho_chave) : indexLocal = 0
        matriz[indexLocal].append(cifra[i])
        indexLocal += 1 

    return matriz

def decifrar_vigenere(matriz):
    i = 0
    for array in (matriz):
        caracter_frequente = caractere_mais_frequente(array)
        delta = diferenca_ascii(caracter_frequente,"e")
        array_decifrado = cifra_de_cesar(array,delta)
        matriz[i] = array_decifrado
        i += 1
        
    return matriz

def caractere_mais_frequente(array):
    frequencias = {}

    for caractere in array:
        if caractere in frequencias:
            frequencias[caractere] += 1
        else:
            frequencias[caractere] = 1

    caractere_max = None
    frequencia_max = -1

    for caractere, frequencia in frequencias.items():
        if frequencia > frequencia_max:
            caractere_max = caractere
            frequencia_max = frequencia

    return caractere_max

def diferenca_ascii(caractere1, caractere2):
    letra_mais_recorrente_do_texto = ord(caractere1)
    letra_mais_recorrente_ingles = ord(caractere2)

    diferenca = letra_mais_recorrente_ingles - letra_mais_recorrente_do_texto

    return diferenca

def cifra_de_cesar(array,delta):
    i = 0

    for letra in array:
        letra_deslocada = (ord(letra) + delta)
        
        if(letra_deslocada < 97) :
            letra_deslocada = 123 - (97 - letra_deslocada)
        elif(letra_deslocada > 122) :
            letra_deslocada = 96 + (letra_deslocada - 122)
        
        array[i] = chr(letra_deslocada)
        i += 1
    
    return array

def concatenar_texto(arrays_decifrados,tamanho_chave):
    texto_claro = ""

    try:
        for i in range(len(arrays_decifrados[0])):
            for j in range(tamanho_chave):
                texto_claro += arrays_decifrados[j][i]

    except IndexError:
        return texto_claro

    return texto_claro

def arquivo_decifrado(texto_claro):
    nome_arquivo = "texto_claro.txt"

    with open(nome_arquivo, "w") as arquivo:
        arquivo.write(texto_claro)

    print("Arquivo de texto criado com sucesso!")

def main():
    cifra = ler_arquivo("cypher17.txt")
    tamanho_chave = estimar_tamanho_chave(cifra)
    texto_divido_pelo_tamanho_da_chave = extrair_substrings_de_arquivo(cifra,tamanho_chave)
    arrays_decifrados = decifrar_vigenere(texto_divido_pelo_tamanho_da_chave,)
    texto_claro = concatenar_texto(arrays_decifrados,tamanho_chave)
    arquivo_decifrado(texto_claro)

if __name__ == "__main__":
    main()