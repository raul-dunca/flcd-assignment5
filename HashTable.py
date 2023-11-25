class Node:
    def __init__(self, val):
        self.value=val
        self.next= None

    def __str__(self):
        return str(self.value)

class MyHashTable:
    def __init__(self, cap):
        self.capacity=cap
        self.list=[None] * (self.capacity)
        #self.size=0

    def hash_fct(self,obj):
        return hash(obj) % self.capacity

    def lookup(self,obj):
        idx = self.hash_fct(obj)
        if self.list[idx] is None:
            return False
        else:
            current=self.list[idx]
            while current.next is not None:
                if current.value==obj:
                    return True
                current = current.next
            if current.value==obj:
                return True
            return False

    def add(self, obj):
        idx=self.hash_fct(obj)
        if self.list[idx] is None:
            self.list[idx]=Node(obj)
        else:
            current=self.list[idx]
            while current.next is not None:
                if current.value==obj:
                    return
                current=current.next
            if current.value == obj:
                return
            current.next=Node(obj)

    def get_poz(self,obj):
        hash = self.hash_fct(obj)
        idx=0
        current = self.list[hash]
        while current.next is not None:
            if current.value == obj:
                return idx
            current = current.next
            idx+=1
        if current.value == obj:
            return idx

    def __str__(self):
        output=""
        for i in self.list:
            output += "List "
            if i is not None:
                while i.next is not None:
                    output+= str(i) + ' '
                    i = i.next
            output+= str(i) + '\n'
        return output
