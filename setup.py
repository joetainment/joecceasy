import os, platform, shutil
from setuptools import setup

import joecceasy
Easy = joecceasy.Easy
Easy.CdToScriptDir()

#assert platform.system()=="Linux"
#assert os.name=='posix'

def runSetup():
    setup(
        name='joecceasy',
        version='0.0.1rc1',    
        description='Make Python Easy',
        url='https://github.com/joetainment/joecceasy',
        author='Joe Crawford',
        author_email='joecceasy@teaching3d.com',
        license='MIT License',
        long_description_content_type='text/markdown',
        packages=['joecceasy'],
        package_data={
            # "" :   means all packages  , otherwise use "packagename":
            #"": ["*.txt"],
            # And include any *.dat files found in the "data" subdirectory
            # of the "mypkg" package, also:
            "joecceasy": [ "*", "submodules/*", "easy/*" ],
        },
        exclude_package_data={"joecceasy": [
            "*/*gitignore*",
            "*/*gitignore*",
            "__pycache__",
            "*/__pycache__",
        ]},
        include_package_data=True,
        install_requires=[],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License', 
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX', 
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX :: BSD', 
            'Programming Language :: Python :: 3',
        ],
    )
    

doContinue = True

try:
    assert not os.path.exists( 'joecceasy/README.md' )
    shutil.copy2( 'README.md', 'joecceasy/README.md')
except:
    doContinue = False
    Easy.Ptb()
    
if doContinue:    
    try:
        runSetup()
    except:
        Easy.Ptb()
    else:
        print('call to setup func did not throw exception')
    
    os.remove( 'joecceasy/README.md' )


print('made it to end of setup.py script')
