# Vectraits db definitions.
# This should be directly compatible with the R csv -> psql converter found on the db repo.

# When deploying for the first time from an external dump (not taken from web2py),
# you MUST enable fake_migrate_all at the DAL definition in db.py

#########################################################################
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable',Field('myfield','string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
########################################################################

# +----------------------------+
# | Global db list definitions |
# +----------------------------+

# +-------------------+
# | Table definitions |
# +-------------------+

migrate = True

db2.define_table('citation',
                 Field('citationid', type='id'),
                 Field('citation', type='string', length=1500),
                 Field('doi', type='string', length=255),
                 Field('published', type='boolean'),
                 migrate=migrate)

db2.define_table('contributor',
                 Field('contributorid', type='id'),
                 Field('submittedby', type='string', length=255),
                 Field('contributoremail', type='string', length=255),
                 migrate=migrate)

db2.define_table('experimentalconditions',
                 Field('experimentid', type='id'),
                 Field('replicates', type='double'),
                 Field('habitat', type='string', length=20),
                 Field('labfield', type='string', length=11),
                 Field('arenavalue', type='double'),
                 Field('arenaunit', type='string', length=255),
                 Field('arenavaluesi', type='double'),
                 Field('arenaunitsi', type='string', length=255),
                 Field('resrepvalue', type='integer'),
                 Field('resrepunit', type='string', length=255),
                 Field('resrepvaluesi', type='double'),
                 Field('resrepunitsi', type='string', length=255),
                 migrate=migrate)

db2.define_table('maintable',
                 Field('uid', type='id'),
                 Field('originalid', type='string', length=20),
                 Field('originaltraitname', type='string', length=255),
                 Field('originaltraitdef', type='text'),
                 Field('standardisedtraitname', type='string', length=255),
                 Field('standardisedtraitdef', type='text'),
                 Field('originaltraitvalue', type='double'),
                 Field('originaltraitunit', type='string', length=255),
                 Field('originalerrorpos', type='double'),
                 Field('originalerrorneg', type='double'),
                 Field('originalerrorunit', type='string', length=255),
                 Field('standardisedtraitvalue', type='double'),
                 Field('standardisedtraitunit', type='string', length=255),
                 Field('standardisederrorpos', type='double'),
                 Field('standardisederrorneg', type='double'),
                 Field('standardisederrorunit', type='string', length=255),
                 Field('ambienttemp', type='double'),
                 Field('ambienttempmethod', type='string', length=255),
                 Field('ambienttempunit', type='string', length=255),
                 Field('ambientlight', type='string', length=255),
                 Field('ambientlightunit', type='string', length=255),
                 Field('secondstressor', type='string', length=255),
                 Field('secondstressordef', type='string', length=255),
                 Field('secondstressorvalue', type='double'),
                 Field('secondstressorunit', type='string', length=255),
                 Field('timestart', type='string', length=255),
                 Field('timeend', type='string', length=255),
                 Field('totalobstimevalue', type='double'),
                 Field('totalobstimeunit', type='string', length=255),
                 Field('totalobstimevaluesi', type='double'),
                 Field('totalobstimeunitsi', type='string', length=255),
                 Field('totalobstimenotes', type='string', length=255),
                 Field('interactor1', type='string', length=255),
                 Field('interactor1common', type='string', length=255),
                 Field('interactor1wholepart', type='string', length=255),
                 Field('interactor1wholeparttype', type='string', length=255),
                 Field('interactor1number', type='string', length=255),
                 Field('interactor1stage', type='string', length=255),
                 Field('interactor1temp', type='double'),
                 Field('interactor1tempunit', type='string', length=255),
                 Field('interactor1tempmethod', type='string', length=255),
                 Field('interactor1growthtemp', type='double'),
                 Field('interactor1growthtempunit', type='string', length=255),
                 Field('interactor1growthdur', type='double'),
                 Field('interactor1growthdurunit', type='string', length=255),
                 Field('interactor1growthtype', type='string', length=255),
                 Field('interactor1acc', type='string', length=255),
                 Field('interactor1acctemp', type='double'),
                 Field('interactor1acctempnotes', type='string', length=255),
                 Field('interactor1acctime', type='double'),
                 Field('interactor1acctimenotes', type='string', length=255),
                 Field('interactor1acctimeunit', type='string', length=255),
                 Field('interactor1origtemp', type='double'),
                 Field('interactor1origtempnotes', type='string', length=255),
                 Field('interactor1origtime', type='double'),
                 Field('interactor1origtimenotes', type='string', length=255),
                 Field('interactor1origtimeunit', type='string', length=255),
                 Field('interactor1equilibtimevalue', type='double'),
                 Field('interactor1equilibtimeunit', type='string', length=255),
                 Field('interactor1size', type='double'),
                 Field('interactor1sizeunit', type='string', length=255),
                 Field('interactor1sizetype', type='string', length=255),
                 Field('interactor1sizesi', type='double'),
                 Field('interactor1sizeunitsi', type='string', length=255),
                 Field('interactor1denvalue', type='double'),
                 Field('interactor1denunit', type='string', length=255),
                 Field('interactor1dentypesi', type='string', length=255),
                 Field('interactor1denvaluesi', type='double'),
                 Field('interactor1denunitsi', type='string', length=255),
                 Field('interactor1massvaluesi', type='double'),
                 Field('interactor1massunitsi', type='string', length=255),
                 Field('interactor2', type='string', length=255),
                 Field('interactor2common', type='string', length=255),
                 Field('interactor2stage', type='string', length=255),
                 Field('interactor2temp', type='double'),
                 Field('interactor2tempunit', type='string', length=255),
                 Field('interactor2tempmethod', type='string', length=255),
                 Field('interactor2growthtemp', type='double'),
                 Field('interactor2growthtempunit', type='string', length=255),
                 Field('interactor2growthdur', type='double'),
                 Field('interactor2growthdurunit', type='string', length=255),
                 Field('interactor2growthtype', type='string', length=255),
                 Field('interactor2acc', type='string', length=255),
                 Field('interactor2acctemp', type='double'),
                 Field('interactor2acctempnotes', type='string', length=255),
                 Field('interactor2acctime', type='double'),
                 Field('interactor2acctimenotes', type='string', length=255),
                 Field('interactor2acctimeunit', type='string', length=255),
                 Field('interactor2origtemp', type='double'),
                 Field('interactor2origtempnotes', type='string', length=255),
                 Field('interactor2origtime', type='double'),
                 Field('interactor2origtimenotes', type='string', length=255),
                 Field('interactor2origtimeunit', type='string', length=255),
                 Field('interactor2equilibtimevalue', type='double'),
                 Field('interactor2equilibtimeunit', type='string', length=255),
                 Field('interactor2size', type='double'),
                 Field('interactor2sizeunit', type='string', length=255),
                 Field('interactor2sizetype', type='string', length=255),
                 Field('interactor2sizesi', type='double'),
                 Field('interactor2sizeunitsi', type='string', length=255),
                 Field('interactor2denvalue', type='double'),
                 Field('interactor2denunit', type='string', length=255),
                 Field('interactor2dentypesi', type='string', length=255),
                 Field('interactor2denvaluesi', type='double'),
                 Field('interactor2denunitsi', type='string', length=255),
                 Field('interactor2massvaluesi', type='double'),
                 Field('interactor2massunitsi', type='string', length=255),
                 Field('locationid', type='reference studylocation'),
                 Field('interactor1id', type='reference taxonomy'),
                 Field('interactor2id', type='reference taxonomy'),
                 Field('traitdescriptionid', type='reference traitdescription'),
                 Field('sourceinfoid', type='reference sourceinfo'),
                 Field('expcondid', type='reference experimentalconditions'),
                 Field('notes', type='string', length=2055),
                 migrate=migrate)

db2.define_table('sourceinfo',
                 Field('sourceid', type='id'),
                 Field('originalid', type='string', length=255),
                 Field('contributorid', type='reference contributor'),
                 Field('citationid', type='reference citation'),
                 Field('figuretable', type='string', length=255),
                 migrate=migrate)

db2.define_table('studylocation',
                 Field('locationid', type='id'),
                 Field('locationtext', type='text'),
                 Field('locationtype', type='string', length=255),
                 Field('locationdate', type='string', length=255),
                 Field('coordinatetype', type='string', length=255),
                 Field('latitude', type='double'),
                 Field('longitude', type='double'),
                 migrate=migrate)

db2.define_table('taxonomy',
                 Field('taxid', type='id'),
                 Field('taxkingdom', type='string', length=50),
                 Field('taxphylum', type='string', length=50),
                 Field('taxclass', type='string', length=50),
                 Field('taxorder', type='string', length=50),
                 Field('taxfamily', type='string', length=50),
                 Field('taxgenus', type='string', length=50),
                 Field('taxspecies', type='string', length=255),
                 migrate=migrate)

db2.define_table('traitdescription',
                 Field('traitdesid', type='id'),
                 Field('physicalprocess', type='string', length=255),
                 Field('physicalprocess_1', type='string', length=255),
                 Field('physicalprocess_2', type='string', length=255),
                 migrate=migrate)
