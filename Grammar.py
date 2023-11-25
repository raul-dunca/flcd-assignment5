class Grammar:
    def __init__(self, t,non_t,st_pt,prod):
        self.terminals=t
        self.non_terminals=non_t
        self.starting_point=st_pt
        self.productions= prod
    def print(self, nr):
        if nr=="1":
            print("Terminals:")
            print(self.terminals)
        elif nr=="2":
            print("Non Terminals:")
            print(self.non_terminals)
        elif nr=="3":
            print("Starting Point:")
            print(self.starting_point)
        elif nr=="4":
            print("Productions:")
            print(self.productions)
        elif nr=="5":
            a=input("Enter non-terminal: ")
            if a not in self.productions:
                print("Wrong non-terminal")
            else:
                print(self.productions[a])

        else:
            print("Invalid selection!")


