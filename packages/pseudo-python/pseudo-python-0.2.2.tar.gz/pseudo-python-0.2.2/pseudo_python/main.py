#!/usr/bin/env python3

import sys
import pseudo_python
import pseudo_python.errors
import yaml
import pseudo
import pseudo.errors
from colorama import init
from termcolor import colored

USAGE = '''
pseudo-python <input-filename.py> [<language>]

where if you omit <language>, pseudo-python will generate a 
<input-filename.pseudo.yaml> file with serialized ast 

<language> can be:
  py / python 
  rb / ruby
  js / javascript
  cs / csharp
  go
'''

def main():
    if len(sys.argv) == 1:
        print(USAGE)
        return

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        source = f.read()
    base = filename.partition('.')[0]
    try:
        if len(sys.argv) == 2:
            yaml.Dumper.ignore_aliases = lambda *args : True
            clj = yaml.dump(pseudo_python.translate(source))
            # clj = yaml.dump(translate(source))
            with open('%s.pseudo.yaml' % base, 'w') as f:
                f.write(clj)
        else:
            language = sys.argv[2]
            if language not in pseudo.SUPPORTED_FORMATS:
                print(colored('%s is not supported' % language, 'red'))
                exit(1)
            node = pseudo_python.translate(source)
            # node = translate(source)
            output = pseudo.generate(node, language)
            with open('%s.%s' % (base, pseudo.FILE_EXTENSIONS[language]), 'w') as f:
                f.write(output)     
            print(colored('OK\nsaved as %s.%s' % (base, pseudo.FILE_EXTENSIONS[language]), 'green'))
    except pseudo_python.errors.PseudoError as e:
    # except errors.PseudoError as e:
        print(colored(e, 'red'))
        if e.suggestions:
            print(colored(e.suggestions, 'green'))
        if e.right:
            print(colored('\nright:\n%s' % e.right, 'green'))
        if e.wrong:
            print(colored('\nwrong:\n%s' % e.wrong, 'red'))
    except pseudo.errors.PseudoError as e:
        print(colored('Pseudo error:\n%s' % e, 'red'))

if __name__ == '__main__':
    main()
