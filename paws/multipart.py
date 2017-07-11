import re

from cgi import parse_header, valid_boundary
from io import BytesIO

BOUNDARY_RE = re.compile("^[ -~]{0,200}[!-~]$")


class File:
    '''
    Light weight convenience wrapper for Files in POST data.
    '''
    __slots__ = ('data', 'filename', 'file')

    def __init__(self, data, filename=''):
        self.data = data
        self.filename = filename
        self.file = BytesIO(data)


def parse_multipart(fp, pdict):
    """Parse multipart input.

    Arguments:
    fp   : input file
    pdict: dictionary containing other parameters of content-type header

    Returns a dictionary just like parse_qs(): keys are the field names, each
    value is a list of values for that field.  This is easy to use but not
    much good if you are expecting megabytes to be uploaded -- in that case,
    use the FieldStorage class instead which is much more flexible.  Note
    that content-type is the raw, unparsed contents of the content-type
    header.

    """
    import http.client

    boundary = b""
    if 'boundary' in pdict:
        boundary = pdict['boundary']
    if not valid_boundary(boundary):
        raise ValueError('Invalid boundary in multipart form: %r' % (boundary,))

    nextpart = b"--" + boundary
    lastpart = b"--" + boundary + b"--"
    partdict = {}
    terminator = b""

    while terminator != lastpart:
        bytes = -1
        data = None
        if terminator:
            # At start of next part.  Read headers first.
            headers = http.client.parse_headers(fp)
            clength = headers.get('content-length')
            if clength:
                try:
                    bytes = int(clength)
                except ValueError:
                    pass
            if bytes > 0:
                data = fp.read(bytes)
            else:
                data = b""
        # Read lines until end of part.
        lines = []
        while 1:
            line = fp.readline()
            if not line:
                terminator = lastpart  # End outer loop
                break
            if line.startswith(b"--"):
                terminator = line.rstrip()
                if terminator in (nextpart, lastpart):
                    break
            lines.append(line)
        # Done with part.
        if data is None:
            continue
        if bytes < 0:
            if lines:
                # Strip final line terminator
                line = lines[-1]
                if line[-2:] == b"\r\n":
                    line = line[:-2]
                elif line[-1:] == b"\n":
                    line = line[:-1]
                lines[-1] = line
                data = b"".join(lines)
        line = headers['content-disposition']
        if not line:
            continue
        key, params = parse_header(line)
        if key != 'form-data':
            continue
        if 'name' in params:
            name = params['name']
        else:
            continue
        if 'filename' in params:
            data = File(data, params['filename'])
        if name in partdict:
            partdict[name].append(data)
        else:
            partdict[name] = [data]

    return partdict
