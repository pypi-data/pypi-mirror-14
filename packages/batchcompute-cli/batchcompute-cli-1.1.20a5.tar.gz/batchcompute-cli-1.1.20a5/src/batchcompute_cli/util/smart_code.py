try:
    import unicode
except:
    def unicode(s,encode='utf-8'):
        return str(s, encode)


def format_utf8(string):
    string = smart_code(string)
    if isinstance(string, unicode):
        string = string.encode('utf-8')
    return string


def smart_code(input_stream):
    if isinstance(input_stream, str):
        try:
            tmp = unicode(input_stream, 'utf-8')
        except UnicodeDecodeError:
            try:
                tmp = unicode(input_stream, 'gbk')
            except UnicodeDecodeError:
                try:
                    tmp = unicode(input_stream, 'big5')
                except UnicodeDecodeError:
                    try:
                        tmp = unicode(input_stream, 'ascii')
                    except:
                        tmp = input_stream
    else:
        tmp = input_stream
    return tmp
