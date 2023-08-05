"""cubicweb-datacat test utilities"""

from cubicweb import Binary


def create_file(cnx, data, data_name=None, **kwargs):
    """Create a File entity"""
    data_name = data_name or data.decode('utf-8')
    kwargs.setdefault('data_format', u'text/plain')
    return cnx.create_entity('File', data=Binary(data),
                             data_name=data_name,
                             **kwargs)


def produce_file(cnx, resourcefeed, inputfile):
    """Simulate the production of `inputfile` by resource feed `resourcefeed`"""
    # Build a transformation process "by hand".
    with cnx.security_enabled(write=False):
        process = cnx.create_entity('DataTransformationProcess',
                                    process_input_file=inputfile,
                                    process_script=resourcefeed.transformation_script)
        cnx.commit()
    iprocess = process.cw_adapt_to('IDataProcess')
    # Add `produced_by` relation.
    with cnx.security_enabled(write=False):
        outfile = iprocess.build_output(inputfile, 'plop')
        cnx.commit()
    return outfile
