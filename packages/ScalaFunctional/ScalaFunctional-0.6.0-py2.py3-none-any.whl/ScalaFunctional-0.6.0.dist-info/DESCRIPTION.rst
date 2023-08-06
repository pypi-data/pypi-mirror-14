PyFunctional
============

|TravisCI| |Coverage by codecov.io| |ReadTheDocs| |Latest Version|
|Gitter|

**Note: ``ScalaFunctional`` is now ``PyFunctional``, see
`RFC <https://github.com/EntilZha/ScalaFunctional/issues/62>`__ for
details**

Introduction
------------

``PyFunctional`` is a Python package that makes working with data easy.
It takes inspiration from several sources that include Scala
collections, Apache Spark RDDs, Microsoft LINQ and more generally
functional programming. It also offers native reading and writing of
data formats such as text, csv, and json files. Support for SQLite3,
other databases, and compressed files is planned for the next release.

The combination of these ideas makes ``PyFunctional`` a great choice for
declarative transformation, creating pipelines, and data analysis.

`Original blog post for
ScalaFunctional <http://entilzha.github.io/blog/2015/03/14/functional-programming-collections-python/>`__

Installation
------------

``PyFunctional`` is available on
`pypi <https://pypi.python.org/pypi/ScalaFunctional>`__ and can be
installed by running:

.. code:: bash

    # Install from command line
    $ pip install pyfunctional

Then in python run: ``from functional import seq``

Examples
--------

``PyFunctional`` is useful for many tasks, and can natively open several
common file types. Here are a few examples of what you can do.

Simple Example
~~~~~~~~~~~~~~

.. code:: python

    from functional import seq

    seq(1, 2, 3, 4)\
        .map(lambda x: x * 2)\
        .filter(lambda x: x > 4)\
        .reduce(lambda x, y: x + y)
    # 14

Streams, Transformations and Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``PyFunctional`` has three types of functions:

1. Streams: read data for use by the collections API.
2. Transformations: transform data from streams with functions such as
   ``map``, ``flat_map``, and ``filter``
3. Actions: These cause a series of transformations to evaluate to a
   concrete value. ``to_list``, ``reduce``, and ``to_dict`` are examples
   of actions.

In the expression
``seq(1, 2, 3).map(lambda x: x * 2).reduce(lambda x, y: x + y)``,
``seq`` is the stream, ``map`` is the transformation, and ``reduce`` is
the action.

Filtering a list of account transactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from functional import seq
    from collections import namedtuple

    Transaction = namedtuple('Transaction', 'reason amount')
    transactions = [
        Transaction('github', 7),
        Transaction('food', 10),
        Transaction('coffee', 5),
        Transaction('digitalocean', 5),
        Transaction('food', 5),
        Transaction('riotgames', 25),
        Transaction('food', 10),
        Transaction('amazon', 200),
        Transaction('paycheck', -1000)
    ]

    # Using the Scala/Spark inspired APIs
    food_cost = seq(transactions)\
        .filter(lambda x: x.reason == 'food')\
        .map(lambda x: x.amount).sum()

    # Using the LINQ inspired APIs
    food_cost = seq(transactions)\
        .where(lambda x: x.reason == 'food')\
        .select(lambda x: x.amount).sum()

    # Using ScalaFunctional with fn
    from fn import _
    food_cost = seq(transactions).filter(_.reason == 'food').map(_.amount).sum()

Word Count and Joins
~~~~~~~~~~~~~~~~~~~~

The account transactions example could be done easily in pure python
using list comprehensions. To show some of the things ``PyFunctional``
excels at, take a look at a couple of word count examples.

.. code:: python

    words = 'I dont want to believe I want to know'.split(' ')
    seq(words).map(lambda word: (word, 1)).reduce_by_key(lambda x, y: x + y)
    # [('dont', 1), ('I', 2), ('to', 2), ('know', 1), ('want', 2), ('believe', 1)]

In the next example we have chat logs formatted in `json lines
(jsonl) <http://jsonlines.org/>`__ which contain messages and metadata.
A typical jsonl file will have one valid json on each line of a file.
Below are a few lines out of ``examples/chat_logs.jsonl``.

.. code:: json

    {"message":"hello anyone there?","date":"10/09","user":"bob"}
    {"message":"need some help with a program","date":"10/09","user":"bob"}
    {"message":"sure thing. What do you need help with?","date":"10/09","user":"dave"}

.. code:: python

    from operator import add
    import re
    messages = seq.jsonl('examples/chat_lots.jsonl')

    # Split words on space and normalize before doing word count
    def extract_words(message):
        return re.sub('[^0-9a-z ]+', '', message.lower()).split(' ')


    word_counts = messages\
        .map(lambda log: extract_words(log['message']))\
        .flatten().map(lambda word: (word, 1))\
        .reduce_by_key(add).order_by(lambda x: x[1])

Next, lets continue that example but introduce a json database of users
from ``examples/users.json``. In the previous example we showed how
``PyFunctional`` can do word counts, in the next example lets show how
``PyFunctional`` can join different data sources.

.. code:: python

    # First read the json file
    users = seq.json('examples/users.json')
    #[('sarah',{'date_created':'08/08','news_email':True,'email':'sarah@gmail.com'}),...]

    email_domains = users.map(lambda u: u[1]['email'].split('@')[1]).distinct()
    # ['yahoo.com', 'python.org', 'gmail.com']

    # Join users with their messages
    message_tuples = messages.group_by(lambda m: m['user'])
    data = users.inner_join(message_tuples)
    # [('sarah',
    #    (
    #      {'date_created':'08/08','news_email':True,'email':'sarah@gmail.com'},
    #      [{'date':'10/10','message':'what is a...','user':'sarah'}...]
    #    )
    #  ),...]

    # From here you can imagine doing more complex analysis

CSV, Aggregate Functions, and Set functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``examples/camping_purchases.csv`` there are a list of camping
purchases. Lets do some cost analysis and compare it the required
camping gear list stored in ``examples/gear_list.txt``.

.. code:: python

    purchases = seq.csv('examples/camping_purchases.csv')
    total_cost = purchases.select(lambda row: int(row[2])).sum()
    # 1275

    most_expensive_item = purchases.max_by(lambda row: int(row[2]))
    # ['4', 'sleeping bag', ' 350']

    purchased_list = purchases.select(lambda row: row[1])
    gear_list = seq.open('examples/gear_list.txt').map(lambda row: row.strip())
    missing_gear = gear_list.difference(purchased_list)
    # ['water bottle','gas','toilet paper','lighter','spoons','sleeping pad',...]

In addition to the aggregate functions shown above (``sum`` and
``max_by``) there are many more. Similarly, there are several more set
like functions in addition to ``difference``.

Reading/Writing SQLite3
~~~~~~~~~~~~~~~~~~~~~~~

``PyFunctional`` can read and write to SQLite3 database files. In the
example below, users are read from ``examples/users.db`` which stores
them as rows with columns ``id:Int`` and ``name:String``.

.. code:: python

    db_path = 'examples/users.db'
    users = seq.sqlite3(db_path, 'select * from user').to_list()
    # [(1, 'Tom'), (2, 'Jack'), (3, 'Jane'), (4, 'Stephan')]]

    sorted_users = seq.sqlite3(db_path, 'select * from user order by name').to_list()
    # [(2, 'Jack'), (3, 'Jane'), (4, 'Stephan'), (1, 'Tom')]

Writing to a SQLite3 database is similarly easy

.. code:: python

    import sqlite3
    from collections import namedtuple

    with sqlite3.connect(':memory:') as conn:
        conn.execute('CREATE TABLE user (id INT, name TEXT)')
        conn.commit()
        User = namedtuple('User', 'id name')

        # Write using a specific query
        seq([(1, 'pedro'), (2, 'fritz')]).to_sqlite3(conn, 'INSERT INTO user (id, name) VALUES (?, ?)')

        # Write by inserting values positionally from a tuple/list into named table
        seq([(3, 'sam'), (4, 'stan')]).to_sqlite3(conn, 'user')

        # Write by inferring schema from namedtuple
        seq([User(name='tom', id=5), User(name='keiga', id=6)]).to_sqlite3(conn, 'user')

        # Write by inferring schema from dict
        seq([dict(name='david', id=7), dict(name='jordan', id=8)]).to_sqlite3(conn, 'user')

        # Read everything back to make sure it wrote correctly
        print(list(conn.execute('SELECT * FROM user')))

        # [(1, 'pedro'), (2, 'fritz'), (3, 'sam'), (4, 'stan'), (5, 'tom'), (6, 'keiga'), (7, 'david'), (8, 'jordan')]

Writing to files
~~~~~~~~~~~~~~~~

Just as ``PyFunctional`` can read from ``csv``, ``json``, ``jsonl``,
``sqlite3``, and text files, it can also write them. For complete API
documentation see the collections API table or the official docs.

Documentation
-------------

Summary documentation is below and full documentation is at
`scalafunctional.readthedocs.org <http://scalafunctional.readthedocs.org/en/latest/functional.html>`__.

Streams API
~~~~~~~~~~~

All of ``PyFunctional`` streams can be accessed through the ``seq``
object. The primary way to create a stream is by calling ``seq`` with an
iterable. The ``seq`` callable is smart and is able to accept multiple
types of parameters as shown in the examples below.

.. code:: python

    # Passing a list
    seq([1, 1, 2, 3]).to_set()
    # [1, 2, 3]

    # Passing direct arguments
    seq(1, 1, 2, 3).map(lambda x: x).to_list()
    # [1, 1, 2, 3]

    # Passing a single value
    seq(1).map(lambda x: -x).to_list()
    # [-1]

``seq`` also provides entry to other streams as attribute functions as
shown below.

.. code:: python

    # number range
    seq.range(10)

    # text file
    seq.open('filepath')

    # json file
    seq.json('filepath')

    # jsonl file
    seq.jsonl('filepath')

    # csv file
    seq.csv('filepath')

    # sqlite3 db and sql query
    seq.sqlite3('filepath', 'select * from data')

For more information on the parameters that these functions can take,
reference the `streams
documentation <http://scalafunctional.readthedocs.org/en/latest/functional.html#module-functional.streams>`__

Transformations and Actions APIs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Below is the complete list of functions which can be called on a stream
object from ``seq``. For complete documentation reference
`transformation and actions
API <http://scalafunctional.readthedocs.org/en/latest/functional.html#module-functional.pipeline>`__.

+----------+--------------+-------+
| Function | Description  | Type  |
+==========+==============+=======+
| ``map(fu | Maps         | trans |
| nc)/sele | ``func``     | forma |
| ct(func) | onto         | tion  |
| ``       | elements of  |       |
|          | sequence     |       |
+----------+--------------+-------+
| ``filter | Filters      | trans |
| (func)/w | elements of  | forma |
| here(fun | sequence to  | tion  |
| c)``     | only those   |       |
|          | where        |       |
|          | ``func(eleme |       |
|          | nt)``        |       |
|          | is ``True``  |       |
+----------+--------------+-------+
| ``filter | Filters      | trans |
| _not(fun | elements of  | forma |
| c)``     | sequence to  | tion  |
|          | only those   |       |
|          | where        |       |
|          | ``func(eleme |       |
|          | nt)``        |       |
|          | is ``False`` |       |
+----------+--------------+-------+
| ``flatte | Flattens     | trans |
| n()``    | sequence of  | forma |
|          | lists to a   | tion  |
|          | single       |       |
|          | sequence     |       |
+----------+--------------+-------+
| ``flat_m | ``func``     | trans |
| ap(func) | must return  | forma |
| ``       | an iterable. | tion  |
|          | Maps         |       |
|          | ``func`` to  |       |
|          | each         |       |
|          | element,     |       |
|          | then merges  |       |
|          | the result   |       |
|          | to one flat  |       |
|          | sequence     |       |
+----------+--------------+-------+
| ``group_ | Groups       | trans |
| by(func) | sequence     | forma |
| ``       | into         | tion  |
|          | ``(key, valu |       |
|          | e)``         |       |
|          | pairs where  |       |
|          | ``key=func(e |       |
|          | lement)``    |       |
|          | and          |       |
|          | ``value`` is |       |
|          | from the     |       |
|          | original     |       |
|          | sequence     |       |
+----------+--------------+-------+
| ``group_ | Groups       | trans |
| by_key() | sequence of  | forma |
| ``       | ``(key, valu | tion  |
|          | e)``         |       |
|          | pairs by     |       |
|          | ``key``      |       |
+----------+--------------+-------+
| ``reduce | Reduces list | trans |
| _by_key( | of           | forma |
| func)``  | ``(key, valu | tion  |
|          | e)``         |       |
|          | pairs using  |       |
|          | ``func``     |       |
+----------+--------------+-------+
| ``union( | Union of     | trans |
| other)`` | unique       | forma |
|          | elements in  | tion  |
|          | sequence and |       |
|          | ``other``    |       |
+----------+--------------+-------+
| ``inters | Intersection | trans |
| ection(o | of unique    | forma |
| ther)``  | elements in  | tion  |
|          | sequence and |       |
|          | ``other``    |       |
+----------+--------------+-------+
| ``differ | New sequence | trans |
| ence(oth | with unique  | forma |
| er)``    | elements     | tion  |
|          | present in   |       |
|          | sequence but |       |
|          | not in       |       |
|          | ``other``    |       |
+----------+--------------+-------+
| ``symmet | New sequence | trans |
| ric_diff | with unique  | forma |
| erence(o | elements     | tion  |
| ther)``  | present in   |       |
|          | sequnce or   |       |
|          | ``other``,   |       |
|          | but not both |       |
+----------+--------------+-------+
| ``distin | Returns      | trans |
| ct()``   | distinct     | forma |
|          | elements of  | tion  |
|          | sequence.    |       |
|          | Elements     |       |
|          | must be      |       |
|          | hashable     |       |
+----------+--------------+-------+
| ``distin | Returns      | trans |
| ct_by(fu | distinct     | forma |
| nc)``    | elements of  | tion  |
|          | sequence     |       |
|          | using        |       |
|          | ``func`` as  |       |
|          | a key        |       |
+----------+--------------+-------+
| ``drop(n | Drop the     | trans |
| )``      | first ``n``  | forma |
|          | elements of  | tion  |
|          | the sequence |       |
+----------+--------------+-------+
| ``drop_r | Drop the     | trans |
| ight(n)` | last ``n``   | forma |
| `        | elements of  | tion  |
|          | the sequence |       |
+----------+--------------+-------+
| ``drop_w | Drop         | trans |
| hile(fun | elements     | forma |
| c)``     | while        | tion  |
|          | ``func``     |       |
|          | evaluates to |       |
|          | ``True``,    |       |
|          | then returns |       |
|          | the rest     |       |
+----------+--------------+-------+
| ``take(n | Returns      | trans |
| )``      | sequence of  | forma |
|          | first ``n``  | tion  |
|          | elements     |       |
+----------+--------------+-------+
| ``take_w | Take         | trans |
| hile(fun | elements     | forma |
| c)``     | while        | tion  |
|          | ``func``     |       |
|          | evaluates to |       |
|          | ``True``,    |       |
|          | then drops   |       |
|          | the rest     |       |
+----------+--------------+-------+
| ``init() | Returns      | trans |
| ``       | sequence     | forma |
|          | without the  | tion  |
|          | last element |       |
+----------+--------------+-------+
| ``tail() | Returns      | trans |
| ``       | sequence     | forma |
|          | without the  | tion  |
|          | first        |       |
|          | element      |       |
+----------+--------------+-------+
| ``inits( | Returns      | trans |
| )``      | consecutive  | forma |
|          | inits of     | tion  |
|          | sequence     |       |
+----------+--------------+-------+
| ``tails( | Returns      | trans |
| )``      | consecutive  | forma |
|          | tails of     | tion  |
|          | sequence     |       |
+----------+--------------+-------+
| ``zip(ot | Zips the     | trans |
| her)``   | sequence     | forma |
|          | with         | tion  |
|          | ``other``    |       |
+----------+--------------+-------+
| ``zip_wi | Zips the     | trans |
| th_index | sequence     | forma |
| (start=0 | with the     | tion  |
| )``      | index        |       |
|          | starting at  |       |
|          | ``start`` on |       |
|          | the right    |       |
|          | side         |       |
+----------+--------------+-------+
| ``enumer | Zips the     | trans |
| ate(star | sequence     | forma |
| t=0)``   | with the     | tion  |
|          | index        |       |
|          | starting at  |       |
|          | ``start`` on |       |
|          | the left     |       |
|          | side         |       |
+----------+--------------+-------+
| ``inner_ | Returns      | trans |
| join(oth | inner join   | forma |
| er)``    | of sequence  | tion  |
|          | with other.  |       |
|          | Must be a    |       |
|          | sequence of  |       |
|          | ``(key, valu |       |
|          | e)``         |       |
|          | pairs        |       |
+----------+--------------+-------+
| ``outer_ | Returns      | trans |
| join(oth | outer join   | forma |
| er)``    | of sequence  | tion  |
|          | with other.  |       |
|          | Must be a    |       |
|          | sequence of  |       |
|          | ``(key, valu |       |
|          | e)``         |       |
|          | pairs        |       |
+----------+--------------+-------+
| ``left_j | Returns left | trans |
| oin(othe | join of      | forma |
| r)``     | sequence     | tion  |
|          | with other.  |       |
|          | Must be a    |       |
|          | sequence of  |       |
|          | ``(key, valu |       |
|          | e)``         |       |
|          | pairs        |       |
+----------+--------------+-------+
| ``right_ | Returns      | trans |
| join(oth | right join   | forma |
| er)``    | of sequence  | tion  |
|          | with other.  |       |
|          | Must be a    |       |
|          | sequence of  |       |
|          | ``(key, valu |       |
|          | e)``         |       |
|          | pairs        |       |
+----------+--------------+-------+
| ``join(o | Returns join | trans |
| ther, jo | of sequence  | forma |
| in_type= | with other   | tion  |
| 'inner') | as specified |       |
| ``       | by           |       |
|          | ``join_type` |       |
|          | `.           |       |
|          | Must be a    |       |
|          | sequence of  |       |
|          | ``(key, valu |       |
|          | e)``         |       |
|          | pairs        |       |
+----------+--------------+-------+
| ``partit | Partitions   | trans |
| ion(func | the sequence | forma |
| )``      | into         | tion  |
|          | elements     |       |
|          | which        |       |
|          | satisfy      |       |
|          | ``func(eleme |       |
|          | nt)``        |       |
|          | and those    |       |
|          | that don't   |       |
+----------+--------------+-------+
| ``groupe | Partitions   | trans |
| d(size)` | the elements | forma |
| `        | into groups  | tion  |
|          | of size      |       |
|          | ``size``     |       |
+----------+--------------+-------+
| ``sorted | Returns      | trans |
| (key=Non | elements     | forma |
| e, rever | sorted       | tion  |
| se=False | according to |       |
| )/order_ | python       |       |
| by(func) | ``sorted``   |       |
| ``       |              |       |
+----------+--------------+-------+
| ``revers | Returns the  | trans |
| e()``    | reversed     | forma |
|          | sequence     | tion  |
+----------+--------------+-------+
| ``slice( | Sequence     | trans |
| start, u | starting at  | forma |
| ntil)``  | ``start``    | tion  |
|          | and          |       |
|          | including    |       |
|          | elements up  |       |
|          | to ``until`` |       |
+----------+--------------+-------+
| ``head() | Returns      | actio |
| ``       | first        | n     |
| /        | element in   |       |
| ``first( | sequence     |       |
| )``      |              |       |
+----------+--------------+-------+
| ``head_o | Returns      | actio |
| ption()` | first        | n     |
| `        | element in   |       |
|          | sequence or  |       |
|          | ``None`` if  |       |
|          | its empty    |       |
+----------+--------------+-------+
| ``last() | Returns last | actio |
| ``       | element in   | n     |
|          | sequence     |       |
+----------+--------------+-------+
| ``last_o | Returns last | actio |
| ption()` | element in   | n     |
| `        | sequence or  |       |
|          | ``None`` if  |       |
|          | its empty    |       |
+----------+--------------+-------+
| ``len()` | Returns      | actio |
| `        | length of    | n     |
| /        | sequence     |       |
| ``size() |              |       |
| ``       |              |       |
+----------+--------------+-------+
| ``count( | Returns      | actio |
| func)``  | count of     | n     |
|          | elements in  |       |
|          | sequence     |       |
|          | where        |       |
|          | ``func(eleme |       |
|          | nt)``        |       |
|          | is True      |       |
+----------+--------------+-------+
| ``empty( | Returns      | actio |
| )``      | ``True`` if  | n     |
|          | the sequence |       |
|          | has zero     |       |
|          | length       |       |
+----------+--------------+-------+
| ``non_em | Returns      | actio |
| pty()``  | ``True`` if  | n     |
|          | sequence has |       |
|          | non-zero     |       |
|          | length       |       |
+----------+--------------+-------+
| ``all()` | Returns      | actio |
| `        | ``True`` if  | n     |
|          | all elements |       |
|          | in sequence  |       |
|          | are truthy   |       |
+----------+--------------+-------+
| ``exists | Returns      | actio |
| (func)`` | ``True`` if  | n     |
|          | ``func(eleme |       |
|          | nt)``        |       |
|          | for any      |       |
|          | element in   |       |
|          | the sequence |       |
|          | is ``True``  |       |
+----------+--------------+-------+
| ``for_al | Returns      | actio |
| l(func)` | ``True`` if  | n     |
| `        | ``func(eleme |       |
|          | nt)``        |       |
|          | is ``True``  |       |
|          | for all      |       |
|          | elements in  |       |
|          | the sequence |       |
+----------+--------------+-------+
| ``find(f | Returns the  | actio |
| unc)``   | element that | n     |
|          | first        |       |
|          | evaluates    |       |
|          | ``func(eleme |       |
|          | nt)``        |       |
|          | to ``True``  |       |
+----------+--------------+-------+
| ``any()` | Returns      | actio |
| `        | ``True`` if  | n     |
|          | any element  |       |
|          | in sequence  |       |
|          | is truthy    |       |
+----------+--------------+-------+
| ``max()` | Returns      | actio |
| `        | maximal      | n     |
|          | element in   |       |
|          | sequence     |       |
+----------+--------------+-------+
| ``min()` | Returns      | actio |
| `        | minimal      | n     |
|          | element in   |       |
|          | sequence     |       |
+----------+--------------+-------+
| ``max_by | Returns      | actio |
| (func)`` | element with | n     |
|          | maximal      |       |
|          | value        |       |
|          | ``func(eleme |       |
|          | nt)``        |       |
+----------+--------------+-------+
| ``min_by | Returns      | actio |
| (func)`` | element with | n     |
|          | minimal      |       |
|          | value        |       |
|          | ``func(eleme |       |
|          | nt)``        |       |
+----------+--------------+-------+
| ``sum()/ | Returns the  | actio |
| sum(proj | sum of       | n     |
| ection)` | elements     |       |
| `        | possibly     |       |
|          | using a      |       |
|          | projection   |       |
+----------+--------------+-------+
| ``produc | Returns the  | actio |
| t()/prod | product of   | n     |
| uct(proj | elements     |       |
| ection)` | possibly     |       |
| `        | using a      |       |
|          | projection   |       |
+----------+--------------+-------+
| ``averag | Returns the  | actio |
| e()/aver | average of   | n     |
| age(proj | elements     |       |
| ection)` | possibly     |       |
| `        | using a      |       |
|          | projection   |       |
+----------+--------------+-------+
| ``aggreg | Aggregate    | actio |
| ate(func | using        | n     |
| )/aggreg | ``func``     |       |
| ate(seed | starting     |       |
| , func)/ | with         |       |
| aggregat | ``seed`` or  |       |
| e(seed,  | first        |       |
| func, re | element of   |       |
| sult_map | list then    |       |
| )``      | apply        |       |
|          | ``result_map |       |
|          | ``           |       |
|          | to the       |       |
|          | result       |       |
+----------+--------------+-------+
| ``fold_l | Reduces      | actio |
| eft(zero | element from | n     |
| _value,  | left to      |       |
| func)``  | right using  |       |
|          | ``func`` and |       |
|          | initial      |       |
|          | value        |       |
|          | ``zero_value |       |
|          | ``           |       |
+----------+--------------+-------+
| ``fold_r | Reduces      | actio |
| ight(zer | element from | n     |
| o_value, | right to     |       |
|  func)`` | left using   |       |
|          | ``func`` and |       |
|          | initial      |       |
|          | value        |       |
|          | ``zero_value |       |
|          | ``           |       |
+----------+--------------+-------+
| ``make_s | Returns      | actio |
| tring(se | string with  | n     |
| parator) | ``separator` |       |
| ``       | `            |       |
|          | between each |       |
|          | ``str(elemen |       |
|          | t)``         |       |
+----------+--------------+-------+
| ``dict(d | Converts a   | actio |
| efault=N | sequence of  | n     |
| one)``   | ``(Key, Valu |       |
| /        | e)``         |       |
| ``to_dic | pairs to a   |       |
| t(defaul | ``dictionary |       |
| t=None)` | ``.          |       |
| `        | If           |       |
|          | ``default``  |       |
|          | is not None, |       |
|          | it must be a |       |
|          | value or     |       |
|          | zero         |       |
|          | argument     |       |
|          | callable     |       |
|          | which will   |       |
|          | be used to   |       |
|          | create a     |       |
|          | ``collection |       |
|          | s.defaultdic |       |
|          | t``          |       |
+----------+--------------+-------+
| ``list() | Converts     | actio |
| ``       | sequence to  | n     |
| /        | a list       |       |
| ``to_lis |              |       |
| t()``    |              |       |
+----------+--------------+-------+
| ``set()  | Converts     | actio |
| / to_set | sequence to  | n     |
| ()``     | a set        |       |
+----------+--------------+-------+
| ``to_fil | Saves the    | actio |
| e(path)` | sequence to  | n     |
| `        | a file at    |       |
|          | path with    |       |
|          | each element |       |
|          | on a newline |       |
+----------+--------------+-------+
| ``to_csv | Saves the    | actio |
| (path)`` | sequence to  | n     |
|          | a csv file   |       |
|          | at path with |       |
|          | each element |       |
|          | representing |       |
|          | a row        |       |
+----------+--------------+-------+
| ``to_jso | Saves the    | actio |
| nl(path) | sequence to  | n     |
| ``       | a jsonl file |       |
|          | with each    |       |
|          | element      |       |
|          | being        |       |
|          | transformed  |       |
|          | to json and  |       |
|          | printed to a |       |
|          | new line     |       |
+----------+--------------+-------+
| ``to_jso | Saves the    | actio |
| n(path)` | sequence to  | n     |
| `        | a json file. |       |
|          | The contents |       |
|          | depend on if |       |
|          | the json     |       |
|          | root is an   |       |
|          | array or     |       |
|          | dictionary   |       |
+----------+--------------+-------+
| ``to_sql | Save the     | actio |
| ite3(con | sequence to  | n     |
| n, table | a SQLite3    |       |
| name_or_ | db. The      |       |
| query, * | target table |       |
| args, ** | must be      |       |
| kwargs)` | created in   |       |
| `        | advance.     |       |
+----------+--------------+-------+
| ``to_pan | Converts the | actio |
| das(colu | sequence to  | n     |
| mns=None | a pandas     |       |
| )``      | DataFrame    |       |
+----------+--------------+-------+
| ``cache( | Forces       | actio |
| )``      | evaluation   | n     |
|          | of sequence  |       |
|          | immediately  |       |
|          | and caches   |       |
|          | the result   |       |
+----------+--------------+-------+
| ``for_ea | Executes     | actio |
| ch(func) | ``func`` on  | n     |
| ``       | each element |       |
|          | of the       |       |
|          | sequence     |       |
+----------+--------------+-------+

Lazy Execution
~~~~~~~~~~~~~~

Whenever possible, ``PyFunctional`` will compute lazily. This is
accomplished by tracking the list of transformations that have been
applied to the sequence and only evaluating them when an action is
called. In ``PyFunctional`` this is called tracking lineage. This is
also responsible for the ability for ``PyFunctional`` to cache results
of computation to prevent expensive re-computation. This is
predominantly done to preserve sensible behavior and used sparingly. For
example, calling ``size()`` will cache the underlying sequence. If this
was not done and the input was an iterator, then further calls would
operate on an expired iterator since it was used to compute the length.
Similarly, ``repr`` also caches since it is most often used during
interactive sessions where its undesirable to keep recomputing the same
value. Below are some examples of inspecting lineage.

.. code:: python

    def times_2(x):
        print(x)
        return 2 * x
    elements = seq(1, 1, 2, 3, 4).map(times_2).distinct()
    elements._lineage
    # Lineage: sequence -> map(times_2) -> distinct

    l_elements = elements.to_list()
    # Prints: 1
    # Prints: 1
    # Prints: 2
    # Prints: 3
    # Prints: 4

    elements._lineage
    # Lineage: sequence -> map(times_2) -> distinct -> cache

    l_elements = elements.to_list()
    # The cached result is returned so times_2 is not called and nothing is printed

Files are given special treatment if opened through the ``seq.open`` and
related APIs. ``functional.util.ReusableFile`` implements a wrapper
around the standard python file to support multiple iteration over a
single file object while correctly handling iteration termination and
file closing.

Road Map
--------

-  Parallel execution engine for faster computation ``0.5.0``
-  SQL based query planner and interpreter (TBD on if/when/how this
   would be done)
-  When is this ready for ``1.0``?
-  Perhaps think of a better name that better suits this package than
   ``PyFunctional``

Contributing and Bug Fixes
--------------------------

Any contributions or bug reports are welcome. Thus far, there is a 100%
acceptance rate for pull requests and contributors have offered valuable
feedback and critique on code. It is great to hear from users of the
package, especially what it is used for, what works well, and what could
be improved.

To contribute, create a fork of ``PyFunctional``, make your changes,
then make sure that they pass when running on
`TravisCI <travis-ci.org>`__ (you may need to sign up for an account and
link Github). In order to be merged, all pull requests must:

-  Pass all the unit tests
-  Pass all the pylint tests, or ignore warnings with explanation of why
   its correct to do so
-  Must include tests that cover all new code paths
-  Must not decrease code coverage (currently at 100% and tested by
   `coveralls.io <coveralls.io/github/EntilZha/ScalaFunctional>`__)
-  Edit the ``CHANGELOG.md`` file in the ``Next Release`` heading with
   changes

Contact
-------

`Google Groups mailing
list <https://groups.google.com/forum/#!forum/scalafunctional>`__

`Gitter for chat <https://gitter.im/EntilZha/ScalaFunctional>`__

Supported Python Versions
-------------------------

``PyFunctional`` supports and is tested against Python 2.7, 3.3, 3.4,
3.5, PyPy, and PyPy3

Changelog
---------

`Changelog <https://github.com/EntilZha/ScalaFunctional/blob/master/CHANGELOG.md>`__

About me
--------

To learn more about me (the author) visit my webpage at
`pedrorodriguez.io <http://pedrorodriguez.io>`__.

I am a PhD student in Computer Science at the University of Colorado at
Boulder. My research interests include large-scale machine learning,
distributed computing, and adjacent fields. I completed my undergraduate
degree in Computer Science at UC Berkeley in 2015. I have previously
done research in the UC Berkeley AMPLab with Apache Spark, worked at
Trulia as a data scientist, and developed several corporate and personal
websites.

I created ``PyFunctional`` while using Python extensively at Trulia, and
finding that I missed the ease of use for manipulating data that Spark
RDDs and Scala collections have. The project takes the best ideas from
these APIs as well as LINQ to provide an easy way to manipulate data
when using Scala is not an option or Spark is overkill.

Contributors
------------

These people have generously contributed their time to improving
``PyFunctional``

-  `adrian17 <https://github.com/adrian17>`__
-  `lucidfrontier45 <https://github.com/lucidfrontier45>`__
-  `Digenis <https://github.com/Digenis>`__
-  `ChuyuHsu <https://github.com/ChuyuHsu>`__

.. |TravisCI| image:: https://travis-ci.org/EntilZha/ScalaFunctional.svg?branch=master
   :target: https://travis-ci.org/EntilZha/ScalaFunctional
.. |Coverage by codecov.io| image:: https://codecov.io/github/EntilZha/ScalaFunctional/coverage.svg?branch=master
   :target: https://codecov.io/github/EntilZha/ScalaFunctional?branch=master
.. |ReadTheDocs| image:: https://readthedocs.org/projects/scalafunctional/badge/?version=latest
   :target: http://scalafunctional.readthedocs.org/en/
.. |Latest Version| image:: https://badge.fury.io/py/scalafunctional.svg
   :target: https://pypi.python.org/pypi/scalafunctional/
.. |Gitter| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/EntilZha/ScalaFunctional?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge


