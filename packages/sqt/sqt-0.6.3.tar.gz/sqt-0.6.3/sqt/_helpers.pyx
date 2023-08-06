# kate: syntax Python;
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from collections import Counter
from cython.view cimport array as cvarray
import cython

DEF START_WITHIN_SEQ1 = 1
DEF START_WITHIN_SEQ2 = 2
DEF STOP_WITHIN_SEQ1 = 4
DEF STOP_WITHIN_SEQ2 = 8
DEF SEMIGLOBAL = 15
DEF ALLOW_WILDCARD_SEQ1 = 1
DEF ALLOW_WILDCARD_SEQ2 = 2

DEF INSERTION_COST = 1
DEF DELETION_COST = 1
DEF MATCH_COST = 0
DEF MISMATCH_COST = 1
DEF WILDCARD_CHAR = b'N'

# structure for a DP matrix entry
ctypedef struct ScoreEntry:
	int score
	int backtrace

# insertion means: inserted into seq1 (does not appear in seq2)

DEF GAPCHAR = b'\0'


@cython.boundscheck(False)
def edit_distance(s, t, int maxdiff=-1):
	"""
	Return the edit distance between the strings s and t.
	The edit distance is the sum of the numbers of insertions, deletions,
	and mismatches that is minimally necessary to transform one string
	into the other.

	If maxdiff is not -1, then a banded alignment is performed. In that case,
	the true edit distance is returned if and only if it is maxdiff or less.
	Otherwise, a value is returned that is guaranteed to be greater than
	maxdiff, but which is not necessarily the true edit distance.
	"""
	cdef int m = len(s)  # index: i
	cdef int n = len(t)  # index: j
	cdef int e = maxdiff
	cdef int i, j, start, stop, c, prev, smallest
	cdef bint match
	cdef bytes s_bytes, t_bytes
	cdef char* sv
	cdef char* tv


	# Return early if string lengths are too different
	if e != -1 and abs(m - n) > e:
		return abs(m - n)

	s_bytes = s.encode() if isinstance(s, unicode) else s
	t_bytes = t.encode() if isinstance(t, unicode) else t
	sv = s_bytes
	tv = t_bytes

	# Skip identical prefixes
	while m > 0 and n > 0 and sv[0] == tv[0]:
		sv += 1
		tv += 1
		m -= 1
		n -= 1

	# Skip identical suffixes
	while m > 0 and n > 0 and sv[m-1] == tv[n-1]:
		m -= 1
		n -= 1

	cdef int[:] costs = cvarray(shape=(m+1,), itemsize=sizeof(int), format="i")
	if e == -1:
		# Regular (unbanded) global alignment
		with nogil:
			for i in range(m + 1):
				costs[i] = i

			# compute columns of the alignment matrix (using unit costs)
			prev = 0
			for j in range(1, n+1):
				prev = costs[0]
				costs[0] += 1
				for i in range(1, m+1):
					match = sv[i-1] == tv[j-1]
					c = min(
						prev + 1 - match,
						costs[i] + 1,
						costs[i-1] + 1)
					prev = costs[i]
					costs[i] = c
	else:
		# Banded alignment
		with nogil:
			for i in range(m + 1):
				costs[i] = i
			smallest = 0
			for j in range(1, n + 1):
				stop = min(j + e + 1, m + 1)
				if j <= e:
					prev = costs[0]
					costs[0] += 1
					smallest = costs[0]
					start = 1
				else:
					start = j - e
					prev = costs[start - 1]
					smallest = maxdiff + 1
				for i in range(start, stop):
					match = sv[i-1] == tv[j-1]
					c = min(
						prev + 1 - match,
						costs[i] + 1,
						costs[i-1] + 1)
					prev = costs[i]
					costs[i] = c
					smallest = min(smallest, c)
				if smallest > maxdiff:
					break
		if smallest > maxdiff:
			return smallest
	return costs[m]


#@cython.boundscheck(False)
def globalalign(char* s1, char* s2, int flags=0, int match=1, int mismatch=-2, int insertion=-2, int deletion=-2):
	"""
	Compute an optimal global or semiglobal alignment between strings s1 and s2.
	An alignment is optimal if it has maximal score.

	The optimal score is not returned. Instead, the number of errors is computed
	and returned.

	Return ... -> (r1, r2, start1, stop1, start2, stop2, errors)

	TODO

	This is a direct translation of the C code and should be re-written to make
	it more readable. (Use Cython's memoryview for the matrix, avoid pointer-like
	access to p1 and p2.)

	FIXME THE REMAINDER OF THIS DOCSTRING

	Return a tuple (row1, row2, start1, stop1, start2, stop2, errors)
	where row1 and row2 are strings of the same length containing the alignment
	(an INDEL is marked by a null byte ('\\0').

	start1 is the position within row1 at which the part of s1, that is aligned, starts.
	start2 is the position within row1 at which the part of s1, that is aligned, ends.
	The same holds for start2, stop2.

	It is always the case that at least one of start1 and start2 is zero.

	It is always the case that either stop1==len(row1) or stop2==len(row2) or both
	(note that len(row1)==len(row2)). This is a property of semiglobal alignments.

	errors is the number of errors in the alignment.

	For example, globalalign("SISSI", "MISSISSIPPI") returns:

	row1 = [   0,   0,   0, 'S', 'I', 'S', 'S', 'I',   0,   0,   0]
	row2 = [ 'M', 'I', 'S', 'S', 'I', 'S', 'S', 'I', 'P', 'P', 'I']
	start1, stop1 = 0, 5
	start2, stop2 = 3, 8
	errors = 0

	This corresponds to the following alignment:
	   SISSI
	   |||||
	MISSISSIPPI
	"""
	cdef int m = len(s1)
	cdef int n = len(s2)
	# DP Matrix:
	#            s2 (j)
	#         ----------> n
	#        |
	# s1 (i) |
	#        |
	#        V
	#        m

	# direction constants for backtrace table
	cdef int LEFT = 1, UP = 2, DIAG = 3

	# the DP matrix is stored column-major
	cdef ScoreEntry[:,:] columns = cvarray(shape=(m+1, n+1), itemsize=sizeof(ScoreEntry), format="ii")

	cdef int i, j, bt, score, tmp

	# initialize first column
	for i in range(m + 1):
		columns[i, 0].score = 0 if (flags & START_WITHIN_SEQ1) else i * deletion
		columns[i, 0].backtrace = UP

	# initialize first row
	for j in range(n + 1):
		columns[0, j].score = 0 if (flags & START_WITHIN_SEQ2) else j * insertion
		columns[0, j].backtrace = LEFT

	# fill the entire DP matrix
	# outer loop goes over columns
	for j in range(1, n+1):
		for i in range(1, m+1):
			bt = DIAG
			score = columns[i-1,j-1].score + (match if (s1[i-1] == s2[j-1]) else mismatch)
			tmp = columns[i-1,j].score + insertion
			if tmp > score:
				bt = UP
				score = tmp
			tmp = columns[i,j-1].score + deletion
			if tmp > score:
				bt = LEFT
				score = tmp
			columns[i,j].score = score
			columns[i,j].backtrace = bt

	# initialize best score and its position to the bottomright cell
	cdef int best_i = m  # also: s1stop
	cdef int best_j = n  # also: s2stop
	cdef int best = columns[m,n].score

	if flags & STOP_WITHIN_SEQ2:
		# search also in last row
		for j in range(n + 1):
			if columns[m,j].score >= best:
				best = columns[m,j].score
				best_i = m
				best_j = j

	cdef ScoreEntry* last_column
	if flags & STOP_WITHIN_SEQ1:
		# search also in last column
		#last_column = &(columns[0,n])
		for i in range(m + 1):
			if columns[i,n].score >= best:
				best_i = i
				best_j = n
				best = columns[i,n].score

	# trace back
	cdef char* alignment1 = <char*>PyMem_Malloc((m+n+4)*sizeof(char))
	if not alignment1:
		raise MemoryError()
	cdef char* alignment2 = <char*>PyMem_Malloc((m+n+4)*sizeof(char))
	if not alignment2:
		PyMem_Free(alignment2)
		raise MemoryError()

	cdef char* p1 = alignment1
	cdef char* p2 = alignment2

	i = m
	j = n

	# first, walk from the lower right corner to the
	# position where we found the maximum score

	cdef int errors = 0

	cdef int gaps_are_errors  # if gaps are currently errors, this is 1, otherwise it's 0
	gaps_are_errors = 0 if (flags & STOP_WITHIN_SEQ2) else 1
	if i == best_i:  # we are in the last row
		while j > best_j:
			p1[0] = GAPCHAR
			j -= 1
			p2[0] = s2[j]
			p1 += 1
			p2 += 1
			errors += gaps_are_errors
	else:  # we are in the last column
		gaps_are_errors = 0 if (flags & STOP_WITHIN_SEQ1) else 1
		while i > best_i:
			i -= 1
			p1[0] = s1[i]
			p2[0] = GAPCHAR
			p1 += 1
			p2 += 1
			errors += gaps_are_errors

	assert i == best_i and j == best_j

	# the actual backtracing
	# The alignments are constructed in reverse
	# and this is undone afterwards.
	cdef int direction
	while i > 0 and j > 0:
		direction = columns[i,j].backtrace
		if direction == DIAG:
			i -= 1
			j -= 1
			if s1[i] != s2[j]:
				errors += 1
			p1[0] = s1[i]
			p2[0] = s2[j]
			p1 += 1
			p2 += 1
		elif direction == LEFT:
			errors += 1
			p1[0] = GAPCHAR
			j -= 1
			p2[0] = s2[j]
			p1 += 1
			p2 += 1
		elif direction == UP:
			i -= 1
			p1[0] = s1[i]
			p2[0] = GAPCHAR
			errors += 1
			p1 += 1
			p2 += 1
		else:
			assert False, 'DP table corrupt'

	cdef int start1 = i if (flags & START_WITHIN_SEQ1) else 0
	cdef int start2 = j if (flags & START_WITHIN_SEQ2) else 0

	errors += (i - start1) + (j - start2)

	while j > 0:
		p1[0] = GAPCHAR
		j -= 1
		p2[0] = s2[j]
		p1 += 1
		p2 += 1
	while i > 0:
		i -= 1
		p1[0] = s1[i]
		p2[0] = GAPCHAR
		p1 += 1
		p2 += 1
	assert i == 0 and j == 0

	align1 = alignment1[:(p1-alignment1)]
	align2 = alignment2[:(p2-alignment2)]

	align1 = align1[::-1]
	align2 = align2[::-1]

	PyMem_Free(alignment1)
	PyMem_Free(alignment2)

	return (align1, align2, start1, best_i, start2, best_j, errors)


def byte_frequencies(bytes s):
	"""Faster replacement for collections.Counter(s) for the case when s is a bytes object.

	Speed advantage depends on the length of the bytes object. When the length is less
	than 10, speedup is at least 2x. For length 100, speedup is 14x. For length 1000, speedup is
	approx 100x.
	"""
	cdef int[256] frequencies
	cdef int i
	cdef unsigned char c
	for i in range(256):
		frequencies[i] = 0
	for c in s:
		frequencies[c] += 1
	counter = Counter()
	for i in range(256):
		if frequencies[i] > 0:
			counter[i] = frequencies[i]
	return counter


def expected_errors(str qualities, int base=33):
	cdef int i, q
	cdef bytes quals = qualities.encode()
	cdef char* cq = quals
	cdef double e = 0.0
	for i in range(len(qualities)):
		q = cq[i] - base
		e += 10 ** (-q / 10)
	return e


def hamming_distance(unicode s, unicode t):
	"""
	Compute hamming distance between two strings. The two strings must have the
	same length.

	Return the number of differences between the strings.
	"""
	cdef Py_ssize_t m = len(s)
	cdef Py_ssize_t n = len(t)
	if m != n:
		raise IndexError("sequences must have the same length")
	cdef Py_ssize_t e = 0
	cdef Py_ssize_t i
	for i in range(m):
		if s[i] != t[i]:
			e += 1
	return e
