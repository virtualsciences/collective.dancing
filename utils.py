import zope.schema.vocabulary
import z3c.form.interfaces
import Acquisition

def aq_append(wrapped, item):
    """Return wrapped with an aq chain that includes `item` at the
    end.
    
      >>> class AQ(Acquisition.Explicit):
      ...     def __init__(self, name):
      ...         self.name = name
      ...     def __repr__(self):
      ...         return '<AQ %s>' % self.name

      >>> one, two, three = AQ('one'), AQ('two'), AQ('three')
      >>> one_of_two = one.__of__(two)
      >>> one_of_two.aq_chain
      [<AQ one>, <AQ two>]
      >>> aq_append(one_of_two, three).aq_chain
      [<AQ one>, <AQ two>, <AQ three>]
    """
    value = item
    for item in reversed(wrapped.aq_chain):
        value = Acquisition.aq_base(item).__of__(value)
    return value

class AttributeToDictProxy(object):
    def __init__(self, wrapped, default=z3c.form.interfaces.NOVALUE):
        super(AttributeToDictProxy, self).__setattr__('wrapped', wrapped)
        super(AttributeToDictProxy, self).__setattr__('default', default)

    def __setitem__(self, name, value):
        self.wrapped[name] = value

    __setattr__ = __setitem__

    def __getattr__(self, name):
        return self.wrapped.get(name, self.default)

class LaxVocabulary(zope.schema.vocabulary.SimpleVocabulary):
    """This vocabulary treats values the same if they're equal.
    """
    def getTerm(self, value):
        same = [t for t in self if t.value == Acquisition.aq_base(value)]
        if same:
            return same[0]
        else:
            raise LookupError(value)