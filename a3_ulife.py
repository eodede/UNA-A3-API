import requests      
import pdfkit        

#DADOS DO USUÁRIO
nome = "André Marcello Leal Leite"
ra = "324124279"
email = "324124279@ulife.com.br"
senha = "v3vayOfpT4nA"

#FAZER LOGIN NA API E PEGAR O TOKEN
url_login = "http://137.184.108.252:5000/api/login"

#Criando um dicionário com os dados de login
meu_login = {
    "email": email,
    "password": senha
}

#Fazendo a requisição POST para fazer login e pegar o token
resposta = requests.post(url_login, json=meu_login)

# Verificando se deu certo
if resposta.status_code == 200:
    dados = resposta.json()         
    token = dados["token"]         
    print("TOKEN GERADO:")
    print(token)
else:
    print("Erro ao fazer login!")
    exit()

#ETAPA 2: USAR O TOKEN PARA PEGAR AS CIDADES
url_cidades = "http://137.184.108.252:5000/api/cidades"

#Criando o cabeçalho com o token
cabecalho = {
    "x-access-token": token
}

#Fazendo a requisição GET para pegar as cidades
resposta_cidades = requests.get(url_cidades, headers=cabecalho)

#Verificando se deu certo
if resposta_cidades.status_code == 200:
    lista_cidades = resposta_cidades.json()
    print("Cidades recebidas com sucesso!")
else:
    print("Erro ao buscar cidades!")
    exit()

#ETAPA 3: HTML COM AS INFORMAÇÕES PARA GERAR O PDF
html = f"""
<html>
  <head>
    <meta charset="utf-8">
    <title>Relatório A3</title>
  </head>
  <body>
    <h1>Relatório A3 - Ulife</h1>
    <p><strong>Nome:</strong> {nome}</p>
    <p><strong>RA:</strong> {ra}</p>
    <p><strong>Token:</strong> {token}</p>
    <h2>Minhas 5 cidades:</h2>
    <table border="1" cellpadding="5">
      <tr>
        <th>ID</th>
        <th>Nome da Cidade</th>
      </tr>
"""

#Adicionando as linhas da tabela com as cidades
for cidade in lista_cidades:
    html += f"<tr><td>{cidade['id']}</td><td>{cidade['nome']}</td></tr>"

#Fechando a tabela e o HTML
html += """
    </table>
  </body>
</html>
"""

#ETAPA 4: GERAR O PDF COM O HTML CRIADO
# Caminho do wkhtmltopdf instalado no meu computador
caminho_pdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Configurando o pdfkit para usar o wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=caminho_pdf)

# Gerando o PDF e salvando com o nome "relatorio_a3.pdf"
pdfkit.from_string(html, 'relatorio_a3.pdf', configuration=config)

print("PDF gerado com sucesso!")

