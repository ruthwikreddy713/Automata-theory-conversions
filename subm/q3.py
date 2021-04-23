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
dfa = json.load(file)
print(dfa["final_states"])
newtransn={}
for [k1,k2,k3] in dfa["transition_function"]:
	try:
		newtransn[(k1,k3)].append(k2)
	except KeyError:
		newtransn[(k1,k3)]=[k2]
print(newtransn)
for stat1 in dfa["states"]:
	for stat2 in dfa["states"]:
		try:
			if len(newtransn[(stat1,stat2)])>1:
				#Removing old transitions
				nregex = ""
				for nlet in newtransn[(stat1,stat2)]:
					dfa["transition_function"].remove([stat1,nlet,stat2])
					if nregex=='':
						nregex = nlet
					else:
						nregex = nregex + '+' + nlet
				dfa["transition_function"].append([stat1,nregex,stat2])
		except KeyError:
			print("cont")
print(dfa["transition_function"])
regex = []
newnfa = {}
newnfa["states"] = dfa["states"]+ ["S"] + ["F"]
newnfa["letters"] = dfa["letters"]
newnfa["transition_function"] = dfa["transition_function"]
for stat in  dfa["start_states"]:
	ttrans = ['S','$',stat]
	newnfa["transition_function"].append(ttrans)
for fin in dfa["final_states"]:
	ttrans = [fin,'$','F']
	newnfa["transition_function"].append(ttrans)
newnfa["start_states"] = ["S"]
newnfa["final_states"] = ["F"]
improvedtrans = {}
for [k1,k2,k3] in newnfa["transition_function"]:
	print(k1,k2,k3)
	improvedtrans[(k1,k3)]=k2
print(improvedtrans)
print(newnfa)
print(newnfa["states"])
transfin = []
try:
	print(  improvedtrans[('Q1','Q1')])
except KeyError:
	print("No")
statech = dfa["states"].copy()
for stat in dfa["states"]:
	ntrans = {}
	statech.remove(stat)
	n1 = statech + ["S"]
	n2 = statech + ["F"]
	for i in n1:
		for j in n2:
			#R1
			R1 = ""
			try:
				R1 = improvedtrans[(i,stat)]
			except KeyError:
				R1=""
			R2 = ""
			try:
				R2 = improvedtrans[(stat,stat)]
			except KeyError:
				R2=""
			R3 = ""
			try:
				R3 = improvedtrans[(stat,j)]
			except KeyError:
				R3=""
			R4 = ""
			try:
				R4 = improvedtrans[(i,j)]
			except KeyError:
				R4=""
			finalop = ""
			'''if (R1!=''):
				finalop = "("+R1+")"
			if (R2!=''):
				finalop = finalop + "(" + R2 + ")" + "*"
			if (R3!=''):
				finalop = finalop + "(" + R3 + ")"
			if (R4 != '' and finalop!=''):
				finalop = finalop + "+" + "(" + R4 + ")"
			elif finalop=='' and R4!='':
				finalop = "("+R4+")"'''
			if R1!= '' and R3 !='':
				if R2!='':
					finalop = "(" + R1 + ")" + "(" + R2 + ")*" + "(" + R3 + ")"
				else:
					finalop = "(" + R1 + ")" + "(" + R3 + ")"
			if R4!='' and finalop!='':
				finalop = finalop + "+("+R4+")"
			elif R4!= '' and finalop=='':
				finalop =  R4
			print(finalop)
			ntrans[(i,j)] = finalop
	print(ntrans)
	improvedtrans = ntrans.copy()
print(ntrans)
final_op  = {}
final_op["regex"] = ntrans[('S','F')]
outputfile = open(arglist[2],'w+')
json.dump(final_op,outputfile,separators = (',\t' , ':'),indent =4)
#Should add new states check self transitions
#outputfile = open(arglist[2],'w+')
#json.dump(dfa,outputfile,separators = (',\t' , ':'),indent =4)