# clusters = ['Politics', 'Sports', 'Technology', 'Arts', 'Justice', 'Travel', 'Dining', 'Health', 'Business', 'World', 'Theater', 'Science', 'US', 'Movies', 'Opinion'];
def cluster_name(clus):
	if isinstance(clus, basestring):
		clus = clus.lower();
		if(clus == 'politics'):
			return 'Politics';
		if(clus == 'sport' or clus == 'sports' or clus == 'worldsport' or clus == 'skiing' or clus == 'horseracing' or clus == 'golf' or clus == 'motorsport' or clus == 'tennis' or clus == 'football' or clus == 'sailing'):
			return 'Sports';
		if(clus == 'technology' or clus == 'tech'):
			return 'Technology';
		if(clus == 'arts' or clus == 'fashion' or clus == 'style'):
			return 'Arts';
		if(clus == 'justice'):
			return 'Justice';
		if(clus == 'travel' or clus == 'intl_travel'):
			return 'Travel';
		if(clus == 'dining'):
			return 'Dining';
		if(clus == 'health'):
			return 'Health';
		if(clus == 'business' or clus == 'jobs' or clus == 'your-money'):
			return 'Business';
		if(clus == 'asia' or clus == 'world' or clus == 'africa' or clus == 'middleeast' or clus == 'europe' or clus == 'intl_world' or clus == 'americas' or clus == 'china'):
			return 'World';
		if(clus == 'showbiz' or clus == 'theater'):
			return 'Theater';
		if(clus == 'science'):
			return 'Science';
		if(clus == 'us'):
			return 'US';
		if(clus == 'movies'):
			return 'Movies';
		if(clus == 'books' or clus == 'living' or clus == 'nyregion' or clus == 'magazine' or clus == 'opinion' or clus == 'opinions' or clus == 'intl_opinion'):
			return 'Opinion';
	return '';
		