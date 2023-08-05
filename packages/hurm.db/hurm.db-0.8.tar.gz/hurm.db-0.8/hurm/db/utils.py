# -*- coding: utf-8 -*-
# :Project:   hurm -- Utility functions
# :Created:   mar 22 dic 2015 16:34:23 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
#

from sqlalchemy import inspect
from sqlalchemy.exc import NoInspectionAvailable, SQLAlchemyError
from sqlalchemy.orm.collections import InstrumentedList

from . import translatable_string as _, logger


def normalize(s, title=None):
    """Normalize the case of a string, removing spurious spaces.

    :param s: a string
    :param title: if `True` always titleize the string, if `False`
                  never do that, if `None` (default) only when the
                  input string is all lower case or all upper case
    :rtype: unicode

    ::

      >>> assert normalize(None) is None
      >>> print(normalize('lele gaifax'))
      Lele Gaifax
      >>> print(normalize('LELE'))
      Lele
      >>> print(normalize('LeLe', title=False))
      LeLe
    """

    if s is None:
        return None
    else:
        n = ' '.join(s.strip().split())
        if title != False and (title == True or
                               n == n.upper() or
                               n == n.lower()):
            n = n.title()
        return n


def njoin(elts, stringify=str, localized=True):
    """Given a sequence of items, concatenate them in a nice way.

    :param elts: a sequence of elements
    :param stringify: the stringification function applied to all elements,
                      by default :py:func:`str`
    :param localized: a boolean flag to disable the translation of the final 'and'
    :rtype: unicode

    If `elts` is empty returns an empty string; if it contains a single element, returns the
    stringified element; otherwise returns a string composed by all but the last elements
    stringified and joined by a comma, followed by the localized version of `and` followed by
    the last element stringified::

      >>> print(njoin([1,2,3]))
      1, 2 and 3
      >>> print(njoin([1,2]))
      1 and 2
      >>> print(njoin([1]))
      1
      >>> assert njoin([]) == ''
      >>> print(njoin([1,2], stringify=lambda x: str(x*10)))
      10 and 20

    Note that *falsey* elements are skipped::

      >>> print(njoin(['first', None, False, '', 'last']))
      first and last

    but ``0`` (*zero*) isn't considered a *falsey* value::

      >>> print(njoin([1,0,2]))
      1, 0 and 2
    """

    elts = [stringify(e) for e in elts if e or (e == 0 and e is not False)]
    if not elts:
        return ''
    elif len(elts) == 1:
        return elts[0]
    else:
        last = elts[-1]
        if localized:
            # TRANSLATORS: this is the final "conjunction" used when joining multiple
            # statements, for example "x, y and z".
            and_ = ' %s ' % _('and')
        else:
            and_ = ' and '
        return ', '.join(elts[:-1]) + and_ + last


def table_from_primary_key(pkname):
    """Given the name of a primary key, return the related table.

    :param pkname: the name of a primary key
    :rtype: a SQLAlchemy table
    """

    from . import metadata

    for t in metadata.sorted_tables:
        if len(t.primary_key.columns) == 1 and pkname in t.primary_key.columns:
            return t

    raise RuntimeError('Unknown PK: %s' % pkname)


def entity_from_primary_key(pkname):
    """Given the name of a primary key, return the mapped entity.

    :param pkname: the name of a primary key
    :rtype: a mapped class
    """

    from sqlalchemy.orm.mapper import _mapper_registry

    for m in list(_mapper_registry):
        if len(m.primary_key) == 1 and m.primary_key[0].name == pkname:
            return m.class_

    raise RuntimeError('Unknown PK: %s' % pkname)


def changes_summary(changes):
    """Format a set of changes into a nice string.

    :param changes: a mapping of field names to ``(oldvalue, newvalue)`` tuples
    :rtype: a string

      >>> print(changes_summary(dict(a=(None, 1))))
      changed a to 1
      >>> print(changes_summary(dict(a=(False, True))))
      changed a from False to True
      >>> print(changes_summary(dict(a=(0,1), b=('foo','bar'))))
      changed a from 0 to 1 and b from "foo" to "bar"
      >>> print(changes_summary(dict(a=(0,1), b=(None,'bar'), c=(True,None))))
      changed a from 0 to 1, b to "bar" and c from True to None
    """

    summary = []
    for field in sorted(changes):
        oldvalue, newvalue = changes[field]

        if oldvalue is None or oldvalue == '':
            oldvalue = False
        else:
            if isinstance(oldvalue, str):
                oldvalue = '"%s"' % oldvalue
            else:
                oldvalue = str(oldvalue)

        if isinstance(newvalue, str):
            newvalue = '"%s"' % newvalue
        else:
            newvalue = str(newvalue)

        if oldvalue is False:
            summary.append('%s to %s' % (field, newvalue))
        else:
            summary.append('%s from %s to %s' % (field, oldvalue, newvalue))

    return 'changed ' + njoin(summary, localized=False)


def save_changes(sasess, request, modified, deleted, clogger=logger):
    """Save insertions, changes and deletions to the database.

    :param sasess: the SQLAlchemy session
    :param request: the Pyramid web request
    :param modified: a sequence of record changes, each represented by
                     a tuple of two items, the PK name and a
                     dictionary with the modified fields; if the value
                     of the PK field is null or 0 then the record is
                     considered new and will be inserted instead of updated
    :param deleted: a sequence of deletions, each represented by a tuple
                    of two items, the PK name and the ID of the record to
                    be removed
    :param clogger: where to log applied changes
    :rtype: a tuple of three lists, respectively inserted, modified and
            deleted record IDs, grouped in a dictionary keyed on PK name.
    """

    iids = []
    mids = []
    dids = []

    # Dictionary with last inserted PK ids: each newly inserted
    # primary key (records with id==0) is stored here by name, and
    # used for the homonym FK with value of 0. This let us insert a
    # new master record with its details in a single call.
    last_ins_ids = {}

    try:
        for key, mdata in modified:
            entity = entity_from_primary_key(key)

            fvalues = {}
            for f, v in mdata.items():
                if f != key:
                    if v != '':
                        fvalues[f] = v
                    else:
                        fvalues[f] = None

            # Update the NULL foreign keys with previously
            # inserted master ids
            for lik in last_ins_ids:
                if lik != key and fvalues.get(lik) == 0:
                    fvalues[lik] = last_ins_ids[lik]

            # If there are no changes, do not do anything
            if not fvalues:
                continue

            # If the PK is missing or None, assume it's a new record
            idrecord = int(mdata.get(key) or 0)

            if idrecord == 0:
                instance = entity(**fvalues)
                sasess.add(instance)
                sasess.flush()
                nextid = getattr(instance, key)
                iids.append({key: nextid})
                last_ins_ids[key] = nextid
                clogger.info('Inserted new %r', instance)
            else:
                instance = sasess.query(entity).get(idrecord)
                if instance is not None:
                    mids.append({key: idrecord})
                    changes = instance.update(fvalues)
                    sasess.flush()
                    clogger.info('Updated %r: %s', instance, changes_summary(changes))

        for key, ddata in deleted:
            entity = entity_from_primary_key(key)
            instance = sasess.query(entity).get(ddata)
            if instance is not None:
                irepr = repr(instance)
                instance.delete(sasess)
                dids.append({key: ddata})
                clogger.info('Deleted %s', irepr)
    except SQLAlchemyError as e:
        clogger.warning('Changes rolled back due to an exception: %s', e)
        raise
    except:
        clogger.exception('Changes rolled back due to an exception')
        raise

    return iids, mids, dids


def dump(roots, specs):
    specs_by_qualname = {spec['entity']: spec for spec in specs}

    seen = set()
    entities = {}
    instances = {}

    def get_identity(instance):
        klass = instance.__class__
        qualname = instance.__module__ + '.' + klass.__name__
        if qualname not in specs_by_qualname:
            return

        spec = specs_by_qualname[qualname]

        key = spec['key']
        if callable(key):
            key = key(instance)
        if isinstance(key, str):
            identity = (qualname, getattr(instance, key))
        else:
            assert isinstance(key, (tuple, list))
            identity = (qualname, tuple(getattr(instance, f) for f in key))

        return identity

    def visit(instance):
        identity = get_identity(instance)
        if identity is None:
            return

        if identity in seen:
            return instances[identity]

        seen.add(identity)

        qualname = identity[0]
        spec = specs_by_qualname[qualname]
        key = spec['key']

        if qualname in entities:
            entity = entities[qualname]
        else:
            entity = entities[qualname] = {'entity': qualname, 'key': key, 'data': []}

        data = instances[identity] = {}
        entity['data'].append(data)

        attributes = []
        if isinstance(key, str):
            attributes.append(key)
        else:
            attributes.extend(key)

        other = spec.get('other', [])
        if isinstance(other, str):
            attributes.append(other)
        else:
            attributes.extend(other)

        for attr in attributes:
            value = getattr(instance, attr)

            if value is None:
                continue

            if isinstance(value, InstrumentedList):
                for i in value:
                    visit(i)
            else:
                try:
                    inspector = inspect(value)
                except NoInspectionAvailable:
                    data[attr] = value
                else:
                    if inspector.is_instance:
                        value = visit(value)
                        if value is not None:
                            data[attr] = value

        return data

    if isinstance(roots, (list, tuple)):
        for root in roots:
            visit(root)
    else:
        visit(roots)

    return [entities[spec['entity']] for spec in specs
            if spec['entity'] in entities]
