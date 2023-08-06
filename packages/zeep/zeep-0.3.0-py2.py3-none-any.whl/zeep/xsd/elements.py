from lxml import etree


class Base(object):

    @property
    def is_optional(self):
        return self.min_occurs == 0


class Any(Base):
    def __init__(self, max_occurs=1, min_occurs=1):
        self.name = 'any'
        self.max_occurs = max_occurs
        self.min_occurs = min_occurs

        # cyclic import
        from zeep.xsd.builtins import AnyType
        self.type = AnyType()

    def render(self, parent, value):
        assert parent is not None
        if value is None and self.is_optional:
            return
        if isinstance(value.value, list):
            for val in value.value:
                value.xsd_type.render(parent, val)
        else:
            value.xsd_type.render(parent, value.value)

    def __call__(self, any_object):
        return any_object


class Element(Base):
    def __init__(self, name, type_=None, min_occurs=1, max_occurs=1):
        self.name = name.localname if name else None
        self.qname = name
        self.type = type_
        self.min_occurs = min_occurs
        self.max_occurs = max_occurs
        # assert type_

    def __repr__(self):
        return '<%s(name=%r, type=%r)>' % (
            self.__class__.__name__, self.name, self.type)

    def serialize(self, value):
        return self.type.serialize(value)

    def resolve_type(self, schema):
        self.type = self.type.resolve(schema)

    def render(self, parent, value):
        assert parent is not None
        assert self.name is not None

        if value is None and self.is_optional:
            return

        node = etree.SubElement(parent, self.qname)
        return self.type.render(node, value)

    def parse(self, value):
        return self.type.parse_xmlelement(value)

    def __call__(self, *args, **kwargs):
        return self.type(*args, **kwargs)


class Attribute(Element):
    def render(self, parent, value):
        value = self.type.xmlvalue(value)
        parent.set(self.qname, value)


class ListElement(Element):

    def __call__(self, *args, **kwargs):
        return [self.type(*args, **kwargs)]

    def serialize(self, value):
        if value:
            return [self.type.serialize(val) for val in value]
        return []

    def render(self, parent, value):
        for val in value:
            node = etree.SubElement(parent, self.qname)
            self.type.render(node, val)


class GroupElement(Element):
    def __init__(self, *args, **kwargs):
        self.children = kwargs.pop('children', [])
        assert self.children
        super(GroupElement, self).__init__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        for item in self.properties():
            yield item

    def properties(self):
        return self.children


class RefElement(object):

    def __init__(self, tag, ref, schema):
        self._ref = ref
        self._schema = schema

    @property
    def _elm(self):
        return self._schema.get_element(self._ref)

    def __iter__(self, *args, **kwargs):
        elm = self._elm
        for item in elm.properties():
            yield item

    def __call__(self, *args, **kwargs):
        return self._elm(*args, **kwargs)

    def __getattr__(self, name):
        if not name.startswith('_'):
            return getattr(self._elm, name)
        return getattr(self, name)
