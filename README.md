# [PT] Web Scraping de Livros 📖 - Python

**Autora:** Roxanne Coelho

---

### Descrição

Este projeto é uma aplicação em Python que realiza web scraping (extração de dados) no site [Books to Scrape](https://books.toscrape.com).  
Extrai informações detalhadas sobre livros, como título, preço, avaliação e link da imagem da capa, em todas as 50 páginas do site.  
Os dados recolhidos são guardados localmente num ficheiro JSON (`books.json`) para utilização posterior.

O programa inclui ainda um menu interativo que permite consultar os dados, como filtrar livros por intervalo de preços, título que começa por uma letra, avaliação, e obter estatísticas.

---

### Tecnologias Utilizadas

- Python 3  
- Bibliotecas:  
  - `requests` (para realizar pedidos HTTP)  
  - `BeautifulSoup` do pacote `bs4` (para analisar o HTML)  
  - `json` (para guardar e carregar os dados)  
  - `os` (para verificar existência de ficheiros)

---

### Estrutura do Projeto

```plaintext
📦 web-scraping-books
┣ 📜 trabalho final web scraping.py          # Script principal com o scraping e o menu
┣ 📜 books.json                              # Ficheiro JSON com os dados extraídos (gerado automaticamente)
┣ README.md                                  # Documento de descrição do projeto
```

---

### Instalação e Utilização
1. Clonar o repositório
 ```bash
https://github.com/RoxanneJCoelho/web-scraping-books
```

2. Aceder a pasta do projeto
  ```bash
cd web-scraping-books                             
```

3. Instalar as dependências
   ```bash
pip install requests beautifulsoup4                            
```
   
4. Executar o programa
  ```bash
python "trabalho final web scraping.py"                         
```

---

### Notas
- O ficheiro JSON (books.json) é criado automaticamente após a primeira execução do scraping.
- Projeto criado para fins educativos e pode ser expandido para projetos mais complexos de web scraping.

  ---

# [ENG] Book Scraper 📖 - Python Web Scraping Project

**Author:** Roxanne Coelho

---

### Description

This project is a Python application that performs web scraping on the website [Books to Scrape](https://books.toscrape.com). 
It extracts detailed information about books such as title, price, rating, and cover image URL across all 50 pages of the site.
The scraped data is saved locally in a JSON file (books.json) for later use.

The program also provides an interactive menu to query the data, including filtering books by price range, title starting letter, rating, and displaying statistics.

---

### Technologies Used

- Python 3  
- Libraries: 
  - `requests` (for HTTP requests) 
  - `BeautifulSoup` from `bs4` (for parsing HTML)
  - `json` (for saving and loading data) 
  - `os` (for file existence checks)

---

### Project Structure

```plaintext
📦 web-scraping-books
┣ 📜 trabalho final web scraping.py          # Main Python script with scraping and menu logic
┣ 📜 books.json                              # JSON file storing scraped data (auto-generated)
┣ README.md                                  # This documentation file
```

---

### Installation & Usage
1. Clone the repository
 ```bash
https://github.com/RoxanneJCoelho/web-scraping-books
```

2. Navigate to the project folder
  ```bash
cd web-scraping-books                             
```

3. Install dependencies
   ```bash
pip install requests beautifulsoup4                            
```
   
4. Run the scraper and menu
  ```bash
python "trabalho final web scraping.py"                         
```

---

### Notes
- The JSON file (books.json) is created automatically after the first scraping run.
- Designed for educational purposes; suitable as a base for more complex scraping projects.
