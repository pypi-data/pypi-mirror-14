# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Acl(models.Model):
    principaltype = models.CharField(max_length=25)
    principalid = models.IntegerField()
    rightname = models.CharField(max_length=25)
    objecttype = models.CharField(max_length=25)
    objectid = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acl'


class Articles(models.Model):
    name = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    sortorder = models.IntegerField()
    class_field = models.IntegerField(db_column='class')  # Field renamed because it was a Python reserved word.
    parent = models.IntegerField()
    uri = models.CharField(max_length=255, blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'articles'


class Attachments(models.Model):
    transactionid = models.IntegerField()
    parent = models.IntegerField()
    messageid = models.CharField(max_length=160, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    contenttype = models.CharField(max_length=80, blank=True, null=True)
    contentencoding = models.CharField(max_length=80, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    headers = models.TextField(blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    contentindex = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'attachments'


class Attributes(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    contenttype = models.CharField(max_length=16, blank=True, null=True)
    objecttype = models.CharField(max_length=64, blank=True, null=True)
    objectid = models.IntegerField(blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attributes'


class Cachedgroupmembers(models.Model):
    groupid = models.IntegerField(blank=True, null=True)
    memberid = models.IntegerField(blank=True, null=True)
    via = models.IntegerField(blank=True, null=True)
    immediateparentid = models.IntegerField(blank=True, null=True)
    disabled = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'cachedgroupmembers'


class Classes(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    sortorder = models.IntegerField()
    disabled = models.SmallIntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)
    hotlist = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'classes'


class Customfields(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    sortorder = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)
    disabled = models.SmallIntegerField()
    lookuptype = models.CharField(max_length=255)
    pattern = models.CharField(max_length=65536, blank=True, null=True)
    maxvalues = models.IntegerField(blank=True, null=True)
    basedon = models.IntegerField(blank=True, null=True)
    rendertype = models.CharField(max_length=64, blank=True, null=True)
    valuesclass = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customfields'


class Customfieldvalues(models.Model):
    customfield = models.IntegerField()
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    sortorder = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customfieldvalues'


class FmArticlecfvalues(models.Model):
    article = models.IntegerField()
    customfield = models.IntegerField()
    content = models.TextField(blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fm_articlecfvalues'


class FmArticles(models.Model):
    name = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    sortorder = models.IntegerField()
    class_field = models.IntegerField(db_column='class')  # Field renamed because it was a Python reserved word.
    parent = models.IntegerField()
    uri = models.CharField(max_length=255, blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fm_articles'


class FmClasscustomfields(models.Model):
    class_field = models.IntegerField(db_column='class')  # Field renamed because it was a Python reserved word.
    customfield = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    sortorder = models.SmallIntegerField()
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fm_classcustomfields'


class FmClasses(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    sortorder = models.IntegerField()
    disabled = models.SmallIntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)
    hotlist = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'fm_classes'


class FmCustomfields(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    sortorder = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fm_customfields'


class FmCustomfieldvalues(models.Model):
    customfield = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    sortorder = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fm_customfieldvalues'


class FmObjecttopics(models.Model):
    topic = models.IntegerField()
    objecttype = models.CharField(max_length=64)
    objectid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fm_objecttopics'


class FmTopics(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    objecttype = models.CharField(max_length=64)
    objectid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fm_topics'


class FmTransactions(models.Model):
    article = models.IntegerField()
    changelog = models.TextField()
    type = models.CharField(max_length=64)
    field = models.CharField(max_length=64)
    oldcontent = models.TextField()
    newcontent = models.TextField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fm_transactions'


class Groupmembers(models.Model):
    groupid = models.IntegerField()
    memberid = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groupmembers'
        unique_together = (('groupid', 'memberid'),)


class Groups(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    domain = models.CharField(max_length=64, blank=True, null=True)
    type = models.CharField(max_length=64, blank=True, null=True)
    instance = models.IntegerField(blank=True, null=True)
    instance_int = models.IntegerField(blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class Links(models.Model):
    base = models.CharField(max_length=240, blank=True, null=True)
    target = models.CharField(max_length=240, blank=True, null=True)
    type = models.CharField(max_length=20)
    localtarget = models.IntegerField()
    localbase = models.IntegerField()
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'links'
        unique_together = (('base', 'target', 'type'),)


class Objectclasses(models.Model):
    class_field = models.IntegerField(db_column='class')  # Field renamed because it was a Python reserved word.
    objecttype = models.CharField(max_length=255)
    objectid = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objectclasses'


class Objectcustomfields(models.Model):
    customfield = models.IntegerField()
    objectid = models.IntegerField()
    sortorder = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objectcustomfields'


class Objectcustomfieldvalues(models.Model):
    objectid = models.IntegerField()
    customfield = models.IntegerField()
    content = models.CharField(max_length=255, blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)
    objecttype = models.CharField(max_length=255)
    largecontent = models.TextField(blank=True, null=True)
    contenttype = models.CharField(max_length=80, blank=True, null=True)
    contentencoding = models.CharField(max_length=80, blank=True, null=True)
    sortorder = models.IntegerField()
    disabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'objectcustomfieldvalues'


class Objectscrips(models.Model):
    scrip = models.IntegerField()
    stage = models.CharField(max_length=32)
    objectid = models.IntegerField()
    sortorder = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objectscrips'
        unique_together = (('objectid', 'scrip'),)


class Objecttopics(models.Model):
    topic = models.IntegerField()
    objecttype = models.CharField(max_length=64)
    objectid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'objecttopics'


class PgaForms(models.Model):
    formname = models.CharField(max_length=64, blank=True, null=True)
    formsource = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pga_forms'


class PgaLayout(models.Model):
    tablename = models.CharField(max_length=64, blank=True, null=True)
    nrcols = models.SmallIntegerField(blank=True, null=True)
    colnames = models.TextField(blank=True, null=True)
    colwidth = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pga_layout'


class PgaQueries(models.Model):
    queryname = models.CharField(max_length=64, blank=True, null=True)
    querytype = models.CharField(max_length=1, blank=True, null=True)
    querycommand = models.TextField(blank=True, null=True)
    querytables = models.TextField(blank=True, null=True)
    querylinks = models.TextField(blank=True, null=True)
    queryresults = models.TextField(blank=True, null=True)
    querycomments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pga_queries'


class PgaReports(models.Model):
    reportname = models.CharField(max_length=64, blank=True, null=True)
    reportsource = models.TextField(blank=True, null=True)
    reportbody = models.TextField(blank=True, null=True)
    reportprocs = models.TextField(blank=True, null=True)
    reportoptions = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pga_reports'


class PgaSchema(models.Model):
    schemaname = models.CharField(max_length=64, blank=True, null=True)
    schematables = models.TextField(blank=True, null=True)
    schemalinks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pga_schema'


class PgaScripts(models.Model):
    scriptname = models.CharField(max_length=64, blank=True, null=True)
    scriptsource = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pga_scripts'


class Principals(models.Model):
    principaltype = models.CharField(max_length=16)
    objectid = models.IntegerField(blank=True, null=True)
    disabled = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'principals'


class Queues(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    correspondaddress = models.CharField(max_length=120, blank=True, null=True)
    commentaddress = models.CharField(max_length=120, blank=True, null=True)
    initialpriority = models.IntegerField()
    finalpriority = models.IntegerField()
    defaultduein = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)
    disabled = models.SmallIntegerField()
    subjecttag = models.CharField(max_length=120, blank=True, null=True)
    lifecycle = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'queues'


class Scripactions(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    execmodule = models.CharField(max_length=60, blank=True, null=True)
    argument = models.CharField(max_length=255, blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scripactions'


class Scripconditions(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    execmodule = models.CharField(max_length=60, blank=True, null=True)
    argument = models.CharField(max_length=255, blank=True, null=True)
    applicabletranstypes = models.CharField(max_length=60, blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scripconditions'


class Scrips(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    scripcondition = models.IntegerField()
    scripaction = models.IntegerField()
    customisapplicablecode = models.TextField(blank=True, null=True)
    custompreparecode = models.TextField(blank=True, null=True)
    customcommitcode = models.TextField(blank=True, null=True)
    template = models.CharField(max_length=200)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)
    disabled = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'scrips'


class Sessions(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    a_session = models.BinaryField(blank=True, null=True)
    lastupdated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sessions'


class Templates(models.Model):
    queue = models.IntegerField()
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=16, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    lastupdated = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'templates'


class Tickets(models.Model):
    effectiveid = models.IntegerField()
    queue = models.IntegerField()
    type = models.CharField(max_length=16, blank=True, null=True)
    issuestatement = models.IntegerField()
    resolution = models.IntegerField()
    owner = models.IntegerField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    initialpriority = models.IntegerField()
    finalpriority = models.IntegerField()
    priority = models.IntegerField()
    timeestimated = models.IntegerField()
    timeworked = models.IntegerField()
    status = models.CharField(max_length=64, blank=True, null=True)
    timeleft = models.IntegerField()
    told = models.DateTimeField(blank=True, null=True)
    starts = models.DateTimeField(blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True)
    due = models.DateTimeField(blank=True, null=True)
    resolved = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    disabled = models.SmallIntegerField()
    ismerged = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'


class Topics(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    objecttype = models.CharField(max_length=64)
    objectid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'topics'


class Transactions(models.Model):
    objectid = models.IntegerField()
    timetaken = models.IntegerField()
    type = models.CharField(max_length=20, blank=True, null=True)
    field = models.CharField(max_length=40, blank=True, null=True)
    oldvalue = models.CharField(max_length=255, blank=True, null=True)
    newvalue = models.CharField(max_length=255, blank=True, null=True)
    data = models.CharField(max_length=255, blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    objecttype = models.CharField(max_length=64)
    referencetype = models.CharField(max_length=255, blank=True, null=True)
    oldreference = models.IntegerField(blank=True, null=True)
    newreference = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transactions'


class Users(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=256, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    emailaddress = models.CharField(max_length=120, blank=True, null=True)
    freeformcontactinfo = models.TextField(blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    realname = models.CharField(max_length=120, blank=True, null=True)
    nickname = models.CharField(max_length=16, blank=True, null=True)
    lang = models.CharField(max_length=16, blank=True, null=True)
    emailencoding = models.CharField(max_length=16, blank=True, null=True)
    webencoding = models.CharField(max_length=16, blank=True, null=True)
    externalcontactinfoid = models.CharField(max_length=100, blank=True, null=True)
    contactinfosystem = models.CharField(max_length=30, blank=True, null=True)
    externalauthid = models.CharField(max_length=100, blank=True, null=True)
    authsystem = models.CharField(max_length=30, blank=True, null=True)
    gecos = models.CharField(max_length=16, blank=True, null=True)
    homephone = models.CharField(max_length=30, blank=True, null=True)
    workphone = models.CharField(max_length=30, blank=True, null=True)
    mobilephone = models.CharField(max_length=30, blank=True, null=True)
    pagerphone = models.CharField(max_length=30, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=16, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    pgpkey = models.TextField(blank=True, null=True)
    creator = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    lastupdatedby = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)
    authtoken = models.CharField(max_length=16, blank=True, null=True)
    smimecertificate = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
