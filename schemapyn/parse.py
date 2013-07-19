import pkgutil
import os
import sys

from parsley import makeGrammar

import nodes

from .remove import RemoveNonJAXBAnnotations

import glob


RAW_GRAMMAR = pkgutil.get_data(__name__, 'java.parsley')

GRAMMAR = makeGrammar(RAW_GRAMMAR, nodes.__dict__)


for j in glob.glob(sys.argv[1]):
    if 'Abstract' in j or 'Deserial' in j:
        continue
    with open(j) as f:
        source = [line for line in f if not line.startswith('//')]
        try:
            tree = GRAMMAR('\n'.join(source).strip()).class_file()
            RemoveNonJAXBAnnotations().remove(tree)
            with open(os.path.join('/tmp', os.path.basename(j)), 'w') as cleaned:
                cleaned.write(str(tree))
        except:
            print j
            raise
