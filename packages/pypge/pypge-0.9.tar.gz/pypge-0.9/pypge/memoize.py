from __future__ import print_function

import sympy
sympy.init_printing(use_unicode=True)


class Memoizer:

	def __init__(self, variables):
		self.models = []
		self.mapper = Mapper(variables)
		self.hmap = {}

	def insert(self,model):
		# h = hash(model.orig)
		# print("ORIG: ", h)

		h = model.orig.__hash__()

		r = self.hmap.get(h,None)
		# conflict
		if r is not None:
			return False

		model.id = len(self.models)
		self.models.append(model)
		self.hmap[h] = model
		return True


	def lookup(self,model):
		# expr = model.orig
		# h = hash(expr)
		h = model.orig.__hash__()
		r = self.hmap.get(h,None)
		if r is None:
			return False,None
		else:
			return True,r



	def encode(self,expr):
		# print expr
		iis = []
		ffs = []
		for i,e in enumerate(sympy.preorder_traversal(expr)):
			# print i, e.func
			ii, ff = self.mapper.get(e)
			iis = iis + ii
			if ff is not None:
				iis.append(len(ffs))
				ffs = ffs + ff
			# print "   ", ii, ff
		return iis, ffs

	def get_by_id(self, i):
		return self.models[i]


class Mapper:

	def __init__(self, variables):
		self.variables = variables
		self.coeffs = sympy.symbols("C C_0:128")
		self.map = {
			## the Leaf types

			# Symbol: self.map_symbol,
			# Constant 'C_#': 1
			# Float '#.#': 2
			# Time 'T': 3
			# System 'S_#': 4
			# Variable 'X_#': 5
			# Derivative 'dX_#': 6

			sympy.numbers.NegativeOne: -1,


			## the Node types
			
			# Mul: 8,  ++ num children
			# Add: 9,  ++ num children
			sympy.Pow: 10,
			# Div: 11,

			sympy.Abs: 12,
			sympy.sqrt: 13,
			sympy.log: 14,
			sympy.exp: 15,

			sympy.cos: 16,
			sympy.sin: 17,
			sympy.tan: 18,
			
		}
		# print self.variables
		# print self.coeffs

	def get(self,expr):
		e = expr.func
		
		if e is sympy.Mul:
			return [8,len(expr.args)], None
		if e is sympy.Add:
			return [9,len(expr.args)], None
		
		if e is sympy.Symbol:
			return self.map_symbol(expr), None

		if e is sympy.Integer or e is sympy.numbers.Zero or e is sympy.numbers.One or e is sympy.numbers.Half:
			return [2, int(expr.evalf(0))], None

		if e is sympy.Float or e is sympy.numbers.Pi:
			return [2], [expr.evalf(8)]
		
		ii = [self.map[e]]
		return ii, None

	def map_symbol(self,expr):
		# print "SYMBOL: ", expr
		if expr in self.variables:
			idx = self.variables.index(expr)
			return [5,idx]
		if expr in self.coeffs:
			idx = self.coeffs.index(expr)
			return [1,idx-1]

		return [-2]



# class Node:

# 	def __init__(self, key=0, value=None):
# 		self.map = {}
# 		self.key = key
# 		self.value = value


# 	def get_key(self):
# 		return self.key

# 	def get_value(self):
# 		return self.value

# 	def insert(self,iis, value):
# 		# print "  processing: ", iis
# 		# print "    ", self.key, self.map
# 		if len(iis) > 1:
# 			ii = iis[0]
# 			if ii not in self.map:
# 				# print "  new node for key: ", ii
# 				self.map[ii] = Node(key=ii)
# 			return self.map[ii].insert(iis[1:], value)
# 		if len(iis) == 1:
# 			ii = iis[0]
# 			if ii not in self.map:
# 				# print "  new node for key: ", ii
# 				self.map[ii] = Node(key=ii, value=value)
# 				return True
# 			else:
# 				return False
# 		return False

# 	def lookup(self,iis):
# 		if len(iis) > 1:
# 			ii = iis[0]
# 			if ii in self.map:
# 				return self.map[ii].lookup(iis[1:])
# 			else:
# 				return False, None
# 		if len(iis) == 1:
# 			ii = iis[0]
# 			if ii in self.map:
# 				return True, self.map[ii].get_value()
# 			else:
# 				return False, None
# 		return False, None

