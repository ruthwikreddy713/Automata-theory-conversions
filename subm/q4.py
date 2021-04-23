import json
import sys
import numpy as np
arglist = sys.argv
def powerset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item
#print(arglist)
file = open(arglist[1])
dfa = json.load(file)
vis = []
#Removing un reachable states using dfs
#Adjacency list
adj = {}
for state in dfa["states"]:
	adj[state] = []
for [i,j,k] in dfa["transition_function"]:
	if k not in adj[i]:
		adj[i].append(k)
print(adj)
#dfs
vis = []
def dfs(pos):
	vis.append(pos)
	for neig in adj[pos]:
		if neig not in vis:
			dfs(neig)
for i in dfa["start_states"]:
	dfs(i)
print(vis)
tmpstat = dfa["states"].copy()
for stat in tmpstat:
	if stat not in vis:
		print(stat)
		if stat in dfa["final_states"]:
			dfa["final_states"].remove(stat)
		dfa["states"].remove(stat)
print(dfa["states"])
print("FINAL ************")
print(dfa["final_states"])
newtrans = {}
for [i,j,k]  in dfa["transition_function"]:
	if i in dfa["states"] and k in dfa["states"]:
		newtrans[(i,j)]=k
print(newtrans)
currtable = np.zeros((len(dfa["states"]),len(dfa["states"])))
print(currtable)
for i in range(len(dfa["states"])):
	for j in range(len(dfa["states"])):
		if(i>j):
			print(i,j)
			if dfa["states"][i] in dfa["final_states"] and dfa["states"][j] not in dfa["final_states"]:
				currtable[i][j] = 1
			elif dfa["states"][i] not in dfa["final_states"] and dfa["states"][j] in dfa["final_states"]:
				currtable[i][j] = 1
		else:
			currtable[i][j]=-1
for i in currtable:
	print(i)
prevtable = np.copy(currtable)
while True:
	newtable = np.copy(prevtable)
	for i in range(len(dfa["states"])):
		for j in range(len(dfa["states"])):
			if i>j:
				if prevtable[i][j]==0:
					for letter in dfa["letters"]:
						s1 = newtrans[(dfa["states"][i],letter)]
						s2 = newtrans[(dfa["states"][j],letter)]
						print(s1,s2)
						if prevtable[dfa["states"].index(s1)][dfa["states"].index(s2)]==1 or prevtable[dfa["states"].index(s2)][dfa["states"].index(s1)]==1  :
							newtable[i][j]=1
							break
	compare = prevtable == newtable
	if (compare.all()):
		print(newtable)
		break
	else:
		prevtable = np.copy(newtable)
setlist = []
for i in range(len(dfa["states"])):
	for j in range(len(dfa["states"])):
		if(i>j):
			if prevtable[i][j] == 0:
				newset = { dfa["states"][i],dfa["states"][j] }
				setlist.append(newset)
print(setlist)
visited = []
adjnew = {}
for i in setlist:
	i = list(i)
	adjnew[i[0]]=[]
	adjnew[i[1]]=[]
def dfsnew(val,temp):
	visited.append(val)
	temp.append(val)
	for i in adjnew[val]:
		if i not in visited:
			temp = dfsnew(i,temp)
	return temp
ccompt = []
for i in setlist:
	i = list(i)
	adjnew[i[0]].append(i[1])
	adjnew[i[1]].append(i[0]) 
for i in setlist:
	i = list(i)
	if i[0] not in visited:
		temp=[]
		ccompt.append(dfsnew(i[0],temp))
	if i[1] not in visited:
		temp=[]
		ccompt.append(dfsnew(i[1],temp))

print(ccompt)
setlist = ccompt
FinalStates = []
for seti in setlist:
	FinalStates.append(list(seti))
for state in dfa["states"]:
	presence = False
	for seti in setlist:
		if state in seti:
			presence=True
			break
	if presence==False:
		FinalStates.append([state])
print(FinalStates)
Transfun = []
for i in FinalStates:
		for letter in dfa["letters"]:
			op = newtrans[(i[0],letter)]
			for destn in FinalStates:
				if op in destn:
					Transfun.append([i,letter,destn])
					break
print(Transfun)
startstatesf = []
for i in FinalStates:
	for j in i:
		if j in dfa["start_states"]:
			startstatesf.append(i)
			break
print(startstatesf)
finalstatesf = []
for i in FinalStates:
	for j in i:
		if j in dfa["final_states"]:
			finalstatesf.append(i)
			break
print(finalstatesf)
FinalDFA = {}
FinalDFA["states"] = FinalStates
FinalDFA["letters"]=dfa["letters"]
FinalDFA["transition_function"] = Transfun
FinalDFA["start_states"] = startstatesf
FinalDFA["final_states"] = finalstatesf
outputfile = open(arglist[2],'w+')
json.dump(FinalDFA,outputfile,separators = (',\t' , ':'),indent =4)
#Describing DFA
'''newtrans = []
for [i,j,k]  in dfa["transition_function"]:
	tlist = [[i],j,[k]]
	newtrans.append(tlist)
print(newtrans)
#print(nfa)
minizedtransfun = {}
dfatransfun = {}
#Formatting transition function

for transition in newtrans:
	#print(transition)
	if (''.join(transition[0]),transition[1]) in dfatransfun:
		#print(transition[0]+transition[1]+transition[2])
		dfatransfun[((''.join(transition[0]),transition[1]))].append(transition[2])
	else:
		dfatransfun[((''.join(transition[0]),transition[1]))] = transition[2]
partition = True
init_states = [ [i] for i in dfa["states"]]
final_states = [[i] for i in dfa["final_states"]]
print(final_states)
print("*****CHECK*******")
print(init_states,final_states)
non_final_states = []
for state in init_states:
	if state not in final_states:
		non_final_states.append(state)
#print(non_final_states)
Stateseperated = []
Stateseperated.append(non_final_states)
Stateseperated.append(final_states)
FinalStates = []
print(Stateseperated)
if(Stateseperated==Stateseperated):
	print("Yes")
def checkingifpartitionispossible():
	prevState = Stateseperated	
	while True:
		newstate = []
		failflag = False
		for partn in prevState:
			#CHecking if these can be in a partition			
			if(len(partn)>1 and failflag==False):
				itr1=0
				itr2=0
				canbeinapart = []
				while itr1 < len(partn)-1 and failflag==False:
					itr2 = itr1+1				
					while itr2 < len(partn) and failflag==False:
						succcheck=0
						for letter in dfa["letters"]:
							templist=[]
							if dfatransfun[(''.join(partn[itr1]),letter)] not in templist:
								templist.append(dfatransfun[(''.join(partn[itr1]),letter)])
							if dfatransfun[(''.join(partn[itr2]),letter)] not in templist:
								templist.append(dfatransfun[(''.join(partn[itr2]),letter)])
							print( ''.join(partn[itr1]), letter, dfatransfun[(''.join(partn[itr1]),letter)])
							print(''.join(partn[itr2]), letter,dfatransfun[(''.join(partn[itr2]),letter)])
							#print(templist)
							for checkpartn in prevState:
								#templist.append()
								#print("State Shit")
								#print(prevState)
								#for x in templist:
								#	print(x)
								#for x in checkpartn:
								#	print(x)
								check = [x in checkpartn for x in templist]
								print(check)
								print(checkpartn,templist)
								if all(x in checkpartn for x in templist):
									#print(templist)
									succcheck=succcheck+1
						print(succcheck)
						if (succcheck==len(dfa["letters"])):
							canbeinapart.append(''.join(partn[itr1]))
							canbeinapart.append(''.join(partn[itr2]))
							#print(canbeinapart)
						else:
							print(prevState,partn)
							print("Failed let's see")
							#print(canbeinapart)							
							failflag=True
							#print(''.join(partn[itr1]))
							#print(''.join(partn[itr2]))
							if(canbeinapart==[]):
								val = [''.join(partn[itr2])]
								print("COol seeing" , val)
								partn.remove(val)
								newstate.append([val])
							else:
								nval = partn[itr1]
								print(nval)
								print(canbeinapart)
								print (nval in canbeinapart)
								if partn[itr1][0] not in canbeinapart:
									val = [''.join(partn[itr1])]
									partn.remove([''.join(partn[itr1])])
									print("COol seeing   `1" , val)
									newstate.append([val])	
								else:
									print(partn)
									print([''.join(partn[itr2])])
									val = [''.join(partn[itr2])]									
									partn.remove([''.join(partn[itr2])])
									print("COol seeing   222" , val)									
									newstate.append([val])
						if failflag:
							print("Hi")
							break
						itr2=itr2+1
					if failflag:
						print("Hi")
						break								
					itr1=itr1+1	
			newstate.append(partn)

		print(newstate)
		print("end")
		if (prevState==newstate):
			return newstate
			break
		else:
			prevState=newstate
		print(prevState)
print("End")
FinalStates = checkingifpartitionispossible();
print(FinalStates)
#Transition Function
dfatransfunminimized = {}
for state in FinalStates:
	for letter in dfa["letters"]:
		op = dfatransfun[(''.join(state[0]),letter)]
		print(op)
		for deststate in FinalStates:
			if op in deststate:
				key1 = ""
				for i in deststate:
					key1+= i[0]
				newlist = []
				for stat in state:
					newlist.append(stat[0])
				print(newlist)
				print(state[0])
				dfatransfunminimized[(tuple(newlist),letter)]=deststate
				break
##Formatting it
dfatransfinal = []
for k,val in dfatransfunminimized.items():
	print(k,val)
	tlist=[]
	for i in val:
		tlist.append(i[0])
	print(k[0])
	elist = [list(k[0]),k[1],tlist]
	print(elist)
	dfatransfinal.append(elist)
print(dfatransfinal)
#Start State:
startstatesf=[]
for state in FinalStates:
	print(dfa["start_states"],state)
	nlist = []
	converted  = [[x] for x in dfa["start_states"]]
	print(converted)
	for j in converted:
		print(j)
		if j in state:
			nlist = []
			for stat in state:
				print(stat[0])
				nlist.append(stat[0])
			startstatesf.append(nlist)
			break
print(startstatesf)
##Fia=nalStates:	
DFAfinalstatesfinal = []
for state in FinalStates:
	print(final_states)
	nlist = []
	for j in final_states:
		if j in state:
			nlist = []
			for stat in state:
				print(stat[0])
				nlist.append(stat[0])
			DFAfinalstatesfinal.append(nlist)
			break
print(DFAfinalstatesfinal)
#Formatting Final States:
FormattedStates=[]
for state in FinalStates:
	tlist = []
	for stat in state:
		tlist.append(stat[0])
	FormattedStates.append(tlist)
print(FormattedStates)
FinalDFA = {}
FinalDFA["states"] = FormattedStates
FinalDFA["letters"] = dfa["letters"]
FinalDFA["transition_function"] = dfatransfinal
FinalDFA["start_states"] = startstatesf
FinalDFA["final_states"] = DFAfinalstatesfinal
outputfile = open(arglist[2],'w+')
json.dump(FinalDFA,outputfile,separators = (',\t' , ':'),indent =4)'''
'''for state in allstates:
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
json.dump(dfa,outputfile,separators = (',\t' , ':'),indent =4)'''
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