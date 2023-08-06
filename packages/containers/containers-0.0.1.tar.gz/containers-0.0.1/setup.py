import setuptools, os

def load_requirements(fname):
  lines = list(open(fname))
  stripped = [line.strip() for line in lines]
  return filter(
    lambda line: line and not line.startswith('#'),
    lines
  )

REQS = load_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'))

ARGS = dict(
  name='containers',
  version='0.0.1',
  description='automatic typed collections in python using decorators',
  author='Abe Winter',
  author_email='awinter.public@gmail.com',
  url='https://github.com/abe-winter/containers',
  license='MIT',
  py_modules=['containers'],
  install_requires=REQS,
)

if __name__ == '__main__':
  setuptools.setup(**ARGS)
