from score.db import create_base
from sqlalchemy_utils import force_auto_coercion


# the next line (force_auto_coercion) fixes an issue with sqlalchemy_utils
# password fields:
# http://stackoverflow.com/questions/27860766/column-update-not-being-commited-in-sqlalchemy-sqlalchemy-utils
force_auto_coercion()
Storable = create_base()
