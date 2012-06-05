import re, sys, pprint

'''
Rough and ready PEG parser, needs much work
'''

def parse_line(line):
	name, rhs = line.split(':',1)
	rhs_parts = [p.strip() for p in rhs.split('|')]
	rhs_parts_seqs = [p.split(' ') for p in rhs_parts]
	return name, rhs_parts_seqs

def validate_tokenised_grammar(tg):
	for v in tg.values():
		for alternative in v:
			for token in alternative:
				if token not in tg:
					regex = re.compile(token)

def consume(symbol, g, txt):
	'''
	Does the text match the specified symbol? If it does, then return the remainder
	of the text after the symbol has been consumed, otherwise return None
	'''
	tree = []
	if symbol in g:
		alternatives = g[symbol]
		matching_alt = None
		remainder = None
		for alt in alternatives:
			all_tokens_in_alt_match = True
			remainder = txt
			tree_for_alt = []
			for token in alt:
				remainder, t = consume(token, g, remainder)
				tree_for_alt.append(t)
				if remainder is None:
					all_tokens_in_alt_match = False
					break
					
			if all_tokens_in_alt_match:
				matching_alt = alt
				tree = (symbol, tuple(tree_for_alt))
				break
		
		if matching_alt:
			return remainder, tree
			
		else:
			return None, None
					
	else:
		match = re.match(symbol, txt)
		if match:
			matching_txt = match.group(0)
			tree.append( matching_txt)
			return txt[len(matching_txt):], matching_txt
		else:
			return None, None

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
		
def flatten(l):
	if type(l) is list:
		return flatten(l[0]) if len(l) == 1 else map(flatten, l)
	else:
		return l
	
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
			
						
def main():
	# read the grammar
	tokenised_grammar = parse_grammar_file('grammar.txt')
	validate_tokenised_grammar(tokenised_grammar)

	# parse the input expression 
	txt = sys.argv[1]
	r,t = consume('EXPR', tokenised_grammar, txt.replace(' ',''));
	if r is None:
		print 'unable to parse'
	
	else:
		if r:
			print 'parsing stopped at: ' + r
		pprint.pprint(t)
		print(eval_tree(t))
	
def parse_grammar_file(file_name):
	f = open(file_name, 'r')
	try:
		g = {}
		for line in f:
			name, entry = parse_line(line)
			g[name] = entry
		return g
		
	finally:
		f.close()
	
if __name__ == '__main__':
	main()
