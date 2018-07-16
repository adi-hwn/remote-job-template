import numpy as np
from scipy.sparse import csr_matrix

# populate tuple-to-index dict
def do_job():
	indices = {}
	id = 0
	def generateTuples(length):
		if length == 1:
			return set([(0,),(1,),(2,)])
		prev = generateTuples(length - 1);
		curr = set([]);
		for tp in prev:
			curr.add(tp + (0,))
			curr.add(tp + (1,))
			curr.add(tp + (2,))
		return curr

	tuples = generateTuples(9)
	nTuples = 0
	i = 0

	def mirror(t):
		(a,s,d,f,g,h,j,k,l) = t
		return (a,f,j,s,g,k,d,h,l)

	norm = {}
	def normalize(t):
		if t in norm:
			return norm[t]

		tmin = np.min(t)
		if tmin == 0:
			norm[t] = t
			return norm[t]
		norm[t] = tuple(t - tmin)
		return norm[t]

	for tup in tuples:
		nt = normalize(tup)
		if not nt in indices:
			indices[nt] = i
			i += 1
			nTuples += 1

	brick_matrix = csr_matrix((nTuples, nTuples),dtype=np.int64)
	brick_vector = csr_matrix((nTuples, 1),dtype=np.int64)
	brick_vector[indices[(0,0,0,0,0,0,0,0,0)]] = 1

	def add_transition(t, nt):
		ti = indices[normalize(t)]
		nti = indices[normalize(nt)]
		brick_matrix[nti, ti] += 1

	def get_transition(t, nt):
		ti = indices[normalize(t)]
		nti = indices[normalize(nt)]
		return brick_matrix[nti, ti]

	firstRow = set([0, 1, 2])
	lastRow = set([6, 7, 8])

	firstCol = set([0, 3, 6])
	lastCol = set([2, 5, 8])
	for t in indices:
		tm = np.argmin(t)
		nt = list(t)
		nt[tm] += 2
		nt = tuple(nt)
		add_transition(t, nt)
		if not (tm in lastCol) and t[tm+1] == t[tm]:
			nt = list(t)
			nt[tm] += 1
			nt[tm+1] += 1
			nt = tuple(nt)
			add_transition(t, nt)
		if not (tm in firstCol) and t[tm-1] == t[tm]:
			nt = list(t)
			nt[tm] += 1
			nt[tm-1] += 1
			nt = tuple(nt)
			add_transition(t, nt)
		if not (tm in lastRow) and t[tm+3] == t[tm]:
			nt = list(t)
			nt[tm] += 1
			nt[tm+3] += 1
			nt = tuple(nt)
			add_transition(t, nt)
		if not (tm in firstRow) and t[tm-3] == t[tm]:
			nt = list(t)
			nt[tm] += 1
			nt[tm-3] += 1
			nt = tuple(nt)
			add_transition(t, nt)

	print("Built %s transition matrix, %d entries" % (brick_matrix.shape, brick_matrix.nnz))
	q = 100000007

	def mulmod(A, B):
		C = A * B
		C.data = np.mod(C.data, q)
		return C

	mul2 = mulmod(brick_matrix, brick_matrix)
	mul4 = mulmod(mul2, mul2)
	mul8 = mulmod(mul4, mul4)
	mul16 = mulmod(mul8, mul8)
	mul32 = mulmod(mul16, mul16)
	mul40 = mulmod(mul32, mul8)
	mul5 = mulmod(mul4, brick_matrix)
	F10 = mulmod(mul40, mul5) # = mul45

	# We need 4.5eN
	for i in range(10000):
		tresult = mulmod(F10, brick_vector)
		print ("f(1e%d) = %d" % (i+1, tresult[indices[(0,0,0,0,0,0,0,0,0)],0]))
		F20 = mulmod(F10, F10)
		F40 = mulmod(F20, F20)
		F80 = mulmod(F40, F40)
		F100 = mulmod(F80, F20)
		F10 = F100


	result = mulmod(F10, brick_vector)

	print("f=",result[indices[(0,0,0,0,0,0,0,0,0)],0])
