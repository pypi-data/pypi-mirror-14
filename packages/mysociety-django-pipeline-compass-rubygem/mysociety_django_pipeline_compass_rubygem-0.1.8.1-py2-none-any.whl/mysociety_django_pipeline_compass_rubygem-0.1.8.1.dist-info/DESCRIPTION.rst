django-pipeline-compass-rubygem is a Compass compiler for django-pipeline using the original Compass Ruby Gem.

Home-page: https://github.com/mysociety/django-pipeline-compass-rubygem
Author: Matthew Somerville
Author-email: matthew@mysociety.org
License: MIT License
Description: Django Pipeline Compass
        =======================
        
        `Compass`_ compiler for django-pipeline using the original Ruby Gem.
        
        Requirements
        ------------
        
        * Compass: ``gem install compass``
        
        Installation
        ------------
        
        .. code-block:: bash
        
            # from PyPi
            $ pip install django-pipeline-compass-rubygem
        
            # from GitHub
            $ pip install git+https://github.com/mila-labs/django-pipeline-compass-rubygem.git
        
        Usage
        -----
        
        COMPASS_BINARY and COMPASS_ARGUMENTS can be either a string or a list/tuple.
        
        .. code-block:: python
        
            # settings.py
        
            PIPELINE['COMPASS_BINARY'] = '/usr/local/bin/compass'        # default: ['/usr/bin/env', 'compass']
            PIPELINE['COMPASS_ARGUMENTS'] = ['-c', 'path/to/config.rb']  # default: []
        
            PIPELINE['COMPILERS'] = (
              'pipeline_compass.compass.CompassCompiler',
            )
        
        .. _Compass: http://compass-style.org/
        
Platform: OS Independent
Classifier: Environment :: Web Environment
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Python
Classifier: Framework :: Django
Classifier: Topic :: Utilities
