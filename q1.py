import json
import sys
def powerset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item
arglist = sys.argv
nfastack = []
statenumber = 0
class NFA:
	def __init__(self, states,letters,start_state,final_state,transition_table):
		self.states=states
		self.letters=letters
		self.start_state=start_state
		self.final_state=final_state
		self.transition_table = transition_table
def UnionofNFA(nfa1,nfa2):
	print("check")
	nstate = "Q"+str(statenumber)
	#statenumber=statenumber+1
	states = nfa1.states +  nfa2.states + [nstate]
	nletter =  nfa1.letters
	start_state = [nstate]
	final_state = nfa1.final_state+nfa2.final_state
	newtransn = []
	for start in nfa1.start_state:
		ttrans = [nstate,'$',start]
		newtransn.append(ttrans)
	for start in nfa2.start_state:
		ttrans = [nstate,'$',start]
		newtransn.append(ttrans)
	new_transn = nfa1.transition_table+nfa2.transition_table+newtransn
	unfa = NFA(states,nletter,start_state,final_state,new_transn)
	nfastack.append(unfa)
	print(states) 
def ConcatNFA(nfa1,nfa2):
	print("Check2")
	states = nfa1.states+nfa2.states
	start_state = nfa1.start_state
	final_state = nfa2.final_state
	etrans = []
	for i in nfa1.final_state:
		for j in nfa2.start_state:
			ttrans = [i,'$',j]
			etrans.append(ttrans)
	final_trans = nfa1.transition_table+nfa2.transition_table+etrans
	cnfa = NFA(states, nfa1.letters,start_state,final_state,final_trans)
	nfastack.append(cnfa)
def starNFA(nfa):
	print("Check3")
	nstate = "Q"+str(statenumber)
	states =nfa.states + [nstate]
	start_state = [nstate]
	final_state = [nstate]+ nfa.final_state
	newtransn = []
	for en in nfa.final_state:
		for j in nfa.start_state:
			ttrans = [en,'$',j]
			newtransn.append(ttrans)
	for j in nfa.start_state:
		ttrans = [nstate,'$',j]
		newtransn.append(ttrans)
	final_trans = nfa.transition_table+newtransn
	snfa = NFA(states,nfa.letters,start_state,final_state,final_trans)
	nfastack.append(snfa)
#print(arglist)
file = open(arglist[1])
regex = json.load(file)
listconv = list(regex["regex"])
print(regex["regex"])
def letter(inp):
	if inp==')' or inp == '(' or inp == '+' or inp == '*' or inp == '?':
		return False
	else:
		return True
def operator(inp):
	if inp==')' or inp == '(':
		return False
	else:
		return True	
def preced(op1,op2):
	if (op1=='*' and op2!='*'):
		return True
	elif (op1=='?' and op2=='+'):
		return True
	else:
		return False
#addingconcatoperator
letters=[]
for i in listconv:
	if letter(i):
		if i not in letters:
			letters.append(i)
print(letters)
inp = [] 
for i in range(len(listconv)):
	print(listconv[i])
	inp.append(listconv[i])
	if (listconv[i]=='*' and i < len(listconv)-1):
		if letter(listconv[i+1]):
			inp.append('?')
	if (i < len(listconv)-1) :
		if listconv[i+1]=='(':
			inp.append('?')
	if (letter(listconv[i]) and i < len(listconv)-1):
		if (letter(listconv[i+1])):
			inp.append('?')
	if (listconv[i]==')' and i < len(listconv)-1):
		if (letter(listconv[i+1])):
			inp.append('?')
print(inp)
##Converting to postfix
postfix = []
stack = []
precedence = {'+':1,'?':2,'*':3}
def precedcheck(val,top):
	try:
		op1 = precedence[val]
		op2 = precedence[top]
		return True if op1<=2 else False
	except KeyError:
		return False
for i in inp:
	if letter(i):
		postfix.append(i)
	elif i == '(':
		stack.append(i)
	elif i == ')':
		while (len(stack)!=0 and stack[-1]!='('):
			val = stack[-1]
			stack.pop()
			postfix.append(val)
		stack.pop()
	else:
		while(len(stack)!=0 and precedcheck(i,stack[-1])):
			postfix.append(stack[-1])
			stack.pop()
		stack.append(i)
while(len(stack)!=0):
	postfix.append(stack[-1])
	stack.pop()
print(postfix)
for i in postfix:
	if(letter(i)):
		S1 = "Q"+str(statenumber)
		statenumber=statenumber+1
		S2 = "Q"+str(statenumber)
		statenumber=statenumber+1
		states = [S1,S2]
		start_state = [S1]
		end_state = [S2]
		transition_matrix = [[S1,i,S2]]
		letterop = letters
		print(states,start_state,end_state,transition_matrix,letterop)
		lnfa = NFA(states,letterop,start_state,end_state,transition_matrix)
		nfastack.append(lnfa)
	else:
		if (i=='+'):
			op2 = nfastack[-1]
			nfastack.pop()
			op1 = nfastack[-1]
			nfastack.pop()
			UnionofNFA(op1,op2)
			statenumber=statenumber+1
			print("Hey +")
		elif (i=='*'):
			op = nfastack[-1]
			nfastack.pop()
			starNFA(op)
			statenumber=statenumber+1	
			print("Hey *")
		else:
			op2 = nfastack[-1]
			nfastack.pop()
			op1 = nfastack[-1]
			nfastack.pop()
			ConcatNFA(op1,op2)		
			print("Hi")
print(len(nfastack))
finalNFA = {}
finalNFA['states'] = nfastack[0].states
finalNFA['letters'] = nfastack[0].letters
finalNFA['transition_matrix'] = nfastack[0].transition_table
finalNFA['start_states'] = nfastack[0].start_state
finalNFA['final_states'] = nfastack[0].final_state
print(finalNFA)
outputfile = open(arglist[2],'w+')
json.dump(finalNFA,outputfile,separators = (',\t' , ':'),indent =4)