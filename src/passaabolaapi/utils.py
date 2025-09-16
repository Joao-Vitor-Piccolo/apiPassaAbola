import random

def cadastrar_times(qtd):
    times = {}

    for i in range(qtd):
        while True:
            nome = input(f"Digite o nome do {i+1}º time: ")
            if nome:
                times[f"Time_{i+1}"] = {"nome": nome, "vitorias": 0}
                break
            else:
                print("O nome do time não pode ser vazio. Tente novamente.")
    print("\nTimes cadastrados com sucesso!")
    return times

def criar_chaveamento(times):

    lista_times = list(times.values())
    random.shuffle(lista_times)

    chaveamento = {
        "Oitavas": [],
        "Quartas": [],
        "Semifinal": [],
        "Final": [],
        "Campeao": None
    }

    print("\n--- Chaveamento das Oitavas de Final ---")
    for i in range(0, 16, 2):
        jogo = {
            "time1": lista_times[i],
            "time2": lista_times[i+1],
            "placar1": None,
            "placar2": None,
            "vencedor": None
        }
        chaveamento["Oitavas"].append(jogo)
        print(f"Jogo {len(chaveamento['Oitavas'])}: {jogo['time1']['nome']} vs {jogo['time2']['nome']}")

    return chaveamento

def atualizar_placar_e_avancar(fase_atual, proxima_fase, chaveamento):
    """
    Função auxiliar para atualizar o placar de uma fase e avançar os vencedores.
    """
    vencedores = []
    print(f"\n--- {fase_atual.replace('_', ' ')} ---")

    for i, jogo in enumerate(chaveamento[fase_atual]):
        if jogo["vencedor"]:
            print(f"Jogo {i+1} (Finalizado): {jogo['time1']['nome']} {jogo['placar1']} x {jogo['placar2']} {jogo['time2']['nome']} -> Vencedor: {jogo['vencedor']['nome']}")
            vencedores.append(jogo["vencedor"])
            continue

        print(f"\nJogo {i+1}: {jogo['time1']['nome']} vs {jogo['time2']['nome']}")
        while True:
            try:
                placar1 = int(input(f"Gols do {jogo['time1']['nome']}: "))
                placar2 = int(input(f"Gols do {jogo['time2']['nome']}: "))

                if placar1 == placar2:
                    print("O placar não pode ser um empate. Decida o vencedor (ex: pênaltis).")
                    continue

                jogo["placar1"] = placar1
                jogo["placar2"] = placar2

                if placar1 > placar2:
                    jogo["vencedor"] = jogo["time1"]
                else:
                    jogo["vencedor"] = jogo["time2"]

                vencedores.append(jogo["vencedor"])
                print(f"Vencedor: {jogo['vencedor']['nome']}")
                break
            except ValueError:
                print("Por favor, digite um número inteiro para o placar.")

    # Cria os jogos da próxima fase
    if proxima_fase:
        for i in range(0, len(vencedores), 2):
            novo_jogo = {
                "time1": vencedores[i],
                "time2": vencedores[i+1],
                "placar1": None,
                "placar2": None,
                "vencedor": None
            }
            chaveamento[proxima_fase].append(novo_jogo)
    elif vencedores:
        chaveamento["Campeao"] = vencedores[0]

