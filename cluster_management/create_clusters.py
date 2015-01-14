from db import app

clusters = ['Politics', 'Sports', 'Technology', 'Arts', 'Justice', 'Travel', 'Dining', 'Health', 'Business', 'World', 'Theater', 'Science', 'US', 'Movies', 'Opinion'];

for cluster in clusters:
	app.createCluster(cluster, []);