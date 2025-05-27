import socket

def buscar_ip(nome_host):
    try:
        # Obtém o IP do nome do host
        ip = socket.gethostbyname(nome_host)
        print(f'O IP de {nome_host} é: {ip}')
    except socket.gaierror:
        print(f'Não foi possível encontrar o IP para o host: {nome_host}')

# Exemplo de uso
nome_host = input('Digite o nome do host para buscar o IP: ')
buscar_ip(nome_host)
