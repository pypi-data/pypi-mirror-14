
import lxml.builder
from bl.dict import Dict

class ElementMaker(lxml.builder.ElementMaker):
    """Our ElementMaker unpacks lists when it is called, enabling it to work with 
    nested-list-returning transformations using .xt.Transformer."""
    
    def __call__(self, tag, *children, **attrib):
        chs = []
        for ch in children:
            if type(ch)==list:
                chs += [c for c in ch]
            elif ch is not None:
                chs.append(ch)
        return lxml.builder.ElementMaker.__call__(self, tag, *chs, **attrib)

class XBuilder(Dict):
    """create a set of ElementMaker methods all bound to the same object."""
    def __init__(self, default=None, nsmap=None, **namespaces):
        Dict.__init__(self)
        for k in namespaces:        # each namespace gets its own method, named k (for each k)
            kdefault = default or namespaces[k]
            if nsmap is None:
                knsmap = {None:kdefault}
                knsmap.update(**{km:namespaces[km] for km in namespaces if namespaces[km]!=kdefault})
            self[k] = ElementMaker(namespace=namespaces[k], nsmap=nsmap or knsmap)
        if default is not None:
            # create an ElementMaker that uses the given namespace as the default
            if nsmap is None:
                knsmap = {None:default}
                knsmap.update(**{km:namespaces[km] for km in namespaces if namespaces[km]!=default})            
            self._ = ElementMaker(namespace=default, nsmap=nsmap or knsmap)
        else:
            # make elements with no namespace by default
            self._ = ElementMaker() 

    @classmethod
    def single(c, namespace):
        """An element maker with a single namespace that uses that namespace as the default"""
        return c(default=namespace)._
