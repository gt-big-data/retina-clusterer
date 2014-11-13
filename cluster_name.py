# clusters = ['Politics', 'Sports', 'Technology', 'Arts', 'Justice', 'Travel', 'Dining', 'Health', 'Business', 'World', 'Theater', 'Science', 'US', 'Movies', 'Opinion'];


def cluster_name(clus):
	clus = clus.lower();
	if(clus == 'politics'):
		return 'Politics';
	if(clus == 'sport' or clus == 'sports' or clus == 'worldsport'):
		return 'Sports';
	if(clus == 'technology' or clus == 'tech'):
		return 'Technology';
	if(clus == 'arts'):
		return 'Arts';
	if(clus == 'justice'):
		return 'Justice';
	if(clus == 'travel'):
		return 'Travel';
	if(clus == 'dining'):
		return 'Dining';
	if(clus == 'health'):
		return 'Health';
	if(clus == 'business'):
		return 'Business';
	if(clus == 'asia' or clus == 'world'):
		return 'World';
	if(clus == 'showbiz' or clus == 'theater'):
		return 'Theater';
	if(clus == 'science'):
		return 'Science';
	if(clus == 'us'):
		return 'US';
	if(clus == 'movies'):
		return 'Movies';
	if(clus == 'books' or clus == 'living' or clus == 'nyregion' or clus == 'magazine' or clus == 'opinion'):
		return 'Opinion';
	return '';