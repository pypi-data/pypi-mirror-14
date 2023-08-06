# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"Import CSV-like data into CubicWeb"

from cubes.dataio.interfaces import DEFAULT_CONVERTERS


def csvimport(req, data, model):
    """ Import data from table-like structures with a definition of new entities
    and relations to create.

    Eg: data = [('Paris', 'France', 'Londres', 'Angleterre', 'Eurostar')]

    To import the 4 columns that make up the 2 cities, one could use the
    following:
    model = {'entities':[{'name': 'City1',
                          'etype': 'Commune',
                          'attributes': {'label': 0, 'country': 1}},
                         {'name': 'City2',
                          'etype': 'Commune',
                          'attributes': {'label': 2, 'country': 3}}]
             'relations': [('City1, 'connected_with', 'City2'),]}

    """
    # Pre-fetch existing entities for types that have a 'unique_on'.
    # They will be reused later on instead of creating new entities for
    # each row of 'data'.
    existing_entities = {}
    for emodel in model['entities']:
        unique_on = emodel.get('options', {}).get('unique_on')
        if unique_on:
            rset = req.execute('Any N, X WHERE X is %s, X %s N'
                               % (emodel['etype'], unique_on))
            existing_entities[emodel['etype']] = dict(rset)
    #
    for row in data:
        row_entities = {}
        for emodel in model['entities']:
            etype = emodel['etype']
            # extract attributes for each entity we want to create for a
            # given row
            attrs = {}
            for attr, col_idx in emodel['attributes'].iteritems():
                attr_type = req.cnx._repo.schema.rschema(attr).objects()[0]
                attrs[attr] = DEFAULT_CONVERTERS[attr_type](row[col_idx])
            # entity creation (or re-use if 'unique_on')
            unique_on = emodel.get('options', {}).get('unique_on')
            if unique_on and existing_entities[etype].get(attrs[unique_on]):
                eid = existing_entities[etype].get(attrs[unique_on])
            else:
                entity = req.create_entity(etype, **attrs)
                eid = entity.eid
                if unique_on:
                    existing_entities[etype][attrs[unique_on]] = eid
            row_entities[emodel['name']] = eid
        # relation creation
        for subj, rtype, obj in model['relations']:
            subj = row_entities.get(subj)
            obj = row_entities.get(obj)
            if subj and obj:
                req.execute('SET S %(rtype)s O WHERE S eid %%(subj)s, O eid %%(obj)s'
                % {'rtype' : rtype}, {'subj' : subj, 'obj': obj})
    #
    req.cnx.commit()
