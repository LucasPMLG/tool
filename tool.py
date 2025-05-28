import socket
import dns.resolver  # type: ignore
import sys

def get_dns_records(domain, timeout=3.0):
    records = {}
    resolver = dns.resolver.Resolver()
    resolver.lifetime = timeout

    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']

    for record_type in record_types:
        try:
            answers = resolver.resolve(domain, record_type)
            if record_type in ['A', 'AAAA']:
                records[record_type] = [r.address for r in answers]
            else:
                records[record_type] = [r.to_text() for r in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            records[record_type] = []
        except dns.exception.Timeout:
            records[record_type] = ['Consulta DNS expirou']
        except Exception as e:
            records[record_type] = [f'Erro: {str(e)}']

    return records

def get_ips(domain):
    try:
        infos = socket.getaddrinfo(domain, None)
        ips = set([info[4][0] for info in infos])
        return list(ips)
    except socket.gaierror:
        return []

def format_results(domain, ips, dns_records):
    output = []
    output.append(f"Domínio consultado: {domain}\n")

    output.append("IPs encontrados:")
    if ips:
        for ip in ips:
            output.append(f"  - {ip}")
    else:
        output.append("  Nenhum IP encontrado.")

    output.append("\nRegistros DNS:")
    for record_type, values in dns_records.items():
        if not values:
            output.append(f"{record_type}: Nenhum registro encontrado.")
        else:
            output.append(f"{record_type}:")
            for value in values:
                output.append(f"  - {value}")

    return '\n'.join(output)

def main():
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = input("Digite o domínio para consulta: ").strip()

    print("\nResolvendo IPs...")
    ips = get_ips(domain)
    if ips:
        print(f"IPs encontrados: {', '.join(ips)}")
    else:
        print("Nenhum IP encontrado.")

    print("\nColetando registros DNS...")
    dns_records = get_dns_records(domain)

    result_text = format_results(domain, ips, dns_records)
    print("\nResultado da consulta:\n")
    print(result_text)

    salvar = input("\nDeseja salvar o resultado em um arquivo .txt? (s/n): ").strip().lower()
    if salvar == 's':
        filename = input("Digite o nome do arquivo sem extensão: ").strip()
        if not filename.endswith('.txt'):
            filename += '.txt'
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result_text)
            print(f"Resultado salvo com sucesso em '{filename}'.")
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")

if __name__ == "__main__":
    main()
