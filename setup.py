from distutils.core import setup
import py2exe


setup(name='Hammertime',
      version='1.0.2',
      description='A point and click pygame',
      author='Ivan Hromada',
      packages=['hammertime'],
      console=['run_HT.py'],
      data_files=[('graphics', ['graphics/forest2.png',
                                'graphics/squirrel_hammerSpriteSheet1.png']),
                  ('sounds', ['sounds/HammerTheme1.ogg']),
                  ('highscore', ['highscore/high_score.txt'])]    
      )
