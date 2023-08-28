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

def epsilon_closure(automaton, states):
    epsilon_closure_set = set(states)  # Inicia com os estados fornecidos
    stack = list(states)  # Inicia a pilha com os estados fornecidos

    while stack:
        current_state = stack.pop()
        for epsilon_state in automaton[4].get(current_state, {}).get('&', set()):
            if epsilon_state not in epsilon_closure_set:
                epsilon_closure_set.add(epsilon_state)
                stack.append(epsilon_state)

    return epsilon_closure_set

def is_accepted(automaton, word):
    current_states = epsilon_closure(automaton, {automaton[0]})
    
    for symbol in word:
        next_states = set().union(*[automaton[4].get(state, {}).get(symbol, set()) for state in current_states])
        current_states = epsilon_closure(automaton, next_states)

    final_states_set = set(automaton[3])
    return bool(current_states & final_states_set)

def main():
    automaton = load_automaton("automato.txt")

    word = input("Digite uma palavra: ")
    if is_accepted(automaton, word):
        print("Aceita!")
    else:
        print("Rejeitada!")

if __name__ == "__main__":
    main()