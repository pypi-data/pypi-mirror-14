
import os
import json
import logging
import platform
from pybythec import utils

log = logging.getLogger('pybythec')


class BuildElements:
  
  def __init__(self, argv):
    '''
      argv (input): a list of arguments with a flag, value pairing ie ['-c', 'gcc'] (where -c is the flag and gcc is the value)
    '''
    
    # get any arguments passed in
    if type(argv) is not list:
      raise Exception('args must be a list, not a {0}'.format(argv))
      
    # TODO: if the first argument is a valid path, ignore it (might allow for leaving out '' as the first argument in some circumstances) 
    
    self.target = ''
    self.binaryType = ''         # executable, staticLib, dynamicLib, plugin
    self.compiler = ''           # gcc-4.4 gcc clang msvc110 etc
    self.osType = ''             # linux, osx, windows
    self.binaryFormat = '64bit'  # 32bit, 64bit etc
    self.buildType = 'debug'     # debug, release etc

    self.multithread = True
    
    self.locked = False
    
    self.installPath = '.build'
    
    self.sources = []
    self.libs    = []
    self.defines = []
    self.flags = []
    self.linkFlags = []
    
    self.incPaths = []
    self.libPaths = []
    self.libSrcPaths = []
    self.keys = []
    
    self.qtClasses = []
    
    self.libInstallPathAppend = True
    self.plusplus = True
    
    #
    # parse the args
    #
    args = dict()
    key = str()
    keyFound = False

    for arg in argv[1:]:
      if keyFound:
        args[key] = arg
        keyFound = False
        continue
      if arg == '-cl' or arg == '-cla': # cleaning
        args[arg] = ''
      elif arg == '-c' or arg == '-os' or arg == '-b' or arg == '-bf' or arg == '-d' or arg == '-p':
        key = arg
        keyFound = True
      else:
        raise Exception(
          '\nvalid arguments:\n\n'
          '-c   compiler: any variation of gcc, clang, or msvc\n'
          '-os  operating system: currently linux, osx, or windows\n'
          '-b   build type: debug release etc \n'
          '-bf  binary format: 32bit, 64bit etc\n'
          '-d   directory of the library being built, to be used when building a library as a dependency (ie from a project)\n'
          '-p   path to a pybythec project config file (json format)\n'
          '-cl  clean the build\n'
          '-cla clean the build as well as the builds of any library dependencies\n'
        )

    self.cwDir = os.getcwd()
    if '-d' in args:
      self.cwDir = args['-d']
  
    # json config files
    globalCf  = None
    projectCf = None
    localCf   = None
  
    # global config
    if 'PYBYTHEC_GLOBALS' in os.environ:
      globalCf = utils.loadJsonFile(os.environ['PYBYTHEC_GLOBALS'])
    if not globalCf and '-g' in args:
      globalCf = utils.loadJsonFile(args['-g'])
    if not globalCf:
      globalCf = utils.loadJsonFile('.pybythecGlobal.json')
  
    # project config
    if 'PYBYTHEC_PROJECT' in os.environ:
      projectCf = os.environ['PYBYTHEC_PROJECT']
    elif '-p' in args:
      projectCf = utils.loadJsonFile(args['-p'])
    else:
      projectCf = utils.loadJsonFile('.pybythecProject.json')
  
    # local config
    localConfigPath = self.cwDir + '/.pybythec.json'
    if os.path.exists(localConfigPath):
      localCf = utils.loadJsonFile(localConfigPath)
      
    if globalCf is not None:
      self._getBuildElements(globalCf)
    if projectCf is not None:
      self._getBuildElements(projectCf)
    if localCf is not None:
      self._getBuildElements(localCf)
        
    # command line overrides
    if '-c' in args:
      self.compiler = args['-c']
    
    if '-os' in args:
      self.osType = args['-os']
    
    if '-b' in args:
      self.buildType = args['-b']
    
    if '-bf' in args:
      self.binaryFormat = args['-bf']
    
    # currently compiler root can either be gcc, clang or msvc
    self.compilerRoot = self.compiler
    if self.compilerRoot.startswith('gcc') or self.compilerRoot.startswith('g++'):
      self.compilerRoot = 'gcc'
    elif self.compilerRoot.startswith('clang') or self.compilerRoot.startswith('clang++'):
      self.compilerRoot = 'clang'
    elif self.compilerRoot.startswith('msvc'):
      self.compilerRoot = 'msvc'
    
    self.keys = ['all', self.compilerRoot, self.compiler, self.osType, self.binaryType, self.buildType, self.binaryFormat]
    if self.multithread:
      self.keys.append('multithread')
  
    if globalCf is not None:
      self._getBuildElements2(globalCf)
    if projectCf is not None:
      self._getBuildElements2(projectCf)
    if localCf is not None:
      self._getBuildElements2(localCf)
    
    # if osType is not specified use the current one
    if not len(self.osType):
      if platform.system() == 'linux':
        self.osType = 'linux'
      elif platform.system() == 'Darwin':
        self.osType = 'osx'
      elif platform.system() == 'Windows':
        self.osType = 'windows'
      else:
        raise Exception('no os specified and current os does not appear to be Linux, OS X or Windows')
    
    # if a compiler isn't specified try to choose an appropiate default compiler
    if not len(self.compiler):
      if platform.system() == 'linux':
        self.compiler = 'g++'
      elif platform.system() == 'Darwin':
        self.compiler = 'clang++'
      elif platform.system() == 'Windows':
        self.compiler = 'msvc'
      else:
        raise Exception('no compiler specified and current os does not appear to be Linux, OS X or Windows')
    
    if not len(self.target):
      raise Exception('no target specified')
    elif not len(self.binaryType):
      raise Exception('no binary type specified')
    elif not len(self.binaryFormat):
      raise Exception('no binary format specified')
    elif not len(self.buildType):
      raise Exception('no build type specified')
    elif not len(self.sources):
      raise Exception('no source files specified')
    
    #
    # compiler config
    #
    self.compilerCmd = self.compiler
    self.linker      = ''
    self.targetFlag  = ''
    self.libFlag     = ''
    self.libPathFlag = ''
    self.objExt      = ''
    self.objPathFlag = ''
    
    self.staticLibExt  = ''
    self.dynamicLibExt = ''
    self.pluginExt     = ''
    
    #
    # gcc / clang
    #
    if self.compilerRoot == 'gcc' or self.compilerRoot == 'clang':
      
      if not self.plusplus: # if forcing plain old C (in the case of a library being built as a dependency that is only C compatible)
        if self.compilerRoot == 'gcc':
          self.compilerCmd = self.compilerCmd.replace('g++', 'gcc')
        elif self.compilerRoot == 'clang':
          self.compilerCmd = self.compilerCmd.replace('clang++', 'clang')
      
      self.objFlag     = '-c'
      self.objExt      = '.o'
      self.objPathFlag = '-o'
      self.defines.append('_' + self.binaryFormat.upper()) # TODO: you sure this is universal?
        
      # link
      self.linker        = self.compilerCmd # 'ld'
      self.targetFlag    = '-o'
      self.libFlag       = '-l'
      self.libPathFlag   = '-L'
      self.staticLibExt  = '.a'
      self.dynamicLibExt = '.so'
      self.pluginExt     = '.so'
      if self.osType == 'osx' and isClang: # TODO: it's not clang that determines this, should have a var called osxConventions or something like that
        self.dynamicLibExt = '.dylib'
        self.pluginExt = '.bundle'
        
      if self.binaryType == 'staticLib' or self.binaryType == 'dynamicLib':
        self.target = 'lib' + self.target
  
      if self.binaryType == 'executable':
        pass
      elif self.binaryType == 'staticLib':
        self.target = self.target + '.a'
        self.linker = 'ar'
        self.targetFlag = 'r'
      elif self.binaryType == 'dynamicLib':
        self.target = self.target + self.dynamicLibExt
      elif self.binaryType == 'plugin':
        self.target = self.target + self.pluginExt
      else:
        raise Exception('unrecognized binary type: {0}'.format(self.binaryType))

    #
    # msvc / msvc
    #
    elif self.compilerRoot == 'msvc':
        
      # compile
      self.compilerCmd = 'cl'
      self.objFlag     = '/c'
      self.objExt      = '.obj'
      self.objPathFlag = '/Fo'
      
      # link
      self.linker        = 'link'
      self.targetFlag    = '/OUT:'
      self.libFlag       = ''
      self.libPathFlag   = '/LIBPATH:'
      self.staticLibExt  = '.lib'
      self.dynamicLibExt = '.dll'
      if self.binaryFormat == '64bit':
        self.linkFlags.append('/MACHINE:X64')
      
      if self.binaryType == 'executable':
        self.target += '.exe'
      elif self.binaryType == 'staticLib':
        self.target += self.staticLibExt
        self.linker = 'lib'
      elif self.binaryType == 'dynamicLib' or self.binaryType == 'plugin':
        self.target += self.dynamicLibExt
        self.linkFlags.append('/DLL')
      else:
        raise Exception('unrecognized binary type: ' + self.binaryType)

    else:
      raise Exception('unrecognized compiler root: ' + self.compilerRoot)


    #
    # determine paths
    #
    self.installPath = utils.makePathAbsolute(self.cwDir, os.path.expandvars(self.installPath))
    self._resolvePaths(self.cwDir, self.sources)
    self._resolvePaths(self.cwDir, self.incPaths)
    self._resolvePaths(self.cwDir, self.libPaths)
    self._resolvePaths(self.cwDir, self.libSrcPaths)

    self.binaryRelPath = '/{0}/{1}/{2}'.format(self.buildType, self.compiler, self.binaryFormat)
    
    self.buildPath = utils.makePathAbsolute(self.cwDir, './.build' + self.binaryRelPath)
          
    if self.libInstallPathAppend and (self.binaryType == 'staticLib' or self.binaryType == 'dynamicLib'):
      self.installPath += self.binaryRelPath
          
    self.targetInstallPath = os.path.join(self.installPath, self.target)


  def _getBuildElements(self, configObj):
    if 'target' in configObj:
      self.target = configObj['target']
    
    if 'binaryType' in configObj:
      self.binaryType = configObj['binaryType']
    
    if 'compiler' in configObj:
      self.compiler = configObj['compiler']

    if 'osType' in configObj:
      self.osType = configObj['osType']
    
    if 'buildType' in configObj:
      self.buildType = configObj['buildType']
    
    if 'binaryFormat' in configObj:
      self.binaryFormat = configObj['binaryFormat']
    
    if 'libInstallPathAppend' in configObj:
      self.libInstallPathAppend = configObj['libInstallPathAppend']
    
    if 'plusplus' in configObj:
      self.plusplus = configObj['plusplus']
    
    if 'multithread' in configObj:
      self.multithread = configObj['multithread']
      
    if 'locked' in configObj:
      self.locked = configObj['locked']
      
    
  def _getBuildElements2(self, configObj):
  
    separartor = ':'
    if platform.system() == 'Windows':
      separartor = ';'
    
    # TODO: PATH will grow  for any build with dependencies, is there a way to prevent it?
    if 'bins' in configObj:
      bins = []
      self._getArgsList(bins, configObj['bins'])
      for bin in bins:
        os.environ['PATH'] = bin + separartor + os.environ['PATH']
        # print('\nappending {0}\n'.format(bin))

    if 'sources' in configObj:
      self._getArgsList(self.sources, configObj['sources'])
    
    if 'libs' in configObj:
      self._getArgsList(self.libs, configObj['libs'])
    
    if 'defines' in configObj:
      self._getArgsList(self.defines, configObj['defines'])
      
    if 'flags' in configObj:
      self._getArgsList(self.flags, configObj['flags'])
      
    if 'linkFlags' in configObj:
      self._getArgsList(self.linkFlags, configObj['linkFlags'])
      
    if 'incPaths' in configObj:
      self._getArgsList(self.incPaths, configObj['incPaths'])
      
    if 'libPaths' in configObj:
      self._getArgsList(self.libPaths, configObj['libPaths'])

    if 'libSrcPaths' in configObj:
      self._getArgsList(self.libSrcPaths, configObj['libSrcPaths'])

    if 'qtClasses' in configObj:
      self._getArgsList(self.qtClasses, configObj['qtClasses'])

    if 'installPath' in configObj:
      installPaths = []
      self._getArgsList(installPaths, configObj['installPath'])
      if len(installPaths):
        self.installPath = installPaths[0]


  def _resolvePaths(self, absPath, paths):
    i = 0
    for path in paths:
      paths[i] = utils.makePathAbsolute(absPath, os.path.expandvars(path))
      i += 1


  def _getArgsList(self, argsList, args):
    '''
      recursivley parses args and appends it to argsList if it has any of the keys
      args can be a dict, str (space-deliminated) or list
    '''    
    if type(args).__name__ == 'dict':
      for key in self.keys:
        if key in args:
          self._getArgsList(argsList, args[key])
    else:
      if type(args).__name__ == 'str' or type(args).__name__ == 'unicode':
        # args = args.split()
        argsList.append(args)
      elif type(args).__name__ == 'list':
        for arg in args:
          argsList.append(arg)

