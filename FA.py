class FiniteAutomata:
    def __init__(self, states,alphabet,transitions,init_st,fin_st):
        self.states=states
        self.alphabet=alphabet
        self.transitions= transitions
        self.initial_state=init_st
        self.final_state=fin_st
    def print(self, nr):
        if nr=="1":
            print("States:")
            print(self.states)
        elif nr=="2":
            print("Alphabet:")
            print(self.alphabet)
        elif nr=="3":
            print("Transitions:")
            print(self.transitions)
        elif nr=="4":
            print("Initial state:")
            print(self.initial_state)
        elif nr=="5":
            print("Final state:")
            print(self.final_state)
        else:
            print("Invalid selection!")


    def is_accepted(self,obj):
        current_state=self.initial_state
        for char in obj:
            transition_found = False
            for key, value in self.transitions.items():
                if key[0] == current_state and char in value:
                    current_state=key[1]
                    transition_found = True
                    break
                else:
                    continue
            if transition_found==False:
                return False
        if current_state in self.final_state:
            return True
        return False


