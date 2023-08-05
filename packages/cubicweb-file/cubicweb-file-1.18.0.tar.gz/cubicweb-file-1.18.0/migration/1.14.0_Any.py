add_attribute('File', 'data_sha1hex')

if (config.get('compute-sha1hex') and
    confirm('compute sha1sum for each File ?', default='n')):
    for entity, data in rql('Any X,D WHERE X is File, X data D').iter_rows_with_entities():
        entity.cw_set(data_sha1hex=entity.compute_sha1hex(data.getvalue()))
        entity.cw_clear_all_caches()
    commit()
