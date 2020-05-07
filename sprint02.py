import requests
from json import dump
from json import loads
import os
import errno
import json
from csv import DictWriter


token = input("Informe seu token do github: ")
headers = {"Authorization": "Bearer " + token} 

def run_query(query, headers): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

query = """
{
  search(query: "stars:>1", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        name
        stargazers {
          totalCount
        }
        primaryLanguage {
          name
        }
        issues(orderBy: {field: CREATED_AT, direction: ASC}, first: 10) {
          totalCount
          nodes {
            id
          }
        }
      }
    }
  }
}
"""

#obtendo a primeira query
resultado = run_query(query, headers)

#carregando o json em um dicionario python
nodes = resultado['data']['search']['nodes']

#preparando o cabecalho do arquivo csv
with open("d:/LAB-Exp-Software/LAB03/top100-repos-issues.csv", 'w') as arquivo_issues_dos_repositorios:
  cabecalho = ['name', 'stargazers', 'primaryLanguage', 'issues']
  writer = DictWriter (arquivo_issues_dos_repositorios, fieldnames = cabecalho)
  writer.writeheader()

  for node in nodes:
    writer.writerow(node)

