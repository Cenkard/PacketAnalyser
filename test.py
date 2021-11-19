import sys
inf= sys.maxint
S = 7
V = [1,2,4,9]

def AlgoOptimiseTab(S,V):
	k = len(V)
	M = [[([0 for l in range(x)],0)for x in range(k+1)] for y in range(S+1)] 

	for s in range(1, S+1):
		M[s][0] = [],inf


	for i in range(1, k+1):
		for s in range(1, S+1):
			terme2,n2 = [],inf
			if (s-V[i-1]>=0):
				terme, n = M[s-V[i-1]][i]
				terme2, n2 = [el for el in terme], n
				terme2[i-1], n2 = terme2[i-1]+1, n2+1
			M[s][i] = terme2, n2
			#print(M[s][i])

			terme1, n1=M[s][i-1]
			#print(terme1,n1)
			if (n1<n2):
				M[s][i] = terme1+[0],n1
			#print(M[s][i])
	return M

def AlgoOptimise(S, V):
	k = len(V)
	M = [[0 for x in range(k+1)] for y in range(S+1)]

	for s in range(1, S+1):
		M[s][0] = inf

	for i in range(1, k+1):
		for s in range(1, S+1):
			terme2 = inf
			if (s-V[i-1]>=0):
				terme2 = M[s-V[i-1]][i]+1
			M[s][i] = min(M[s][i-1], terme2)
	return M

M = AlgoOptimiseTab(S,V)

for el in M:
	print el

#complexite: 
"""
#Init
inf= sys.maxint
k= 3
S= 3
M = [[0 for x in range(k+1)] for y in range(S+1)] 

for j in range(1, S+1):
	M[j][0] = inf

s=0
i=1
tmpS= 0 #contient la valeure de s quand i atteind k
tmpI=1 #determine la valeure de i quand s atteind S

while (i+tmpS <= k+S):
	cst= s
	i=1

	arretI=cst
	if (cst==S):
		i= tmpI

	while (i<=cst and i<=k):
		terme2 = inf
		if (s-i>=0):

			
		terme2= M[s-i][i]+1
		M[s][k] = min(M[s][i-1], M[s-i][i]+1)
		i=i+1
		s=s-1
	tmpS=s

	s=cst+1
	if (cst==S):
		s=cst
		tmpI = tmpI+1

print(M)
"""
