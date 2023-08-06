"""This is the nester.py module sample list with 2 degrees of nesting"""

def list_frame(movie_list):
	for movie in movie_list:
		if isinstance(movie, list):
			list_frame(movie)
		else:
			print(movie)