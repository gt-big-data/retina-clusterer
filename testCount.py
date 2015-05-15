from db import app

count = app.db.cleanarticles.find({"img": {'$exists': True}}).count()

print count