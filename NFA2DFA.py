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
#print(arglist)
file = open(arglist[1])
nfa = json.load(file)
#Describing DFA
#print(nfa)
nfatransfun = {}
dfatransfun = {}
for transition in nfa["transition_function"]:
	#print(transition)
	if (transition[0],transition[1]) in nfatransfun:
		#print(transition[0]+transition[1]+transition[2])
		nfatransfun[(transition[0],transition[1])].append(transition[2])
	else:
		nfatransfun[(transition[0],transition[1])] = transition[2].split()
#print(nfatransfun)
startstate = nfa["states"]
allstates = [x for x in powerset(startstate)]
#print(startstate)
#allstates =  allstates.sort()
#print(allstates)
for state in allstates:
	#print(state)
	if(state==[]):
		for letter in nfa["letters"]:
			dfatransfun[(tuple(state),letter)]=state
	else:
		#print(state)
		for letter in nfa["letters"]:
			uniquestatereached=[]
			#print(letter)
			for eachstate in state:
				if (eachstate,letter) in nfatransfun:
					#print(nfatransfun[(eachstate,letter)])
						#print(opchar)
					if nfatransfun[(eachstate,letter)] not in uniquestatereached:
						#print(uniquestatereached)
						uniquestatereached.append(nfatransfun[(eachstate,letter)])
			dfatransfun[(tuple(state),letter)] = uniquestatereached
#print(dfatransfun)
#print("**********************************")
dfatfinal=[]
for k,val in dfatransfun.items():
	if(val!=[]):
		val=val[0]
	elist =[[list(k[0]),k[1],val]]
	#print(elist)
	dfatfinal.extend(elist)
#print(dfatfinal)
#final states
dfatfinalstates=[]
for state in allstates:
	flag=False
	for eachstate in state:
		if eachstate in nfa["final_states"]:
			flag=True
	if flag:
		dfatfinalstates.append(state)
dfa = {}
dfa["states"] = allstates
dfa["letters"]=nfa["letters"]
dfa["transition_function"]=dfatfinal
dfa["start_states"]= nfa["start_states"]
dfa["final_states"]=dfatfinalstates
outputfile = open(arglist[2],'w+')
json.dump(dfa,outputfile,separators = (',\t' , ':'),indent =4)
'''Q = []
Q.append((nfa["start_states"],))
#phi is represented as Dead state D
for state in Q:
	print(len(state))
	for letter in nfa["letters"]:
		for i in range(len(state)):
			statereached=[]
			uniquestatereached=[]
			for estate in state:
				if(estate,letter) in nfatransfun:
					for echar in nfatransfun[(estate,letter)]:
						if echar not in uniquestatereached:
							uniquestatereached.append(echar)
		if uniquestatereached:
			dfatransfun[(state,letter)]=uniquestatereached
			if tuple(uniquestatereached) not in Q:
				Q.append(tuple(uniquestatereached))		
		else:
			dfatransfun[(state,letter)]="D"
dfatfinal=[]
for k,val in dfatransfun.items():
	elist = [[k[0]],k[1],val]
	dfatfinal.extend(elist)
dfa = {}
dfa["states"]= 2 ** nfa["states"]
dfa["letters"]=nfa["letters"]
dfa["transition_function"]=dfatfinal
opfile = open('op.json','w+')
#json.dump(dfa,opfile,separators=(',\t',':'))
print(json.dumps(dfa,separators=(',\t',':'),indent=2))'''