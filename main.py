from FA import FiniteAutomata
from HashTable import MyHashTable
from Grammar import Grammar
from Parser import Parser


def test_hash_tbl():
    m=MyHashTable(10)
    n=MyHashTable(50)
    m.add("a")
    m.add("a")
    m.add("b")
    m.add("c")
    m.add("d")

    for i in range(100):
        n.add(i)

    assert m.lookup("a") == True
    assert m.lookup(2) == False

    assert n.lookup("c") == False
    assert n.lookup(95) == True
    assert n.lookup(102) == False


def test_int(fa):

    assert fa.is_accepted("2190") == True
    assert fa.is_accepted("-101") == True
    assert fa.is_accepted("-01") == False
    assert fa.is_accepted("-1") == True
    assert fa.is_accepted("6443198310-") == False
    assert fa.is_accepted("0") == True
    assert fa.is_accepted("02") == False

def test_identifier(fa):

    assert fa.is_accepted("array_List") == True
    assert fa.is_accepted("pongBall") == True
    assert fa.is_accepted("Class") == False
    assert fa.is_accepted("02an") == False
    assert fa.is_accepted("a1") == True
    assert fa.is_accepted("_cnt") == False
    assert fa.is_accepted("f1_A") == True

def read_fa(file_path):
    with open(file_path, 'r') as file:
        content = file.read().split('\n')

    states = content[0].split(': ')[1].split()
    alphabet = content[1].split(': ')[1].split()
    initial = content[2].split(': ')[1]
    final = set(content[3].split(': ')[1].split())
    transitions = [line.split() for line in content[4:] if line.strip() and line != 'transitions:']

    transitions_dict = {}
    for transition in transitions:
        from_state, symbol, to_state = transition
        if (from_state,to_state) not in transitions_dict:
            transitions_dict[(from_state,to_state)] = set()
        transitions_dict[(from_state,to_state)].add(symbol)

    fa=FiniteAutomata(states, alphabet, transitions_dict, initial,final)

    while True:
        print("Select one:")
        print("1) Print the FA states")
        print("2) Print the FA alphabet")
        print("3) Print the FA transitions")
        print("4) Print the FA initial state")
        print("5) Print the FA final states")
        print("0) Continue")
        n=input()
        if n=="0":
            break
        else:
            fa.print(n)
    if file_path=="FA2.in":
        test_int(fa)
    elif file_path=="FA.in":
        test_identifier(fa)
    return fa

def validate_cfg(gr):
    for non_terminal in gr.non_terminals:
        if non_terminal not in gr.productions:
            return False
    return True
def read_grammar(file_path):
    with open(file_path, 'r') as file:
        content = file.read().split('\n')

    non_terminals = set(content[0].split(': ')[1].split())
    terminals = set(content[1].split(': ')[1].split())
    terminals.add('\n')
    terminals.add('\t')
    terminals.add(' ')
    starting_point = content[2].split(': ')[1]

    grammar_dict = {}
    for line in content[4:]:
        if line:
            key, value = line.split(' -> ')
            if key not in grammar_dict:
                grammar_dict[key] = value.split(' | ')
            else:
                grammar_dict[key].extend(value.split(' | '))

    gr = Grammar(terminals, non_terminals, starting_point, grammar_dict)
    if validate_cfg(gr):
        while True:
            print("Select one:")
            print("1) Print the Grammar terminals")
            print("2) Print the Grammar non-terminals")
            print("3) Print the Grammar starting point")
            print("4) Print the Grammar productions")
            print("5) Print productions for a given non-terminal")
            print("0) Continue")
            n=input()
            if n=="0":
                break
            else:
                gr.print(n)
        return gr
    else:
        print("Not a CFG grammar!!!")

test_hash_tbl()
identifiers_sym_tbl = MyHashTable(10)
consts_sym_tbl = MyHashTable(20)
PIF = []
tokens=[]
separators=[]
operators=[]

with open("token.in", 'r') as file:
    for line in file:
        tokens.append(line.replace('\n',''))

separators=tokens[17:27]
separators.append('\n')
separators.append('\t')

operators=tokens[2:17]
print("\n")
file_path = input("Enter the file name (e.g., a.txt):")

glb_error=False
line_cntr=0

fa_id=read_fa('FA.in')
fa_int=read_fa('FA2.in')
gr=read_grammar('g2.txt')
program=""
with open(file_path, 'r') as file:
    for line in file:
        program+=line
        line_cntr+=1
        token=""
        ok=True
        for i in line:
            if i=='"':
                if ok==False:       # we found the closing "
                    token+='"'
                    consts_sym_tbl.add(token)
                    PIF.append(("const",(consts_sym_tbl.hash_fct(token),consts_sym_tbl.get_poz(token))))
                    #print(token+" is a string const!")
                    token=""
                ok=not ok
            if ok==False:
                token+=i
                continue
            if i in separators or i in operators:
                if token not in tokens and token !="":

                    if fa_int.is_accepted(token):
                        consts_sym_tbl.add(token)
                        PIF.append(("const", (consts_sym_tbl.hash_fct(token), consts_sym_tbl.get_poz(token))))
                        if i != ' ' and i != '\n' and i != '\t':
                            PIF.append((tokens.index(i), -1))
                    elif fa_id.is_accepted(token):
                        identifiers_sym_tbl.add(token)
                        PIF.append(("id", (identifiers_sym_tbl.hash_fct(token), identifiers_sym_tbl.get_poz(token))))
                        if i != ' ' and i != '\n' and i != '\t':
                            PIF.append((tokens.index(i), -1))
                    else:
                        print(token + " is undefined; On line: " + str(line_cntr))
                        glb_error = True
                else:
                    if token !="":
                        PIF.append((tokens.index(token), -1))
                    if i != ' ' and i != '\n' and i != '\t' and i!='"':
                        if not isinstance(PIF[len(PIF)-1][0],str):
                            op=tokens[PIF[len(PIF)-1][0]]+i
                            if tokens[PIF[len(PIF)-1][0]] in operators and i in operators and op in operators:
                                PIF.pop()
                                PIF.append((tokens.index(op),-1))
                            else:
                                PIF.append((tokens.index(i), -1))
                        else:
                            PIF.append((tokens.index(i), -1))
                token = ""
            else:
                token+=i

        if ok==False:
            print("You forgot to close the \" on line " +str(line_cntr))
            glb_error=True


    if not glb_error:
        print("Program is lexically correct!")
        with open('ST.out', 'w') as file:
            file.write("The data structure used for the ST is hashmap.\n\n")
            file.write("Identifier Symbol Table.\n")
            file.write(str(identifiers_sym_tbl))
            file.write("\n")
            file.write("Constants Symbol Table.\n")
            file.write(str(consts_sym_tbl))

        with open('PIF.out', 'w') as file:
            for pair in PIF:
                file.write(str(pair)+ "\n")
        parser = Parser('q', 1, [], gr.starting_point, gr,program)
        print(program)
    else:
        with open('ST.out', 'w'):
            pass
        with open('PIF.out', 'w'):
            pass
