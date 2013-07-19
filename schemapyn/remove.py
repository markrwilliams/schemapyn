from .nodes import ClassFile, ImportStmt


class RemoveNonJAXBAnnotations(object):

    def __init__(self):
        self.jaxb = []
        self.to_delete = []

    def remove(self, node):
        if hasattr(node, 'imports'):
            for i in node.imports:
                self.remove(i)
        elif hasattr(node, 'target'):
            if node.target.name.startswith('javax.xml.bind.annotation'):
                self.jaxb.append(node.target.unqualified_name)
        elif hasattr(node, 'annotations'):
            ok = []
            for a in node.annotations:
                if a.name in self.jaxb:
                    ok.append(a)
                else:
                    self.to_delete.append(a.unqualified_name)
            node.annotations = ok

        for possible in ['class_declaration',
                         'block',
                         'body',
                         'instantiations']:
            child = getattr(node, possible, None)
            if child:
                child = [child] if not isinstance(child, list) else child
                for c in child:
                    self.remove(c)

        if isinstance(node, ClassFile):
            ok = []
            for i in node.imports:
                if i.target.unqualified_name not in self.to_delete:
                    ok.append(i)
            node.imports = ok
