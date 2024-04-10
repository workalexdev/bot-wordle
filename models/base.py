from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unicodedata



service = Service(executable_path="chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_extension('C:/Users/alexa/Desktop/Hack Termoo/extensions/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_57_0_0.crx')


driver = webdriver.Chrome(options=options, service=service)


driver.get('https://wordleplay.com/pt/unlimited')
time.sleep(1)
driver.refresh()
driver.execute_script("document.body.style.backgroundImage = \"url(\'https://w.wallhaven.cc/full/85/wallhaven-856dlk.png\')\"")
listaPrimeiraLinha = []
listaSegundaLinha = []
listaTerceiraLinha = []



def is_nome_proprio(palavra):
    # Verifica se a palavra não está vazia e começa com uma letra maiúscula
    return bool(palavra) and palavra[0].isupper()



def remover_acentos(texto):
    # Normaliza o texto para a forma de decomposição canônica compatível (NFKD)
    # que separa os acentos das letras. Em seguida, filtra para manter apenas caracteres não acentuados.
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    resultado = []
    for caractere in texto_normalizado:
        if caractere == 'ç' or caractere == 'Ç':
            resultado.append(caractere)
        elif not unicodedata.combining(caractere):
            resultado.append(caractere)
    return ''.join(resultado)

def retornaIndice(listaLinha,  palavra):
    listaIndicesCerto = []
    listaIndicesErrado = []
    palavrasCerto = []
    palavrasErrado = []
    for n in range(0,5):
        if  listaLinha[n] == "cell correct":
            listaIndicesCerto.append(n)
        elif listaLinha[n] == "cell elsewhere":
            listaIndicesErrado.append(n)
    for certo in listaIndicesCerto:
        palavrasCerto += remover_acentos(palavra)[certo]
    for errado in listaIndicesErrado:
        palavrasErrado += remover_acentos(palavra)[errado]
    return palavrasCerto, palavrasErrado


def retornaDescartadas(palavra, palavrasCerto, palavrasErrado):
    palavrasDescartadas = []
    for letra in remover_acentos(palavra):
        if letra not in palavrasCerto and letra not in palavrasErrado:
            palavrasDescartadas.append(letra)
    return palavrasDescartadas
   

def retornaCoringas(palavra, listaLinha):
    novoCoringaCerto = ""
    novoCoringaErrado = ""

    indice = 0
    for letra in remover_acentos(palavra):
        try:
            if listaLinha[indice] == "cell correct":
                novoCoringaCerto += letra
                novoCoringaErrado += "0"
                
            if  listaLinha[indice] == "cell elsewhere":
                novoCoringaCerto += "0"
                novoCoringaErrado += letra
             
            if listaLinha[indice] == "cell absent":
                novoCoringaCerto += "0"
                novoCoringaErrado += "0"
           
        except IndexError:
            novoCoringaCerto += "0"
            novoCoringaErrado += "0"

        indice += 1

            
     
    return novoCoringaCerto, novoCoringaErrado        


def retornaLetrasContem(palavrasCerto, palavrasErrado):
    contem = []
    for letra in palavrasCerto:
        contem.append(letra)
    for letra in palavrasErrado:
        contem.append(letra)
    return contem


def juntarCoringasCertos(certoOne, certoTwo, certoThree):
    coringaCertoFinal = "00000"
    try: 
        for i in range(len(coringaCertoFinal)):
           
            
            if certoOne[i] != "0":
                coringaCertoFinal = coringaCertoFinal[:i] + certoOne[i] + coringaCertoFinal[i+1:]
        
            
            if certoTwo[i] != "0":
                coringaCertoFinal = coringaCertoFinal[:i] + certoTwo[i] + coringaCertoFinal[i+1:]
        
           
            if certoThree[i] != "0":
                coringaCertoFinal = coringaCertoFinal[:i] + certoThree[i] + coringaCertoFinal[i+1:]
        
    except:
        print("Erro Index")
        
    return coringaCertoFinal


def verificarPosicaoCerta(palavra, coringa):
    try:

        for i in range(len(coringa)):
            if coringa[i] != "0" and palavra[i] != coringa[i]:
                return False
        return True
    except:
        return False


def verificarPosicoesErradas(palavra, coringas):
    try:
        for coringa in coringas:
            for i in range(len(coringa)):
                if coringa[i] != "0":
                    if coringa[i] not in palavra or palavra[i] == coringa[i]:
                        return False
        return True
    except:
        return False


def enviarTeclasS(driver, palavra):
    driver.switch_to.active_element.send_keys(palavra)
    driver.switch_to.active_element.send_keys(Keys.ENTER)


def filtrarPalavras(caminho):

    
    podamCerto, podamErrado = retornaIndice(listaPrimeiraLinha, "podam")
    trensCerto, trensErrado = retornaIndice(listaSegundaLinha, "trens")
    fuzilCerto, fuzilErrado = retornaIndice(listaTerceiraLinha, "fuzil")



    listaContem = retornaLetrasContem(podamCerto, podamErrado) + retornaLetrasContem(trensCerto, trensErrado) + retornaLetrasContem(fuzilCerto, fuzilErrado)
    listaDescartadas = retornaDescartadas("podam", podamCerto, podamErrado) + retornaDescartadas("trens", trensCerto, trensErrado) + retornaDescartadas("fuzil", fuzilCerto, fuzilErrado)

  

    podamCoringaCerto, podamCoringaErrado = retornaCoringas("podam", listaPrimeiraLinha)
    trensCoringaCerto, trensCoringaErrado = retornaCoringas("trens", listaSegundaLinha)
    fuzilCoringaCerto, fuzilCoringaErrado = retornaCoringas("fuzil", listaTerceiraLinha)

    coringaCertoFinal = juntarCoringasCertos(podamCoringaCerto, trensCoringaCerto, fuzilCoringaCerto)
    coringaErradoFinal = [podamCoringaErrado, trensCoringaErrado, fuzilCoringaErrado]
  
    
    palavrasFiltradas = set()
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            palavra = linha.strip()
            palavra_sem_acentos = remover_acentos(palavra)


            if (len(palavra_sem_acentos) == 5 and
                all(remover_acentos(letra) in palavra_sem_acentos for letra in listaContem) and 
                not any(remover_acentos(letra) in palavra_sem_acentos for letra in listaDescartadas) and 
                verificarPosicaoCerta(palavra_sem_acentos, coringaCertoFinal) and 
                not is_nome_proprio(palavra_sem_acentos) and
                verificarPosicoesErradas(palavra_sem_acentos, coringaErradoFinal)):
                palavrasFiltradas.add(palavra)
                
        palavrasFiltradas = list(palavrasFiltradas)
        print(f"Total de palavras filtradas: {len(palavrasFiltradas)}")

    if len(palavrasFiltradas) == 1:
        enviarTeclasS(driver, remover_acentos(palavrasFiltradas[0]))
        print(f"Total de palavras filtradas: {len(palavrasFiltradas)}")

    if len(palavrasFiltradas) > 1:
        enviarTeclasS(driver, remover_acentos(palavrasFiltradas[0]))
        listaQuartaLinha = []
        quartaPalavrasFiltradas = set()
     
        
        for n in range(1,6):
            elementoI = driver.find_element(By.CSS_SELECTOR, f'#root > div.App-container > div.Game > div:nth-child(4) > div:nth-child({n})') 
            listaQuartaLinha.append(elementoI.get_attribute('class'))
        listaQuartaLinhaProcessada = [elemento.replace(" cell-reveal", "") for elemento in listaQuartaLinha]
        listaQuartaLinha = listaQuartaLinhaProcessada
      
        
        time.sleep(1)
        QuartaPalavraCerto, QuartaPalavraErrado = retornaIndice(listaQuartaLinha, palavrasFiltradas[0])
        QuartaListaContem = retornaLetrasContem(QuartaPalavraCerto, QuartaPalavraErrado)
        QuartaListaDescartadas = retornaDescartadas(palavrasFiltradas[0], QuartaPalavraCerto, QuartaPalavraErrado) 
        QuartaCoringaCerto, QuartaCoringaErrado = retornaCoringas(palavrasFiltradas[0], listaQuartaLinha)
        QuartaCoringaErradaFinal = [QuartaCoringaErrado]
    
        for palavraQuarta in palavrasFiltradas:
            palavraQuarta = palavraQuarta.strip()
            palvraQuartaFiltrada = remover_acentos(palavraQuarta)

            

            #not any(letra in palavraQuarta for letra in listaDescartadas)
            if (all(remover_acentos(letra) in palvraQuartaFiltrada for letra in QuartaListaContem) and
                verificarPosicaoCerta(palvraQuartaFiltrada, QuartaCoringaCerto) and
                verificarPosicoesErradas(palvraQuartaFiltrada, QuartaCoringaErradaFinal)):
                #verificarPosicaoCerta(palavraQuarta, coringaCertoFinal) and 
                #erificarPosicoesErradas(palavraQuarta, coringaErradoFinal)):
                quartaPalavrasFiltradas.add(palvraQuartaFiltrada)
                
        print(f"Total de palavras Refiltradas: {len(quartaPalavrasFiltradas)}")
        if len(quartaPalavrasFiltradas) < 3:
            for word in quartaPalavrasFiltradas:
                if word != palavrasFiltradas[0]:
            
                 enviarTeclasS(driver, word)
        
                
        if len(quartaPalavrasFiltradas) >= 2:
            woords = quartaPalavrasFiltradas
            quartaPalavrasFiltradas = []
            for filtred in woords:
                quartaPalavrasFiltradas.append(filtred)
           
            enviarTeclasS(driver, remover_acentos(quartaPalavrasFiltradas[0]))
            listaQuintaLinha = []
            QuintaPalavrasFiltradas = set()
            for n in range(1,6):
                elementoII = driver.find_element(By.CSS_SELECTOR, f'#root > div.App-container > div.Game > div:nth-child(5) > div:nth-child({n})') 
                listaQuintaLinha.append(elementoII.get_attribute('class'))
            listaQuintaLinhaProcessada = [elemento.replace(" cell-reveal", "") for elemento in listaQuartaLinha]
            listaQuintaLinha = listaQuintaLinhaProcessada
       

            time.sleep(1)
            QuintaPalavraCerto, QuintaPalavraErrado = retornaIndice(listaQuintaLinha, quartaPalavrasFiltradas[1])
            QuintaListaContem = retornaLetrasContem(QuintaPalavraCerto, QuintaPalavraErrado)
            QuintaListaDescartadas = retornaDescartadas(quartaPalavrasFiltradas[1], QuintaPalavraCerto, QuintaPalavraErrado) 
            QuintaCoringaCerto, QuintaCoringaErrado = retornaCoringas(quartaPalavrasFiltradas[1], listaQuintaLinha)
            QuintaCoringaErradaFinal = [QuintaCoringaErrado]
          
            for palavraQuinta in quartaPalavrasFiltradas:
                palavraQuinta = palavraQuinta.strip()
                palvraQuintaFiltrada = remover_acentos(palavraQuinta)

            
 #not any(remover_acentos(letra) in palavra_sem_acentos for letra in listaDescartadas) and 

            #not any(letra in palavraQuinta for letra in QuintaListaDescartadas)
            if (not any(letra in palavraQuinta for letra in QuintaListaDescartadas) and
                all(remover_acentos(letra) in palvraQuintaFiltrada for letra in QuintaListaContem) and
                verificarPosicaoCerta(palvraQuintaFiltrada, QuintaCoringaCerto) and
                verificarPosicoesErradas(palvraQuintaFiltrada, QuintaCoringaErradaFinal)):
                    #verificarPosicaoCerta(palavraQuinta, coringaCertoFinal) and 
                    #erificarPosicoesErradas(palavraQuarta, coringaErradoFinal)):
                QuintaPalavrasFiltradas.add(palvraQuintaFiltrada)
              
            print(f"Total de palavras Re(Refiltradas): {len(QuintaPalavrasFiltradas)}")


                

    
    with open('palavras_filtradas.txt', 'w') as arquivo_saida:
        for palavra in palavrasFiltradas:
            arquivo_saida.write(palavra + '\n')

    
   

def pegarClasses(driver, palavraOne, palavraTwo, palavraThree, listaPrimeiraLinha, listaSegundaLinha, listaTerceiraLinha):

    listaPrimeiraLinha.clear()
    listaSegundaLinha.clear()
    listaTerceiraLinha.clear()

   
    driver.switch_to.active_element.send_keys(palavraOne)
    driver.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(1)

    driver.switch_to.active_element.send_keys(palavraTwo)
    driver.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(1)
    
    driver.switch_to.active_element.send_keys(palavraThree)
    driver.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(1)

    try:
        for n in range(1,6):
            elementoI = driver.find_element(By.CSS_SELECTOR, f'#root > div.App-container > div.Game > div:nth-child(1) > div:nth-child({n})') 
            listaPrimeiraLinha.append(elementoI.get_attribute('class'))
            

        for n in range(1,6):
            elementoI = driver.find_element(By.CSS_SELECTOR, f'#root > div.App-container > div.Game > div:nth-child(2) > div:nth-child({n})') 
            listaSegundaLinha.append(elementoI.get_attribute('class'))
            

        for n in range(1,6):
            elementoI = driver.find_element(By.CSS_SELECTOR, f'#root > div.App-container > div.Game > div:nth-child(3) > div:nth-child({n})') 
            listaTerceiraLinha.append(elementoI.get_attribute('class'))   
            
    except: 
        for n in range(1,6):
            listaPrimeiraLinha.append("cell correct")
            listaSegundaLinha.append("cell absent")
            listaTerceiraLinha.apppend("cell absent")

caminho = "res/br-utf8.txt"

def jogar():

    while True:
        pegarClasses(driver, "podam", "trens", "fuzil", listaPrimeiraLinha, listaSegundaLinha, listaTerceiraLinha)
        filtrarPalavras(caminho)
        time.sleep(2)
        tentarClicar = True
        while tentarClicar:
            try:
                elementoNovoJogo = driver.find_element(By.CSS_SELECTOR, "#root > div.App-container > div.Game > div:nth-child(8) > div > div > div.Top-window-content > div > button.App-button.App-button-marked")
                elementoNovoJogo.click()
                tentarClicar = False
        
    
            except:
                try:
                    elementoDesistir = driver.find_element(By.CSS_SELECTOR, "#giveUp_button > button.button-giveup")
                    time.sleep(2)
                    elementoDesistir.click()
                    print("Erro ao clicar")
                    time.sleep(2)
                except:
                    print("Erro ao clicar")

        time.sleep(2)
    
        





  



        

        