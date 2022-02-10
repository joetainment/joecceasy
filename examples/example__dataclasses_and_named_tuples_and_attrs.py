#### Dataclasses Named Tupled and Attrs - Easy Data Structures For Python
##     this doc intended primarily as quick reference
##
##     See end of this doc for notes and snippets from official docs
##
## most useful example from here:  https://www.attrs.org/en/stable/examples.html

from joecceasy import Easy ; #Easy.Init()




@Easy.DataClass
class MyDataClass:
    simple: bool = True
    dataclassesAreTheOnlyOption: bool = False
    thisCouldBeAnything: object = None

myDataInstance = MyDataClass( )
Easy.Ic( myDataInstance )




Point2d = Easy.NamedTuple(
    'Point2d',
        ['x',
         'y'])

point2d = Point2d( 5, -2 )
Easy.Ic( point2d )




@Easy.Mods.attrs.define
class AttrsExample_Empty:
    pass

Easy.PrintLoop(
  " AttrsExample_Empty instance comparisons",
  "\n   Equality should be True  ",
  AttrsExample_Empty() == AttrsExample_Empty(),
  "\n   Identity should be False  ",
  AttrsExample_Empty() is AttrsExample_Empty()
)
attrsEmpty = AttrsExample_Empty
Easy.Ic( attrsEmpty )




@Easy.Mods.attrs.define
class AttrsExample_Basic:
    a = True
    b = 3
    c = 0.4
    d = None
    e = "words"

basic = AttrsExample_Basic()
Easy.Ic( basic )


@Easy.Mods.attrs.define
class AttrsExample_FactoryAndDefaults:
    ## normally just use a var "field" rather than being this verbose, lol
    ## three methods shown, only use first for immutables
    a = Easy.Mods.attrs.field( default=False )
    b = Easy.Mods.attrs.field( factory=list )
    c = Easy.Mods.attrs.field()
    @c.default
    def c_default(self):
        return Easy.Mods.random.randint(1,8)

attrsFactory = AttrsExample_FactoryAndDefaults()
Easy.Ic( attrsFactory )





@Easy.Mods.attrs.define
class AttrsExample_TypeAnnotations:
    ## Remember, annotate all or None.
    ## If you do want some, use super generic object for flexible ones
    a: bool = True
    b: int = 3
    c: float = 0.4
    d: None = None
    e: str = "words"
    f: object = []


annotatedTypes = AttrsExample_TypeAnnotations()
Easy.Ic( annotatedTypes )



@Easy.Mods.attrs.define
class AttrsExample_Point3d:
    x: float
    y: float
    z: float

point3d = AttrsExample_Point3d( -0.5, 0.0, 1.5 )
Easy.Ic( point3d )



@Easy.Mods.attrs.define(slots=False)
class AttrsExample_FlexibleLater:
    a: 0
    b: 0
    c: 0

flexibleLater = AttrsExample_FlexibleLater( 1, 2, 3 )
    
Easy.Ic( flexibleLater )
Easy.Ic( Easy.Attrs.asdict(flexibleLater) )



@Easy.Attrs.define
class AttrsWithCustomInit:
    x: object

    def __init__(self, x: int = 42):
        self.__attrs_init__(x)
                              # 
attrsWithCustomInit = AttrsWithCustomInit()
Easy.Ic(AttrsWithCustomInit)



class UvRangeAbstract():
    this_is_an_example_base_class_classmember = True
    def __init__(self):
        print( "--Super Init and then... --", end="  " )
@Easy.Attrs.define
class UvRange(UvRangeAbstract):
    u0: float = 0.0
    v0: float = 0.0
    u1:float = None   #Easy.Attrs.NOTHING  gives errors  :( 
    v1:float = None
    
    def __attrs_pre_init__(self):
        super().__init__()
        
    def __attrs_post_init__(self):
        if self.u1 is None:
            self.u1 = self.u0 + 1.0
        if self.v1 is None:
            self.v1 = self.v0 + 1.0

uvRange = UvRange( 1.4, 3.5 )
Easy.Ic( uvRange )
uvRange2 = UvRange( 1.4, 3.5, 2.0, 3.9 )
Easy.Ic( uvRange2 )






## From attrs docs:
#
# You can choose freely between the approaches,
# but please remember that if you choose to use type annotations,
# you must annotate all attributes!
#
# attrs.NOTHING  ## Sentinel class to indicate the lack of a value when None is ambiguous.
# attrs.make_class(name, attrs, bases=(<class 'object'>, ), **attributes_arguments)
# attrs.define(same_as_define)
# attrs.frozen(same_as_define)  ##Behaves the same as attrs.define but sets frozen=True and on_setattr=None.

# attrs.define(maybe_cls=None, *, these=None, repr=None, hash=None, init=None, slots=True,
#   frozen=False, weakref_slot=True, str=False, auto_attribs=None, kw_only=False,
#   cache_hash=False, auto_exc=True, eq=None, order=False, auto_detect=True,
#   getstate_setstate=None, on_setattr=None, field_transformer=None, match_args=True)
#
# attrs.field(*, default=NOTHING, validator=None, repr=True, hash=None, init=True,
#    metadata=None, converter=None, factory=None, kw_only=False, eq=None,
#    order=None, on_setattr=None)


#@define
#class SomeClass:
#    a_number = field(default=42)#
#    list_of_numbers = field(factory=list)
