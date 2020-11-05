class image:
	def __init__(self, name, version, matrix ):
		self.name = name
		self.version = version
		self.matrix = matrix
		self.hauteur = len(matrix)
		self.largeur = len(matrix[0])
		self.vecteur