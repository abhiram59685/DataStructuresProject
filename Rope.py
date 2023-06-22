from tkinter import *
from tkinter import filedialog

characters=0
words=0
class Rope(object):
  def __init__(self, value = "", parent=None):
      if isinstance(value,str):
          if parent==None and value=="":
              self.left= None
              self.right = None
              self.weight = 0
              self.parent=None

          elif parent==None:
              self.weight = len(value)//2
              self.parent=None
              self.left= Rope(value[:self.weight],self)
              self.right = Rope(value[self.weight:],self)
          else:
              self.left = None
              self.right = None
              self.value = value
              self.weight = 0
              self.parent = parent
      else:
          raise TypeError('For time being Only Strings are supported')

  def search_node(self, index):

      if self.weight <= index and self.right != None:
           return self.right.search_node(index - self.weight)
      elif self.left != None:
          return self.left.search_node(index)
      return [self, index]

  def concatenation(self, node1, node2):

        self.right=node2
        self.left = node1
        self.weight = self.weights(self.left)
        node1.parent = self
        node2.parent = self
        return self

  def Indexing(self, index):
        # node= self.parent
        if self.weight <= index and self.right != None:
            return self.right.Indexing(index - self.weight)
        elif self.left != None:
            return self.left.Indexing(index)
        else:
            return self.value[index]

  def weights(self, node):
      if node.right!=None:
          return node.weight + node.right.weights(node.right)
      else:
          return len(node.value)

  def split(self, index):
      node, ind = self.search_node(index)
      node1=Rope(node.value[:ind],node)
      node2=Rope(node.value[ind:],node)
      node.value = ""
      node.weight = len(node1.value)
      node.left = node1
      node.right=node2
      return node
  
  def check_balancing(self,node,char):
      if node.weight <=(0.45*char) or (node.left==None and node.right==None):
          return (True, None)
      else:
           char=char-node.weight
           check, empty_node=node.right.check_balancing(node.right,char)
           return(False,node)
       
  def insertion(self, s,characters):
      characters+=len(s)
      check,node=self.check_balancing(self, characters)
      new_self=Rope()
      string_to_connect=Rope(s,new_self)
      if (check==True):
          new_self=new_self.concatenation(self, string_to_connect)
          return new_self, characters
      elif (check==False):
          new_self=new_self.concatenation(node.right, string_to_connect)
          new_self.parent=node
          node.right=new_self
          return self,characters

  def deletion (self, index_i, index_j, characters):
      for char in range(index_i, index_j):
          node, i = self.search_node(char)
          print(i)
          if node is not None:
              print(node.value)
              characters -= len(node.value)
              node.value = ""
              node = None
      return self, characters

  def split_node(self, node, s_index):
      value = node.value
      node1 = Rope(value[:s_index])
      node2 = Rope(value[s_index:])
      return node1, node2

  def edit(self, index, str1, characters):
      node, i = self.search_node(index)
      node1 = Rope(node.value[:i], node)
      node2 = Rope(str1 + node.value[i:], node)
      node.value = ""
      node.weight = len(node1.value)
      node.left=node1
      node.right =node2
      characters +=len(str1)
      return self,characters

  def print_rope(self, characters):
        result =""
        for i in range(characters):
            node, ind=self.search_node(i)
            result + node.value[ind]
        return result

def add_first(starting_string):
    document_rope=Rope(starting_string)
    characters = len(starting_string)
    return document_rope, characters

''' 
 starting_string="structures" 
 characters+=len(starting_string)
 document_rope=add_first(starting_string)
 document_rope, characters=document_rope.insertion(" data", characters)
 document_rope, characters=document_rope.insertion(" and", characters)
 document_rope, characters=document_rope.insertion(" and", characters)
 document_rope, characters=document_rope.insertion(" algorithms", characters)
 document_rope, characters=document_rope.insertion("||", characters)
 document_rope, characters=document_rope.insertion(" 4th", characters)
 document_rope, characters=document_rope.insertion(" semester", characters)
 document_rope, characters=document_rope.insertion(" Habib", characters)
 document_rope, characters=document_rope.insertion(" university", characters)
 #document_rope, characters=document_rope.edit(13, information, characters)
 #document_rope, characters=document_rope.deletion(e, 18, characters)
 document_rope.print_rope(characters)
 '''

