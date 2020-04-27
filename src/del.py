import pickle
from datetime import datetime

tmp = [132, 2321, 543, 654, 3465, 46, 4327, 438]

def ietrator(tmp):
	for i in tmp:
		yield i


def func(gen):
	print("Resuming iteration")
	idx, num = next(gen)
	print(idx, num)




def call(gen):
	enum = enumerate(gen)
	iter(enum)
	while True:
		try:
			idx, num = next(enum)
			if idx == 3:
				raise StopIteration
		except StopIteration:
			func(enum)
			break
		print(idx, num)


def main():
	gen = ietrator(tmp)
	# pickled = pickle.dumps(gen)
	call(gen)
	

if __name__ == '__main__':
	res = datetime.strptime("2018-03-16", '%Y-%m-%d')
	print(res)
	main()