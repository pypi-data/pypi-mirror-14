from pymining import itemmining
from collections import deque 
import sys 
import pickle

def test1(fname, group_size, min_support):
	l = deque()
	transactions = []
	line = 0 
	with open(fname, 'r') as ifile:
		# while line < 100:
		# 	l.append(ifile.readline().strip(' \n\t\r'))
		# 	line += 1
		# transactions.append(tuple(l))
		# element = ifile.readline().strip(' \n\t\r')
		# line += 1
		# while element:
		# 	l.append(element)
		# 	l.popleft()
		# 	transactions.append(tuple(l))
		# 	element = ifile.readline().strip(' \n\t\r')
		# 	line += 1
		# 	print(line)
		flag = True 
		while flag:
			while line < group_size:
				e = ifile.readline().strip(' \n\t\r')
				if not e:
					flag = False 
					break 
				l.append(e)
				line += 1
			transactions.append(tuple(l))
			l.clear()
			line = 0



	print(len(transactions))
	print("memory: " + str(sys.getsizeof(transactions)))
	# transactions = [('a', 'b', 'c'), ('b'), ('a'), ('a', 'c', 'd'), ('b', 'c'), ('b', 'c')]
	# itemmining.




	relim_input = itemmining.get_relim_input(transactions)
	report = itemmining.relim(relim_input, min_support=min_support)
	for i,j in report.items():
		print(str(i)+': ' + str(j))

	with open("../Data/mining.dat", 'w') as ofile:
		for i in report.keys():
			ofile.write(','.join(i) + '\n')


	# print(report)
	# with open(fname + '_r2', 'wb') as ofile:
	# 	pickle.dump(report, ofile)


test1(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
# print('\n'*12)
# test1('b')