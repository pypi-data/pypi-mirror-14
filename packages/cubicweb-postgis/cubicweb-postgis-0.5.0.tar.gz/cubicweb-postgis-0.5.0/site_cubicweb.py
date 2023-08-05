from logilab.database import FunctionDescr, AggrFunctionDescr
from logilab.database import get_db_helper
from logilab.database.sqlgen import SQLExpression

from yams import register_base_type

from rql.utils import register_function

from cubes.postgis import _GEOM_PARAMETERS, _GEOG_PARAMETERS

# register new base type
register_base_type('Geometry', _GEOM_PARAMETERS)
register_base_type('Geography', _GEOG_PARAMETERS)


def pg_geometry_sqltype(rdef):
    """Return a PostgreSQL column type corresponding to rdef's geom_type, srid
    and coord_dimension.
    """
    target_geom_type = rdef.geom_type
    if rdef.coord_dimension is not None and rdef.coord_dimension >= 3:  # XXX: handle 2D+M
        target_geom_type += 'Z'
    if rdef.coord_dimension == 4:
        target_geom_type += 'M'
    assert target_geom_type
    assert rdef.srid
    return 'geometry(%s, %s)' % (target_geom_type, rdef.srid)

def pg_geography_sqltype(rdef):
    """Return a PostgreSQL column type corresponding to rdef's geom_type and srid
    """
    srid = rdef.srid or 4326
    return 'geography(%s, %s)' % (rdef.geom_type, srid)

# Add the datatype to the helper mapping
pghelper = get_db_helper('postgres')
pghelper.TYPE_MAPPING['Geometry'] = pg_geometry_sqltype
pghelper.TYPE_MAPPING['Geography'] = pg_geography_sqltype

sqlitehelper = get_db_helper('sqlite')
sqlitehelper.TYPE_MAPPING['Geometry'] = 'text'
sqlitehelper.TYPE_MAPPING['Geography'] = 'text'

# Add a converter for Geometry
def convert_geom(x):
    if isinstance(x, SQLExpression):
        return x
    if isinstance(x, (tuple, list)):
        # We give the (Geometry, SRID)
        return SQLExpression('ST_GeomFromText(%(geo)s, %(srid)s)', geo=x[0], srid=x[1])
    # We just give the Geometry
    return SQLExpression('ST_GeomFromText(%(geo)s, %(srid)s)', geo=x, srid=-1)

def convert_geog(x):
    # takes only a Geometry type, assumes GPS srid
    return SQLExpression('ST_GeogFromText(%(geo)s)', geo=x)

# Add the converter function to the known SQL_CONVERTERS
pghelper.TYPE_CONVERTERS['Geometry'] = convert_geom
pghelper.TYPE_CONVERTERS['Geography'] = convert_geog

# actually don't care of sqlite, it's just to make it possible to test
sqlitehelper.TYPE_CONVERTERS['Geometry'] = str
sqlitehelper.TYPE_CONVERTERS['Geography'] = str



class ST_EQUALS(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Bool'


class ST_INTERSECTS(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Bool'

class ST_INTERSECTION(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Geometry'


class ST_OVERLAPS(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Bool'

class ST_CROSSES(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Bool'

class ST_TOUCHES(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Bool'


class ST_GEOMETRYN(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Geometry'


class ST_WITHIN(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Bool'


class ST_CONTAINS(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Bool'


class ST_DWITHIN(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Float'


class ST_LENGTH(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Float'


class ST_DISTANCE(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Float'


class ST_DISTANCE_SPHERE(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Float'


class ST_AREA(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Float'


class ST_NUMINTERIORRINGS(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Int'


class ST_SIMPLIFY(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Geometry'


class ST_TRANSFORM(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Geometry'


class ST_ASGEOJSON(FunctionDescr):
    minargs = 1
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'String'


class ST_ASTEXT(FunctionDescr):
    minargs = 1
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'String'


class ST_GEOMFROMTEXT(FunctionDescr):
    minargs = 1
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Geometry'

class ST_GEOGFROMTEXT(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Geography'

class ST_COVERS(FunctionDescr):
    minargs = 1
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Bool'

class GEOMETRY(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Geometry'

class ST_UNION(FunctionDescr):
    aggregat = True
    minargs = 1
    supported_backends = ('postgres',)
    rtype = 'Geometry'

class ST_COLLECT(FunctionDescr):
    aggregat = True
    minargs = 1
    supported_backends = ('postgres',)
    rtype = 'Geometry'

class ST_CONVEXHULL(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Geometry'

class ST_CONCAVEHULL(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Geometry'


class DISPLAY(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'String'

    def as_sql_postgres(self, args):
        return 'ST_ASGeoJSON(ST_Transform(%s, %s))' % (args[0], args[1])


class ST_MAKEPOINT(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Geometry'


class ST_SRID(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Geometry'


class ST_SETSRID(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Geometry'


class ST_X(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Float'


class ST_Y(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Float'


class ST_Z(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Float'


class ST_M(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Float'


class ST_EXTENT(AggrFunctionDescr):
    supported_backends = ('postgres',)
    rtype = 'Geometry'


register_function(ST_EQUALS)
register_function(ST_INTERSECTS)
register_function(ST_INTERSECTION)
register_function(ST_OVERLAPS)
register_function(ST_CROSSES)
register_function(ST_TOUCHES)
register_function(ST_GEOMETRYN)
register_function(ST_WITHIN)
register_function(ST_CONTAINS)
register_function(ST_DWITHIN)
register_function(ST_LENGTH)
register_function(ST_DISTANCE)
register_function(ST_AREA)
register_function(ST_NUMINTERIORRINGS)
register_function(ST_SIMPLIFY)
register_function(ST_TRANSFORM)
register_function(DISPLAY)
register_function(ST_ASGEOJSON)
register_function(ST_ASTEXT)
register_function(ST_GEOMFROMTEXT)
register_function(ST_GEOGFROMTEXT)
register_function(ST_COVERS)
register_function(GEOMETRY)
register_function(ST_UNION)
register_function(ST_COLLECT)
register_function(ST_CONVEXHULL)
register_function(ST_CONCAVEHULL)
register_function(ST_MAKEPOINT)
register_function(ST_SETSRID)
register_function(ST_SRID)
register_function(ST_DISTANCE_SPHERE)
register_function(ST_X)
register_function(ST_Y)
register_function(ST_Z)
register_function(ST_M)
register_function(ST_EXTENT)
