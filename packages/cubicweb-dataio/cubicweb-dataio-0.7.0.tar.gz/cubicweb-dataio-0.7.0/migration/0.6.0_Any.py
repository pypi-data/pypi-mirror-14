session.system_sql('TRUNCATE TABLE is_relation')
session.system_sql('INSERT INTO is_relation (eid_from, eid_to) '
                   'SELECT e.eid, t.cw_eid FROM entities AS e, cw_cwetype AS t '
                   'WHERE e.type = t.cw_name')
