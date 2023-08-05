"""
::Juice::

https://github.com/mardix/juice

{project_name}.py

This is the entry point of the application.

--------------------------------------------------------------------------------

** To serve the local development app

> juicy serve {project_name}

#---------

** To deploy with Propel ( https://github.com/mardix/propel )

> propel -w

#---------

** To deploy with Gunicorn

> gunicorn {project_name}:app

"""

from juice import Juice

# Import the project's views
import application.{project_name}.views

# 'app' variable name is required if you intend to use 'juicy' the cli tool
app = Juice(__name__, project="{project_name}")

