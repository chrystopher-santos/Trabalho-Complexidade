def load_automaton(project):
    transitions = {}
    with open(project, 'r') as arc:
        initial_state = arc.readline().strip()  # Lê o estado inicial
        alphabet = set(arc.readline().split())  # Lê o alfabeto
        states = set(arc.readline().split())  # Lê os estados
        final_state = set(arc.readline().split())  # Lê o estado final

        for linha in arc:
            original_state, symbol, destiny_state = linha.split()  # Lê as transições
            transitions.setdefault(original_state, {}).setdefault(symbol, set()).add(destiny_state)

    return initial_state, alphabet, states, final_state, transitions

# Função para calcular o epsilon-fechamento de um conjunto de estados
def epsilon_closure(automaton, start_states):
    epsilon_closure_set = set()  # Conjunto que armazena os estados alcançados
    stack = list(start_states)    # Pilha para processar estados

    # Enquanto houver estados na pilha
    while stack:
        current_state = stack.pop()
        
        # Para cada estado alcançável por ε-transições a partir do estado atual
        for epsilon_state in automaton[4].get(current_state, {}).get('&', set()):
            if epsilon_state not in epsilon_closure_set:
                epsilon_closure_set.add(epsilon_state)
                stack.append(epsilon_state)

    return epsilon_closure_set

# Função para verificar se uma palavra é aceita pelo autômato
def is_accepted(automaton, word):
    current_states = epsilon_closure(automaton, {automaton[0]})  # Inicializa com o epsilon-fechamento do estado inicial
    
    # Para cada símbolo na palavra
    for symbol in word:
        next_states = set().union(*[automaton[4].get(state, {}).get(symbol, set()) for state in current_states])
        current_states = epsilon_closure(automaton, next_states)

    final_states_set = set(automaton[3])  # Conjunto de estados finais do autômato
    return bool(current_states & final_states_set)  # Verifica se há interseção entre estados atuais e finais

# Função principal
def main():
    automaton = load_automaton("automato.txt")  # Carrega o autômato de um arquivo
    
    word = input("Digite uma palavra: ")  # Solicita uma palavra ao usuário
    if is_accepted(automaton, word):
        print("Aceita!")  # A palavra é aceita pelo autômato
    else:
        print("Rejeitada!")  # A palavra é rejeitada pelo autômato

# Executa a função main() quando o script é executado diretamente
if __name__ == "__main__":
    main()
