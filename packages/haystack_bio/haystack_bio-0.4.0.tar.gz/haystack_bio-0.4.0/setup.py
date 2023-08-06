#!/usr/bin/env python
"""Description: 
Setup script for Haystack -- Epigenetic Variability and Transcription Factor Motifs Analysis Pipeline
@status:  beta
@version: $Revision$
@author:  Luca Pinello
@contact: lpinello@jimmy.harvard.edu
"""

import os
import sys
import re
from setuptools import setup, Extension
import os
import pickle as cp
import glob
import subprocess as sb
import sys
import platform 
import shutil
from os.path import expanduser
import urllib
import time
from distutils.dir_util import copy_tree


#TO INSTALL HAYSTACK DEPENDECIENS IN A CUSTOM LOCATION SET THE ENV VARIABLE: HAYSTACK_DEPENDENCIES_FOLDER
if os.environ.get('HAYSTACK_DEPENDENCIES_FOLDER'):
	INSTALLATION_PATH=os.environ.get('HAYSTACK_DEPENDENCIES_FOLDER')
else:
	INSTALLATION_PATH='%s/Haystack_dependencies' % os.environ['HOME']

BIN_FOLDER=os.path.join(INSTALLATION_PATH,'bin')

def main():
	if float(sys.version[:3])<2.6 or float(sys.version[:3])>=2.8:
		sys.stdout.write("CRITICAL: Python version must be 2.7!\n")
		sys.exit(1)


	version = re.search(
    	'^__version__\s*=\s*"(.*)"',
    	open('haystack/haystack_common.py').read(),
    	re.M
    	).group(1)
	
	
	if float(sys.version[:3])<2.6 or float(sys.version[:3])>=2.8:
    		sys.stdout.write("ERROR: Python version must be 2.6 or 2.7!\n")
    		sys.exit(1)

	setup( 
		   version=version,
          name = "haystack_bio",
          include_package_data = True,
    	   packages = ["haystack"],
    	   package_dir={'haystack': 'haystack'},
          package_data={'haystack': ['./*']},     
    	   entry_points = {
        	"console_scripts": ['haystack_pipeline = haystack.haystack_pipeline_CORE:main',
          'haystack_hotspots =  haystack.haystack_hotspots_CORE:main',
          'haystack_motifs = haystack.haystack_motifs_CORE:main',
          'haystack_tf_activity_plane = haystack.haystack_tf_activity_plane_CORE:main',
          'haystack_download_genome = haystack.haystack_download_genome_CORE:main',]
           },
          description="Epigenetic Variability and Transcription Factor Motifs Analysis Pipeline",
          author='Luca Pinello',
          author_email='lpinello@jimmy.harvard.edu',
          url='http://github.com/lucapinello/Haystack',
  
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Intended Audience :: Developers',
              'Intended Audience :: Science/Research',              
              'License :: OSI Approved :: BSD License',
              'Operating System :: MacOS :: MacOS X',
              'Operating System :: POSIX',
              'Topic :: Scientific/Engineering :: Bio-Informatics',
              'Programming Language :: Python',
              ],
          install_requires=[
              'numpy>=1.8.2',
              'pandas>=0.13.1',
              'matplotlib>=1.3.1',
              'argparse>=1.3',
              'scipy>=0.13.3',
              'jinja2>=2.7.3',
              'bx-python>=0.7.3',
              ],

          )



def which(program):
	import os
	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			path = path.strip('"')
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

	return None

def check_installation(filename,tool_name,verbose=False):
    if os.path.isfile(filename):
        if verbose:
            sys.stdout.write('%s is/was succesfully installed ' % tool_name)
        return True
    else:
        if verbose:
            sys.stdout.write('Sorry I cannot install %s for you, check you have all the required dependencies and and try again to install HAYSTACK.' % tool_name)
        return False


def check_fimo():
            if not check_installation(os.path.join(BIN_FOLDER,'fimo'),'FIMO',verbose=False):
                sys.stdout.write('\nHAYSTACK requires to install FIMO from the MEME suite(4.11.1)')
                sys.stdout.write('I will download and install for you. Please be patient!')
                os.chdir('dependencies/')
                sb.call('rm -Rf meme_4.11.1 &> /dev/null',shell=True)
                sb.call('rm meme_4.11.1.tar.bz2 &> /dev/null',shell=True)
                urllib.urlretrieve ('http://bcb.dfci.harvard.edu/~lpinello/HAYSTACK/dependencies/meme_4.11.1.tar.bz2','meme_4.11.1.tar.bz2')
                sb.call('tar xvjf meme_4.11.1.tar.bz2',shell=True)                
                
                os.chdir('meme_4.11.1/')

                cmd_cfg='./configure --prefix=%s --enable-build-libxml2 --enable-build-libxslt ' % INSTALLATION_PATH

                sys.stdout.write(cmd_cfg)
                sb.call(cmd_cfg,shell=True)
                #sb.call('make clean',shell=True)
                sb.call('make && make install',shell=True)
                #sb.call('make clean',shell=True)
                os.chdir('..')
                sb.call('rm -Rf meme_4.11.1',shell=True)
                sb.call('rm meme_4.11.1.tar.bz2',shell=True)
                os.chdir('..')   
                #installa fimo
                sys.stdout.write('FIMO should be installed (please check the output)')
            
    	    if not check_installation(os.path.join(BIN_FOLDER,'fimo'),'FIMO'):
             sys.exit(1)

            
def check_samtools():
            if not check_installation(os.path.join(BIN_FOLDER,'samtools'),'SAMTOOLS',verbose=False):
                sys.stdout.write('\nHAYSTACK requires to install SAMTOOLS 0.1.19:http://sourceforge.net/projects/samtools/files/samtools/0.1.19/')
                sys.stdout.write('I will download and install for you. Please be patient!')
                os.chdir('dependencies/')    
                sb.call('rm -Rf samtools-0.1.19 &> /dev/null',shell=True)
                sb.call('rm samtools-0.1.19.tar.bz2 &> /dev/null',shell=True)
                urllib.urlretrieve ('http://bcb.dfci.harvard.edu/~lpinello/HAYSTACK/dependencies/samtools-0.1.19.tar.bz2','samtools-0.1.19.tar.bz2')
                sb.call('tar xvjf samtools-0.1.19.tar.bz2',shell=True)
                os.chdir('samtools-0.1.19/')
                sb.call('make clean',shell=True)
                sb.call('make',shell=True)
                
                try:
                    shutil.copy2('samtools',BIN_FOLDER)
                except:
                    pass
                #sb.call('make clean',shell=True)
                os.chdir('..')
                sb.call('rm -Rf samtools-0.1.19',shell=True)
                sb.call('rm samtools-0.1.19.tar.bz2',shell=True)
                os.chdir('..')         
                
            if not check_installation(os.path.join(BIN_FOLDER,'samtools'),'SAMTOOLS'):
            	sys.exit(1)
            
                
def check_bedtools():
        
        if not check_installation(os.path.join(BIN_FOLDER,'bedtools'),'BEDTOOLS',verbose=False):
            sys.stdout.write('\nHAYSTACK requires to install BEDTOOLS v2.20.1')
            sys.stdout.write('I will download and install for you. Please be patient!')
            os.chdir('dependencies/')  
            sb.call('rm bedtools2-2.20.1.tar.bz2 &> /dev/null',shell=True)   
            sb.call('rm -Rf bedtools2-2.20.1 &> /dev/null',shell=True)             
            urllib.urlretrieve ('http://bcb.dfci.harvard.edu/~lpinello/HAYSTACK/dependencies/bedtools2-2.20.1.tar.bz2','bedtools2-2.20.1.tar.bz2')
            sb.call('tar xvjf bedtools2-2.20.1.tar.bz2',shell=True)
            os.chdir('bedtools2-2.20.1/')
            sb.call('make clean',shell=True)
            sb.call('make',shell=True)
            for filename in glob.glob(os.path.join('bin', '*')):
                shutil.copy(filename, BIN_FOLDER)
            #sb.call('make clean',shell=True)    
            os.chdir('..')
            sb.call('rm -Rf bedtools2-2.20.1',shell=True)
            sb.call('rm bedtools2-2.20.1.tar.bz2',shell=True)
            os.chdir('..')
            
        if not check_installation(os.path.join(BIN_FOLDER,'bedtools'),'BEDTOOLS'):
            sys.exit(1)

            
def check_ghostscript(CURRENT_PLATFORM):

        if (not check_installation(os.path.join(BIN_FOLDER,'gs'),'Ghostscript',verbose=False) and CURRENT_PLATFORM=='Linux') or ( CURRENT_PLATFORM=='Darwin' and which('gs') is None):
            sys.stdout.write('\nHAYSTACK requires to install Ghostscript 9.14')
            
            if CURRENT_PLATFORM=='Linux':
                sys.stdout.write('I will download and install for you. Please be patient!')
                sb.call('rm dependencies/Linux/gs &> /dev/null',shell=True)
                urllib.urlretrieve ('http://bcb.dfci.harvard.edu/~lpinello/HAYSTACK/dependencies/Linux/gs','dependencies/Linux/gs')
                shutil.copy2('dependencies/Linux/gs',BIN_FOLDER)
                time.sleep(3) # we need some time to allow the NFS to sync the file... 		
                sb.call('chmod +x %s' % os.path.join(BIN_FOLDER,'gs'),shell=True)
                sb.call('rm dependencies/Linux/gs',shell=True)
               
                #if not check_installation(os.path.join(BIN_FOLDER,'gs'),'Ghostscript'):
                #    sys.exit(1)
 
            elif CURRENT_PLATFORM=='Darwin': 
                sys.stdout.write('Ok downloading and launching the installer for you!')
                sb.call('rm dependencies/Darwin/Ghostscript-9.14.pkg &> /dev/null',shell=True)
                urllib.urlretrieve ('http://bcb.dfci.harvard.edu/~lpinello/HAYSTACK/dependencies/Darwin/Ghostscript-9.14.pkg','dependencies/Darwin/Ghostscript-9.14.pkg')
                sys.stdout.write('To install Ghostscript I need admin privileges.')
                sb.call('sudo installer -pkg dependencies/Darwin/Ghostscript-9.14.pkg -target /',shell=True)
                sb.call('rm dependencies/Darwin/Ghostscript-9.14.pkg',shell=True)

def install_dependencies(CURRENT_PLATFORM):



   if CURRENT_PLATFORM not in  ['Linux','Darwin'] and platform.architecture()!='64bit':
		sys.stdout.write('Sorry your platform is not supported\n CRISPResso is supported only on 64bit versions of Linux or OSX ')
		sys.exit(1)
   
   if not os.path.exists(INSTALLATION_PATH):
		sys.stdout.write ('OK, creating the folder:%s' % INSTALLATION_PATH)
		os.makedirs(INSTALLATION_PATH)
		os.makedirs(BIN_FOLDER)
   else:
		sys.stdout.write ('\nI cannot create the folder!\nThe folder %s is not empty!' % INSTALLATION_PATH)

		try:
			os.makedirs(BIN_FOLDER)
		except:
			pass


   sys.stdout.write( '\nCHECKING DEPENDENCIES...')
   check_ghostscript(CURRENT_PLATFORM)
   check_fimo()
   check_bedtools()
   check_samtools()


def copy_data(CURRENT_PLATFORM):
    
   
    #coping data in place
    d_path = lambda x: (x,os.path.join(INSTALLATION_PATH,x))
    
    s_path=lambda x: os.path.join(INSTALLATION_PATH,x)
    
    copy_tree(*d_path('genomes'))
    copy_tree(*d_path('gene_annotations'))
    copy_tree(*d_path('motif_databases'))
    copy_tree(*d_path('extra'))
    
    
    if CURRENT_PLATFORM=='Linux':
        src='precompiled_binary/Linux/'
    
    elif CURRENT_PLATFORM=='Darwin':
        src='precompiled_binary/Darwin/'

    dest=BIN_FOLDER
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dest)      
    
    
    #fix permission so people can write in haystack dep folders
    
    sb.call('chmod -R 777 %s' % os.path.join(INSTALLATION_PATH,'genomes'),shell=True)
    sb.call('chmod -R 777 %s' % os.path.join(INSTALLATION_PATH,'gene_annotations'),shell=True)
    sb.call('chmod -R 777 %s' % os.path.join(INSTALLATION_PATH,'motif_databases'),shell=True)
            
    #COPY current env for subprocess
    os.environ['PATH']=('%s:' % BIN_FOLDER) +os.environ['PATH'] #here the order is important
    os.environ['HAYSTACK_DEPENDENCIES_PATH']=INSTALLATION_PATH
    system_env=os.environ
    cp.dump(system_env,open(os.path.join('haystack','system_env.pickle'),'w+'))
	

if __name__ == '__main__':
    if sys.argv[1]=='install':
        
        CURRENT_PLATFORM=platform.system().split('_')[0]
        
        sys.stdout.write ('\n\nInstalling dependencies...')
        install_dependencies(CURRENT_PLATFORM)
        copy_data(CURRENT_PLATFORM)
        sys.stdout.write ('\nInstalling Python package installed')
    main()
    
    if sys.argv[1]=='install':
        sys.stdout.write ('\n\nINSTALLATION COMPLETED, open a NEW terminal and enjoy HAYSTACK!'    )







