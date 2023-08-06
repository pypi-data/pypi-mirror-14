
# coding: utf-8

# # Examples of the *mgkit.db* package

# ## Imports

# In[84]:

from mgkit.io import gff
import mgkit.net
from mgkit.db import dbm
from mgkit.db import mongo
import mgkit.taxon
import gzip


# ## Download Example GFF

# In[66]:

# This will just load the data from the repository and save it in the same directory as
# this notebook
data = mgkit.net.url_read('https://bitbucket.org/setsuna80/mgkit/downloads/assembly.gff.gz')
# The data is compressed
open('assembly.gff.gz', 'w').write(data)


# ## GFF Annotations
# The are a few ways to load the GFF, but the result of *parse_gff* is a generator that yields one annotation at a time when it's iterate over. One way to keep the annotations in memory is building a dictionary, with the unique identifier for each annotation (called **uid**) used as key, while the annotation object is the value.

# In[4]:

# *mgkit.io.gff.parse_gff* can read compressed data, gzip, bz2 (also lzma on python3)
annotations = {
    annotation.uid: annotation
    for annotation in gff.parse_gff('assembly.gff.gz')
}


# Each annotation is parsed and an instance of the **mgkit.io.gff.Annotation** is created. The class contains several properties, like the unique identifier (uid), the gene identifier (gene_id) and the taxon identifier (taxon_id)

# In[30]:

annotation = annotations['d002b31c-1d78-438c-b8f9-aba791807724']
print annotation

print annotation.uid, annotation.gene_id, annotation.taxon_id


# Other properties and methods can be accessed, like the *Annotation.get_mappings* to get a dictionary of all mappings, or using the *len* function on the instance to get it's length (or using the property *length*).

# In[11]:

print len(annotation), annotation.length
print annotation.get_mappings()


# ### Taxonomy and Annotations
# When using metagenomics, one of the problem is associated functionality to taxonomy. MGKit contains a class that can read the taxonomy from [Uniprot](www.uniprot.org), which is compatible with NCBI taxonomy. The **mgkit.taxon** contains the **UniprotTaxonomy** that is use to store and in part search the taxonomy. The module contains many more functions to resolve different levels of the taxonomy. A few examples applied to the annotations loaded follow.

# In[90]:

# This will just load the data from the repository and save it in the same directory as
# this notebook
data = mgkit.net.url_read(
    "https://bitbucket.org/setsuna80/mgkit/downloads/taxonomy.pickle.gz"
)
open('taxonomy.pickle.gz', 'w').write(data)
del data


# In[91]:

# Using compress taxonomy files makes it slower to load
taxonomy = mgkit.taxon.UniprotTaxonomy('taxonomy.pickle.gz')


# In[103]:

# to find the Bacteoidales taxon identifier
taxonomy.find_by_name('bacteroidales')


# In[121]:

# to find all the annotations that belong to the Order Bacteroidales
count = 0
for annotation in annotations.itervalues():
    if mgkit.taxon.is_ancestor(taxonomy, annotation.taxon_id, 171549):
        count += 1
        print annotation.uid, annotation.gene_id
print "Number of annotation:", count


# In[109]:

# to find out the Phyla represented in the annotations
print set(
    taxonomy.get_ranked_taxon(annotation.taxon_id, rank='phylum').s_name
    for annotation in annotations.itervalues()
)   


# In[116]:

# to get the lineage of the first annotations
annotation = annotations['b97ead95-81a7-4caf-8d25-349ee6e276c1']
print taxonomy[annotation.taxon_id].s_name, mgkit.taxon.get_lineage(taxonomy, annotation.taxon_id)


# In[115]:

# to get the names, quickly
annotation = annotations['b97ead95-81a7-4caf-8d25-349ee6e276c1']
print taxonomy[annotation.taxon_id].s_name, mgkit.taxon.get_lineage(taxonomy, annotation.taxon_id, names=True)


# ### Issues
# Keeping the annotations in memory can lead to a high memory usage, as well as a long time traversing all of them to specifically filter them. MGKit uses two solutions to interface with DBs, one is using a *dbm-like* database, *semidbm* and the other is using *MongoDB*.

# ## semidbm
# Packages to use *dbm* database are included with Python, but they depend on the type of OS python is installed onto. A pure Python implementation of a dbm is [semidbm](https://github.com/jamesls/semidbm). As other *dbm*, it works in a similar way as a dictionary, while keeping the memory usage low. To create a *semidbm* DB from annotations, the **get-gff-info** can be used, using the **dbm** command:

# In[21]:

get_ipython().system(u'get-gff-info dbm -d assembly-db assembly.gff.gz ')


# or interactively, using *mgkit.db.dbm.create_gff_dbm*:

# In[27]:

db = dbm.create_gff_dbm(annotations.itervalues(), 'assembly-db')


# Which also return an instance of db. *semidbm* allows the use of only strings as keys and strings as values, so for the same annotation as before, you see what MGKit stores in it, the actual GFF line:

# In[28]:

db['d002b31c-1d78-438c-b8f9-aba791807724']


# The GFF line must then be converted back into an **Annotation** instance. To automate the process, the **mgkit.db.dbm.GFFDB** class wraps the *semidbm*. The same example as the one above:

# In[56]:

db = dbm.GFFDB('assembly-db')
db['d002b31c-1d78-438c-b8f9-aba791807724']


# It can also be iterated over as a dictionary (for compatibility, both *iteritems* and *items* return an iterator)

# In[52]:

for uid in db.db:
    print uid, db[uid]
    break


# In[55]:

for uid, annotation in db.iteritems():
    print uid, annotation
    break


# Using this class, it is possible to use a DB as a drop-in replacement for a dictionary in a script that used annotations stored in memory in MGKit. The [examples using the taxonomy](#Taxonomy-and-Annotations) will works in the same way, for example.

# ## Using MongoDB
# [MongoDB](https://www.mongodb.org/) is Document based DB that is not based on SQL. One of the advantage of it the absence of a schema, which makes it easy to insert annotations into it. Moreover, the data in a MongoDB is easily accessible from a variety of programming languages, as well as its own shell. Another advantage is the possiblity to query the annotations and index specific values to speed up them.
# 
# In the same way as with *dbm*, the **get-gff-info** can help produce a file that can be directly loaded into a *mongod* instance.
# 
# The following example uses **pymongo** (the official client library for Python) and requires a **mongod** instance running on the same machine. The annotations will be imported into the **test** database, into the **gff** collection.

# In[69]:

get_ipython().system(u'gunzip -c assembly.gff.gz | get-gff-info mongodb | mongoimport --db test --collection gff --drop')


# You can use the **pymongo** module directly or just use the **mgkit.db.mongo.GFFDB** class to automate connection and conversion of the **JSON** documents back into **Annotation** objects.

# In[72]:

db = mongo.GFFDB('test', 'gff')


# In[74]:

for annotation in db.find_annotation():
    print annotation.uid, annotation.gene_id
    break


# The DB can be queried by passing the **GFF.find_annotation** method the same query that are explained in [Pymongo documentation](https://docs.mongodb.org/getting-started/python/client/).

# In[76]:

# To look for all annotations that have the KO mapping to K01883
for annotation in db.find_annotation({'map.ko': 'K01883'}):
    print annotation


# In[79]:

# To look for all annotations that have the KO mapping to K01883 *AND*
# the taxonomy was inferred from a blast to NCBI (see refinement of
# taxonomy in theTutorial - Gene Prediction)
for annotation in db.find_annotation({'map.ko': 'K01883', 'taxon_db': 'NCBI-NT'}):
    print annotation


# In[117]:

# Finding all annotation from a specific taxon
for annotation in db.find_annotation({'taxon_id': 224911}):
    print annotation


# ### Using Taxonomy
# The usual approach about the taxonomy is to traverse all the annotations (those returned by one of the previous queries, even) and use the functionality in the **mgkit.taxon** module. It is possible to repeat the example that search all annotations that belong to Order *Bacteroidales*, but the records must be loaded with the lineage into the DB. This can be done having a taxonomy file, *taxonomy.pickle.gz* in our case, with the following command:

# In[118]:

get_ipython().system(u'gunzip -c assembly.gff.gz | get-gff-info mongodb -t taxonomy.pickle.gz | mongoimport --db test --collection gff --drop')


# The script will first load the taxonomy and add to each record in the database the **lineage** key. This contains an array of integers, that are the output of the **mgkit.taxon.lineage** function and can be searched using:

# In[123]:

count = 0
for annotation in db.find_annotation({'lineage': 171549}):
    count += 1
    print annotation
print "Number of annotation:", count


# And as you can see, the number of annotations is the same as the [example above](#Taxonomy-and-Annotations). The use of MongoDB to store the annotations can make it simplier to use richer queries, even from other languages.
