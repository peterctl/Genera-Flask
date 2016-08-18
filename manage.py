import sqlalchemy as sa

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import _BoundDeclarativeMeta as BDA

from app import app
from app.models import db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('runserver', Server(port=8000))
manager.add_command('db', MigrateCommand)

@manager.command
def createroles(verbose=False, cleardb=False):
	"""Create auth roles as defined in config.auth"""

	if cleardb:
		clear(verbose=verbose)

	from config.auth import roles
	from scripts.auth import create_or_update_role
	for role in roles:
		create_or_update_role(role)
		if verbose:
			print role['key']
			for perm in role['permissions']:
				print '  %s' % perm

@MigrateCommand.command
def clear(verbose=False):
	"""Clear all entries in the database."""

	models = [m for m in db.Model._decl_class_registry.values()
		if isinstance(m, BDA)]

	for Model in models:
		deleted = 0
		for instance in Model.all():
			instance.delete()
			deleted += 1
		if verbose:
			print "Deleted from %s: %s" % (Model.__tablename__, deleted)

	db.session.commit()

if __name__ == '__main__':
	manager.run()
