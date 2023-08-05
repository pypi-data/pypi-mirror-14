import setuptools
import os
if os.environ.get('USER','') == 'vagrant':
	del os.link
setuptools.setup(
        setup_requires=['pbr'],
        pbr=True)
#setup(
#        name = 'demo',
#        version  = '0.3',
#        packages = find_packages('src'), 
#        package_dir = {'':'src'},
#        package_data = {
#                '':['*.txt'],
#                'demo':['data/*.dat'],
#            },
#        entry_points = {
#                'console_scripts':[
#                    'foo = cmd.api:main',  
#                    'bar = demo.hello:hello',  
#                    ],
#                'gui_scripts':[
#                    'baz = demo.hello:hello',
#                    ],
#            }
#        )
