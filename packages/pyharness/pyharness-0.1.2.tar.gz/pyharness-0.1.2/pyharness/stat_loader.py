""" stat_loader: a utility for loading log dumps and writing them to postgres.
"""
import glob
import json
import os
from sqlalchemy import Table, Column, MetaData, types, create_engine, Sequence
from sqlalchemy.engine import reflection
from sqlalchemy.schema import DropSchema, CreateSchema
import sys

def to_postgres(dump_directory, db_name, schema_name, overwrite=True):
    db = create_engine("postgresql://localhost/" + db_name)
    inspector = reflection.Inspector.from_engine(db)

    # Drop and recreate the schema
    schema_exists = schema_name in inspector.get_schema_names()
    if overwrite and schema_exists:
        print "Schema exists and overwrite requested. Dropping schema..."
        sys.stdout.flush()
        db.execute(DropSchema(schema_name, cascade=True))
        schema_exists = False

    if not schema_exists:
        print "No existing schema. Recreating schema..."
        sys.stdout.flush()
        db.execute(CreateSchema(schema_name))
    else:
        print "Schema exists, not creating..."
        sys.stdout.flush()

    # Load the schema if necessary
    for filename in glob.glob(os.path.join(dump_directory, '*.json')):
        table_name = os.path.splitext(os.path.basename(filename))[0]

        table_names = inspector.get_table_names(schema=schema_name)
        print "Tables: %s" % table_names
        table_exists = table_name in table_names
        if overwrite and table_exists:
            print "Table exists and overwrite requested. Dropping table %s..." % table_name
            sys.stdout.flush()
            table.drop(db, checkfirst=True)
            table_exists = False

        if not table_exists:
            print "No existing table. Creating table %s..." % table_name
            sys.stdout.flush()

            print "Loading schema for table %s...  " % table_name,
            sys.stdout.flush()
            schema = {}
            with open(filename, 'rb') as f:
                for (i, raw_line) in enumerate(f):
                    if i % 10000 == 0:
                        print ".",
                        sys.stdout.flush()
                    try:
                        row = parse_line(raw_line)
                    except Exception as e:
                        print e
                        import pdb;pdb.set_trace()
                        continue # Error with data, just drop it.

                    # extract all columns and their types
                    safe_update(schema, extract_schema(row))

            print "Done!"
            sys.stdout.flush()

            # create the table
            metadata = MetaData()
            table = Table(table_name, metadata,
                          Column('id', types.Integer,
                                 Sequence(table_name + '_id_seq',
                                          schema=schema_name),
                                 primary_key=True),
                          *sorted(schema.values(), key=lambda c: c.name),
                          schema=schema_name)
            table.create(db)
            schema_keys = schema.keys()
        else:
            print "Table exists. Inspecting from the database..."
            sys.stdout.flush()
            metadata = MetaData()
            table = Table(table_name, metadata, 
                          Column('id', types.Integer,
                                 Sequence(table_name + '_id_seq',
                                          schema=schema_name),
                                 primary_key=True),
                          autoload=True, autoload_with=db, schema=schema_name)
            schema_keys = [c['name'] for c in inspector.get_columns(table_name, schema=schema_name) 
                           if c['name'] != 'id']

        # insert the data
        print "Inserting the data into table %s..." % table_name,
        sys.stdout.flush()
        with open(filename, 'rb') as f:
            cur_batch = []
            for i, raw_line in enumerate(f):
                row = extract_data(parse_line(raw_line), schema_keys)
                cur_batch.append(row)
                if (i + 1) % 10000 == 0:
                    print ".",
                    sys.stdout.flush()
                    db.execute(table.insert(), *cur_batch)
                    cur_batch = []
            db.execute(table.insert(), *cur_batch)
        print "Done!"
        sys.stdout.flush()

def parse_line(raw_line):
    return json.loads(raw_line.strip('[],\n'))

def extract_data(row, schema_keys, key_prefix=''):
    def p(key): return key_prefix + key
    data = {}
    for k, v in row.iteritems():

        # recurse if v is a dictionary
        if isinstance(v, dict):
            data.update(extract_data(v, {}, key_prefix=p(k) + '.'))

        # record the key's value
        else:
            data[p(k)] = v

    # add nulls for missing keys
    for missing_key in set(schema_keys) - set(data.keys()):
        assert missing_key not in data
        data[missing_key] = None
    return data

def extract_schema(row, key_prefix=''):
    def p(key): return key_prefix + key

    schema = {}
    for k, v in row.iteritems():
        # recurse if v is a dictionary
        if isinstance(v, dict):
            schema.update(extract_schema(v, key_prefix=p(k) + '.'))

        # detect standard types
        elif isinstance(v, bool):
            schema[p(k)] = Column(p(k), types.Boolean)

        elif isinstance(v, int):
            schema[p(k)] = Column(p(k), types.Integer)

        elif isinstance(v, float):
            schema[p(k)] = Column(p(k), types.Float)

        elif isinstance(v, str) or isinstance(v, unicode):
            schema[p(k)] = Column(p(k), types.String)

        elif v is None:
            schema[p(k)] = None

        else:
            raise TypeError("Unrecognized type for DB: " + str(v))

    return schema

def safe_update(d1, d2):
    for k, v in d2.iteritems():
        if (k in d1
            and v is not None
            and d1[k] is not None
            and str(v.type) != str(d1[k].type)):
            # try resolving numeric types
            numeric_types = ['INTEGER', 'FLOAT']
            if str(v.type) in numeric_types and str(d1[k].type) in numeric_types:
                d1[k] = Column(k, types.Float)
            else:
                raise ValueError("Inconsistent schema: %s in multiple rows, but"
                                 " values of type %s and %s exist!" %
                                 (k, str(v.type), str(d1[k].type)))
        elif v is not None:
            d1[k] = v
