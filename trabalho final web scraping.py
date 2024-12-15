# TRABALHO FINAL
# Realizado por: Roxanne Coelho

# Importar as bibliotecas que vão ser necessárias
from bs4 import BeautifulSoup
import requests
import json
import os

# Ver a estrutura da página, para assim saber como extrair os dados (esta parte está comentada para não atrapalhar no restante código)
# page = requests.get('https://books.toscrape.com/index.html')
# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())

# Função para buscar e criar uma lista com as categorias de livros
def categorias():
    page = requests.get('https://books.toscrape.com/index.html')
    soup = BeautifulSoup(page.content, 'html.parser')
    lista_categorias = [categoria.text.strip() for categoria in soup.find_all('a', href=True) if 'category' in categoria['href']] # dentro das tags a com o atributo href extrai as que tenham a palavra category nele, assim extrai o nome das categorias
    return lista_categorias

# Função para realizar web scraping duma página
def scraping(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    livros = [] # cria-se uma lista vazia para armazenar os dados dos livros
    livros_total = soup.find_all('article', class_='product_pod') # procura os elementos article que tenham a classe product_pod; cada elemento é um livro

# Extrair os dados pedidos
    for item in livros_total:
        cover = item.find('img')['src'] # dentro da tag img localiza o atributo scr que contém o link para a imagem da capa
        rating_tag = item.find('p', class_='star-rating')
        rating = rating_tag['class'][1] # o segundo item da lista é o rating
        title = item.find('h3').a['title'] # dentro da tag h3 localiza o atributo title
        price_tag = item.find('p', class_='price_color')
        price_text = price_tag.text # localiza só o texto do elemento, que corresponde ao preço
        livros.append({
            'Capa': cover,
            'Avaliacao': rating,
            'Titulo': title,
            'Preco': price_text
        }) # cria um dicionário com as informações que se quer de cada livro
    return livros

# Função para realizar web scraping de todas as páginas
def scraping_total():
    livros = []
    pagina = 1  # começa-se o looping na pagina 1
    while pagina <= 50:  # o site tem 50 páginas
        print(f'A processar a página {pagina}...')  # ajuda a acompanhar o processo de scraping
        link_pagina = f'https://books.toscrape.com/catalogue/page-{pagina}.html'         
        livros_pagina = scraping(link_pagina)  # faz o processo de scraping página a página e guarda as informações numa lista de dicionários
        if livros_pagina:  # verifica se livros_pagina tem resultados
            livros.extend(livros_pagina)  # coloca as informações na lista livros
            pagina += 1  # aumenta a página à medida que o loop vai avançando
        else:
            break  # para o loop se não encontrar livros
    return livros

# Função para salvar a lista de dicionários no ficheiro books.json
def salvar(lista_categorias, livros):
    print('A guardar as informações dos livros e das categorias no ficheiro books.json, por favor aguarde...') # esta mensagem é para ter a certeza de que esta função iniciou
    dados = {
        'Categorias': lista_categorias,
        'Livros': livros
    } # cria um dicionario com as categorias e as informações dos livros
    with open('books.json', 'w') as f:
        json.dump(dados, f, indent=4) # salva a lista dados no ficheiro books.json
    print(f'O web scraping de {len(livros)} livros e {len(lista_categorias)} categorias foi concluído com sucesso!') # esta mensagem serve não só para mostrar que o web scraping foi concluido, como tambem mostra quantos livros e categorias estão no ficheiro books.json
    
# Função que verfica se o ficheiro books.json existe ou não e se tem todos os 1000 livros
def main():
    livros = []  
    lista_categorias = []

    if os.path.exists('books.json'): # se o ficheiro books.json existe, irá carregar os dados para python para usar esses dados no menu
        print('O ficheiro books.json foi encontrado. A começar o carregamento dos dados, por favor aguarde...') # esta mensagem é para ter a certeza que o carregamento irá começar
        with open('books.json', 'r') as f:
            dados = json.load(f) # converte json para python
            livros = dados.get('Livros', []) # extrai a lista dados 
            lista_categorias = dados.get('Categorias', []) # extrai a lista lista_categorias
        print(f'O carregamento de {len(livros)} livros e {len(lista_categorias)} categorias foi concluído com sucesso!') # esta mensagem serve para mostrar que o carregamento dos dados foi concluido, e quantos livros e categorias foram carregadas
        
        if len(livros) < 1000: # se o ficheiro books.json existe, mas está incompleto (tem menos de 1000 livros), o processo de web scraping irá ser continuado
            print(f'Como este ficheiro contém apenas {len(livros)} livros, o web scraping será continuado...') # esta mensagem é para ter a certeza que o web scraping irá continuar
            livros.extend(scraping_total()) # extrai as informações que faltam
            salvar(lista_categorias, livros) # salva os dados no ficheiro books.json
    else:
        print(f'O ficheiro books.json não foi encontrado. O web scraping irá começar, por favor aguarde...') # esta mensagem é para ter a certeza que o web scraping irá começar
        lista_categorias = categorias()
        livros = scraping_total()
        salvar(lista_categorias, livros) # chama as funções categorias e scraping_total e salva os dados no ficheiro books.json
    return livros, lista_categorias

# Função do menu
def mostrar_menu():
    print('''\nBem-vindo/a ao menu dos livros! Indique abaixo o número da operação que gostaria de efetuar:
    1 - Retornar os livros cujo preço está entre X e Y
    2 - Retornar livros cujo título começa com a letra A
    3 - Retornar todos os livros cujo rating é X
    4 - Devolver estatísticas dos livros
    5 - Sair''')

# Função para filtrar os livros cujo preço está entre dois valores
def filtro_do_preco(livros, x, y):
    livros_filtro_do_preco = [] # para garantir que não há repetição de nenhum livro, primeiro cria-se uma lista vazia para armazenar os valores
    for livro in livros:
        if x <= float(livro['Preco'][1:]) <= y and livro not in livros_filtro_do_preco: # por cada livro na lista livros, adiciona a lista os que estevem dentro do intervalo, e se o livro já tiver na lista, não se repete. o float é para converter o texto em número e o preço [1:] é para retirar o símbolo da moeda
            livros_filtro_do_preco.append(livro)
    
    # Imprime se foram encontrados livros ou não, e se sim, quais foram
    if livros_filtro_do_preco:
        print(f'Foram encontrados {len(livros_filtro_do_preco)} livros:\n')  # se houver livros que satisfaçam as condições, irão ser apresentados
        for livro in livros_filtro_do_preco:
            print(f'{livro} \n')  # imprime cada livro seguido de uma quebra de linha para ficar mais legível
    else:  # se não houver livros, a seguinte mensagem é mostrada
        print('Lamento, mas nenhum livro foi encontrado.')    
    return livros_filtro_do_preco

# Função para devolver os livros cujo título começa com a letra A (esta função segue os mesmo modelos da funçao filtro_do_preco)
def titulo_A(livros):  
    livros_tituloA = []  
    for livro in livros:
        if livro['Titulo'][0] == ('A') and livro not in livros_tituloA:
         livros_tituloA.append(livro)    

    if livros_tituloA:
        print(f'Foram encontrados {len(livros_tituloA)} livros que começam com a letra A:\n') 
        for livro in livros_tituloA:
            print(f'{livro} \n')            
    else:  
        print('Lamento, mas nenhum livro foi encontrado.')  
    return livros_tituloA

# Função para filtrar os livros por rating (esta função segue os mesmo modelos da funçao filtro_do_preco)
def filtro_do_rating(livros, rating_input):    
    rating_dict = {
        1: 'One',
        2: 'Two',
        3: 'Three',
        4: 'Four',
        5: 'Five'
    } # para ser mais fácil e evitar menos erros, o usuário deve escrever 1, 2, 3, 4 ou 5 em vez de one, two, three, four ou five. cria se um dicionário para ajudar na correspondência
    rating = rating_dict[rating_input] # faz a associação entre o número e o texto
    livros_filtro_do_rating = []
    for livro in livros:
     if livro['Avaliacao'] == rating and livro not in livros_filtro_do_rating:
        livros_filtro_do_rating.append(livro)

    if livros_filtro_do_rating:
     print(f'Foram encontrados {len(livros_filtro_do_rating)} livros:\n')  
     for livro in livros_filtro_do_rating:
          print(f'{livro} \n')  
    else:  
     print('Lamento, mas nenhum livro foi encontrado.')
    return livros_filtro_do_rating

# Função para devolver as estatísticas sobre os livros
def estatisticas(livros):
    total_livros = len(livros) # devolve o numero total de livros

    livros_rating = ['One', 'Two', 'Three', 'Four', 'Five']
    total_livros_rating = {rating: 0 for rating in livros_rating} # comeca-se o looping atribuindo 0 a todos os campos
    for livro in livros:
        rating = livro['Avaliacao'] # por cada iteração, adiciona mais 1 ao rating correspondente
        if rating == 'One':
                total_livros_rating['One'] += 1
        elif rating == 'Two':
                total_livros_rating['Two'] += 1
        elif rating == 'Three':
                total_livros_rating['Three'] += 1
        elif rating == 'Four':
                total_livros_rating['Four'] += 1
        else:
                total_livros_rating['Five'] += 1
    
    intervalos_preco = ['<= 10', '>10 and <=25', '>25 and <=50', '>50'] # o mesmo método do total_livros_rating irá ser usado para o total_preco_intervalos
    total_preco_intervalos = {intervalo: 0 for intervalo in intervalos_preco}
    for livro in livros:
            preco = float(livro['Preco'][1:]) 
            if preco <= 10:
                total_preco_intervalos['<= 10'] += 1
            elif preco <= 25:
                total_preco_intervalos['>10 and <=25'] += 1
            elif preco <= 50:
                total_preco_intervalos['>25 and <=50'] += 1
            else:
                total_preco_intervalos['>50'] += 1

    return total_livros, total_livros_rating, total_preco_intervalos

# Função da estrutura do menu
def menu(livros):    
    while True:
        mostrar_menu() # no final de cada operação regressa á pagina inicial do menu dos livros
        opcao = input('>>>: ') # aqui o usuario colocará a opção que pretende
        if opcao == '1':  
            while True:
                try:
                    x = float(input('Por favor, indique o preço mínimo: '))
                    y = float(input('Por favor, indique o preço máximo: '))
                    if x > y:
                        print('O preço mínimo não pode ser maior que o preço máximo. Por favor, tente novamente.')
                        continue
                    filtro_do_preco(livros, x, y)
                    break  
                except ValueError: # se o usuário apresentar outros inputs que nãos sejam numeros válidos
                    print('Entrada inválida! Por favor, insira números válidos.')            
        elif opcao == '2':
            titulo_A(livros)            
        elif opcao == '3':  
            while True:
                try:
                   rating_input = int(input('Escolha a avaliação (1, 2, 3, 4 ou 5):'))
                   filtro_do_rating(livros, rating_input)
                   break 
                except ValueError: # se o usuário apresentar outros valores
                    print('Entrada inválida! Por favor, digite em número ou 1, ou 2, ou 3, ou 4, ou 5')                
        elif opcao == '4':             
                info = estatisticas(livros) # chama a função estatisticas
                total_livros = info[0] # como os valores foram guardados em listas, para utilizar los nesta função chama-se o primeiro valor da lista, e assim sucessivamente
                total_por_rating = info[1]
                total_preco_intervalos = info[2]
                print(f'''Sobre a nossa biblioteca:\n
            Total de livros: {total_livros}\n
            Total de livros por rating: {total_por_rating}\n
            Total de livros por intervalo de preço: {total_preco_intervalos} ''' )        
        elif opcao == '5': 
            print('Obrigada pela visita. Volte sempre!') # sai do programa
            break            
        else:  
            print('Opção inválida. Por favor, tente novamente.')

# Executar o programa
if __name__ == '__main__':
    livros, lista_categorias = main()  # chama a lista de livros e categorias na função main
    menu(livros) # inicia a função menu

