import json
import sys
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
#Describing DFA
#print(nfa)
minizedtransfun = {}
dfatransfun = {}
for transition in dfa["transition_function"]:
	#print(transition)
	if (''.join(transition[0]),transition[1]) in dfatransfun:
		#print(transition[0]+transition[1]+transition[2])
		dfatransfun[((''.join(transition[0]),transition[1]))].append(transition[2])
	else:
		dfatransfun[((''.join(transition[0]),transition[1]))] = transition[2]
partition = True
init_states = dfa["states"]
final_states = dfa["final_states"]
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
							print("Failed let's see")
							#print(canbeinapart)							
							failflag=True
							#print(''.join(partn[itr1]))
							#print(''.join(partn[itr2]))
							if(canbeinapart==[]):
								val = [''.join(partn[itr2])]
								print("COol seeing" , val)
								partn.remove((''.join(partn[itr2])))
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
	print(k[0])
	elist = [list(k[0]),k[1],val]
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
	print(dfa["final_states"])
	nlist = []
	for j in dfa["final_states"]:
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
json.dump(FinalDFA,outputfile,separators = (',\t' , ':'),indent =4)
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