import requests
import hashlib
import json

url1 = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=4fc0ea473e4195456255ce937ed9d3f3ec982d5f'
url2 = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=4fc0ea473e4195456255ce937ed9d3f3ec982d5f'
r = requests.get(url1)
r_json = r.json()

numb_casas = r_json['numero_casas']
cifrado = r_json['cifrado']
token = r_json['token']

texto = cifrado
chave = numb_casas


def decripta( texto, chave):
    cripto = ''
    for i in texto:
        if 'A' <= i <= 'Z':
            if ord(i) - chave < ord('A'):
                cripto += chr(ord('Z') - (chave - (ord(i) + 1 - ord('A'))))
            else:
                cripto += chr(ord(i) - chave)
        elif 'a' <= i <= 'z':
            if ord(i) - chave < ord('a'):
                cripto += chr(ord('z') - (chave - (ord(i) + 1 - ord('a'))))
            else:
                cripto += chr(ord(i) - chave)
        else:
            cripto += i
    return cripto

orig = decripta(texto, chave)

resumo_crip = hashlib.sha1(str(orig).encode('utf-8')).hexdigest()

resultado = {
    "numero_casas": numb_casas,
    "token": token,
    "cifrado": cifrado,
    "decifrado": orig,
    "resumo_criptografico": resumo_crip
}


def criar_arquivo():
    arquivo = open('answer.json', 'w')
    json.dump(resultado, arquivo)
    arquivo.close()


def postar():
    subm = url2
    file = {"answer": open("answer.json", "rb")}
    requests.post(subm, files=file)

if __name__ == '__main__':
    print(resultado)
    criar_arquivo()
    postar()