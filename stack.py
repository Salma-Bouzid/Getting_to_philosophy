class Stack:
    
    """implementation of stack data structure in order to store values of the output 
    of a recursive function"""
    
    def __init__(self):
        self.list = []

    def push(self, key):
        if key not in self.list:
            self.list.append(key)
        else:
            raise Exception('stuck in a loop')   
    def pop(self):
        return self.list.pop()

    def is_empty(self):
        if  len(self.list) == 0:
            raise Exception('no links found')
    def length(self):
        return len(self.list)
    
    def __str__(self):
        return self.list
         