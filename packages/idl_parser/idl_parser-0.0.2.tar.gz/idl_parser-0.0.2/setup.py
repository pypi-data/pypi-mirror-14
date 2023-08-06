from setuptools import setup, find_packages
import sys



long_description = '''
"""
idl_parser package example
"""

from idl_parser import parser
parser_ = parser.IDLParser()
idl_str = """
module my_module {
  struct Time {
    long sec;
    long usec;
  };

  typedef sequence<double> DoubleSeq;

  struct TimedDoubleSeq {
    Time tm;
    DoubleSeq data;
  };

  enum RETURN_VALUE {
    RETURN_OK,
    RETURN_FAILED,
  };

  interface DataGetter {
    RETURN_VALUE getData(out TimedDoubleSeq data);
  };

};
"""

global_module = parser_.load(idl_str)
my_module = global_module.module_by_name('my_module')
dataGetter = my_module.interface_by_name('DataGetter')
print 'DataGetter interface'
for m in dataGetter.methods:
  print '- method:'
  print '  name:', m.name
  print '  returns:', m.returns.name
  print '  arguments:'
  for a in m.arguments:
    print '    name:', a.name
    print '    type:', a.type
    print '    direction:', a.direction

doubleSeq = my_module.typedef_by_name('DoubleSeq')
print 'typedef %s %s' % (doubleSeq.type.name, doubleSeq.name)

timedDoubleSeq = my_module.struct_by_name('TimedDoubleSeq')
print 'TimedDoubleSeq'
for m in timedDoubleSeq.members:
  print '- member:'
  print '  name:', m.name
  print '  type:', m.type.name   
'''

setup(name='idl_parser',
      version='0.0.2',
      url = 'http://www.sugarsweetrobotics.com/',
      author = 'ysuga',
      author_email = 'ysuga@ysuga.net',
      description = 'OMG IDL Parser',
      long_description = long_description,
      download_url = 'https://github.com/sugarsweetrobotics/idl_parser',
      packages = ["idl_parser"],
      #py_modules = ["pepper_kinematics"],
      license = 'GPLv3',
      install_requires = [''],
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        ],
      #test_suite = "foo_test.suite",
      #package_dir = {'': 'src'}
    )
