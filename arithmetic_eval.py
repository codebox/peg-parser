'''
Functions for evaluating arithmetic expressions
'''
def op(o, n1, n2):
	if o == '+':
		return n1 + n2
	elif o == '-':
		return n1 - n2
	elif o == '*':
		return n1 * n2
	elif o == '/':
		return n1 / n2
	else:
		raise 'op fail'
	
def eval_tree(tree):
	n=tree[0]
	o=tree[1]
	if (n == 'EXPR') or (n == 'TERM') :
		if len(o) == 3:
			return op(o[1][1][0], eval_tree(o[0]), eval_tree(o[2]))
		else:
			return eval_tree(o[0])
		
	elif n == 'VAL':
		if len(o) == 3:
			return eval_tree(o[1])
		else:
			return eval_tree(o[0])
			
	elif n == 'NUM':
		return int(o[0])
		
	else:
		raise 'eval fail'
			
						
