# clusters = ['Politics', 'Sports', 'Technology', 'Arts', 'Justice', 'Travel', 'Dining', 'Health', 'Business', 'World', 'Theater', 'Science', 'US', 'Movies', 'Opinion'];


def cluster_name(clus):
	clus = clus.lower();
	if(clus == 'politics'):
		return 'Politics';
	if(clus == 'sport' || clus == 'sports' || clus == 'worldsport'):
		return 'Sports';
	if(clus == 'technology' || clus == 'tech'):
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
	if(clus == 'asia' || clus == 'world'):
		return 'World';
	if(clus == 'showbiz' || clus == 'theater'):
		return 'Theater';
	if(clus == 'science'):
		return 'Science';
	if(clus == 'us'):
		return 'US';
	if(clus == 'movies'):
		return 'Movies';
	if(clus == 'books' || clus == 'living' || clus == 'nyregion' || clus == 'magazine' || clus == 'opinion'):
		return 'Opinion';
	return '';