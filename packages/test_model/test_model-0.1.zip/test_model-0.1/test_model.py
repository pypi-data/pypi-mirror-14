def sumin_test(A):
	for a in A:
		if isinstance(a,list):
			sumin_test(a)
		else:
			print(a)