from distutils.core import setup

from distutils.command.install import install

class post_install(install):
    def run(self):
        # Call parent 
        install.run(self)
        # Execute commands
        import os
        print "Running post-install"
        codepath=os.path.join(self.install_libbase,'radioflux')
        ds9path=os.path.join(self.install_data,'ds9','radio-flux.ds9')
        print 'Path to .ds9 file is',ds9path
        os.system('sed -i -e s!REPLACE!'+codepath+'! '+ds9path)
        os.system('chmod +x '+codepath+'/*.py')

setup(name='radioflux',
      author='Martin Hardcastle',
      author_email='mjh@extragalactic.info',
      url='http://www.extragalactic.info/',
      description='Radio flux measurement for ds9',
      download_url = 'https://github.com/mhardcastle/radioflux/tarball/1.2',
      version='1.2',
      packages=['radioflux'],
      data_files=[('ds9',['radio-flux.ds9'])],
      cmdclass={"install": post_install}
      )
