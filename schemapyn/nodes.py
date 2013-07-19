from collections import namedtuple


class SetsAttrs(object):

    def __init__(self, *args, **kwargs):
        missing = object()
        attrs = getattr(self.__class__, 'attrs', [])
        for a in attrs:
            value = kwargs.pop(a, missing)
            if value is missing and not hasattr(self, a):
                raise ValueError('missing kwarg: {}'.format(a))
            setattr(self, a, value)
        super(SetsAttrs, self).__init__(*args, **kwargs)

    def __repr__(self):
        cls = self.__class__.__name__
        attrvals = ', '.join('{}={}'.format(a, getattr(self, a))
                             for a in self.attrs)
        return '{}({})'.format(cls, attrvals)


class UnqualifiedName(object):

    @property
    def unqualified_name(self):
        _, _, u = self.name.rpartition('.')
        return u


class PackageName(SetsAttrs, UnqualifiedName):
    attrs = ['name']

    def __str__(self):
        return '{}.*'.format(str(self.name));


class ClassName(SetsAttrs, UnqualifiedName):
    attrs = ['name']

    def __init__(self, **kwargs):
        super(ClassName, self).__init__(**kwargs)

    def __str__(self):
        return str(self.name)


class ImportStmt(SetsAttrs):
    attrs = ['target']

    def __str__(self):
        return 'import {};'.format(str(self.target));


class Argument(SetsAttrs):
    attrs = ['value']

    def __str__(self):
        return str(self.value)


class Array(SetsAttrs):
    attrs = ['elements']

    def __str__(self):
        return '{{{}}}'.format(', '.join(str(s) for s in self.elements))


class String(SetsAttrs):
    attrs = ['value']

    def __str__(self):
        return '"{}"'.format(self.value)


class NamedArgument(SetsAttrs):
    attrs = ['name', 'value']

    def __str__(self):
        return '{}={}'.format(self.name, str(self.value))


class Generic(SetsAttrs):
    attrs = ['name', 'type']

    def __str__(self):
        return '{}<{}>'.format(self.name, str(self.type))


class Annotation(SetsAttrs, UnqualifiedName):
    attrs = ['name', 'arguments']

    def __str__(self):
        args = ", ".join(str(a) for a in self.arguments)
        annotation = '@{}'.format(self.name)
        if args:
            return '{}({})'.format(annotation, args)
        return '{}'.format(annotation)


class FieldDeclaration(SetsAttrs):
    attrs = ['name', 'type', 'visibility', 'static', 'annotations', 'default']

    def __str__(self):
        annotations = '\n'.join(str(a) for a in self.annotations)
        default = ' = {}'.format(self.default) if self.default else ''
        decl = '{} {} {}{};'.format(self.visibility, self.type,
                                    self.name, default)
        return '\n'.join([annotations, decl])


class Block(SetsAttrs):
    attrs = ['body']

    def __str__(self):
        return '{{\n{}\n}}'.format('\n'.join(('\t' + str(el)).replace('\n',
                                                                      '\n\t')
                                             for el in self.body))

class EnumDeclaration(SetsAttrs):
    attrs = ['name', 'visibility', 'static', 'annotations',
             'block']

    def __str__(self):
        annotations = '\n'.join(str(a) for a in self.annotations)
        static = ' static' if self.static else ''

        return '{}\n{}{} enum {} {}'.format(annotations,
                                            self.visibility, static,
                                            self.name,
                                            str(self.block))


class EnumInstantiation(SetsAttrs):
    attrs = ['annotations', 'name', 'args']

    def __str__(self):
        annotations = '\n'.join(str(a) for a in self.annotations)
        if annotations:
            annotations += '\n'
        return '{}{}({})'.format(annotations, self.name, self.args)



class EnumInstantiationGroup(SetsAttrs):
    attrs = ['instantiations']

    def __str__(self):
        return ',\n'.join(str(i) for i in self.instantiations) + ';'



class ClassDeclaration(SetsAttrs):
    attrs = ['name', 'visibility', 'static', 'annotations',
             'super_class', 'block']

    def __str__(self):
        super_class = (' extends {}'.format(self.super_class)
                       if self.super_class else '')
        annotations = '\n'.join(str(a) for a in self.annotations)
        static = ' static' if self.static else ''

        return '{}\n{}{} class {}{} {}'.format(annotations,
                                               self.visibility, static,
                                               self.name, super_class,
                                               str(self.block))


class MethodDeclaration(SetsAttrs):
    attrs = ['name', 'type', 'visibility', 'static', 'annotations',
             'args', 'static', 'block']

    def __str__(self):
        return '{} {} {}({}) {{\n{}}}\n'.format(self.visibility,
                                                self.type,
                                                self.name,
                                                self.args,
                                                self.block)


class Instantiation(SetsAttrs):
    attrs = ['type', 'args']

    def __str__(self):
        return 'new {}({})'.format(self.type, self.args)


class Package(SetsAttrs, UnqualifiedName):
    attrs = ['name']

    def __str__(self):
        return 'package {};'.format(self.name)


class ClassFile(SetsAttrs):
    attrs = ['package', 'imports', 'class_declaration']

    def __str__(self):
        contents = [self.package] + self.imports + [self.class_declaration]
        return '\n'.join(str(s) for s in contents)
