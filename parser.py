import re, sys

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
	if symbol in g:
		alternatives = g[symbol]
		matching_alt = None
		remainder = None
		for alt in alternatives:
			all_tokens_in_alt_match = True
			remainder = txt
			for token in alt:
				remainder = consume(token, g, remainder)
				if remainder is None:
					all_tokens_in_alt_match = False
					break
					
			if all_tokens_in_alt_match:
				matching_alt = alt
				break
		
		if matching_alt:
			return remainder
			
		else:
			return None
					
	else:
		match = re.match(symbol, txt)
		if match:
			matching_txt = match.group(0)
			return txt[len(matching_txt):]
		else:
			return None
						
def main():
	tokenised_grammar = parse_grammar_file('grammar.txt')
	validate_tokenised_grammar(tokenised_grammar)
	txt = sys.argv[1]

	r = consume('EXPR', tokenised_grammar, txt);
	if r is None:
		print 'unable to parse'
	else:
		print 'remainder=' + r
	
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