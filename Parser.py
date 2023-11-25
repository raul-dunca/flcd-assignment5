class Parser:
    def __init__(self, s,i,w_st,in_st,gr,w):
        self.state=s
        self.position=i             #position of current symbol in input sequence
        self.working_stack=w_st
        self.input_stack= in_st
        self.grammar=gr
        self.sequence=w

