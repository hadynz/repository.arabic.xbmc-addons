import httplib
import urlparse

def get_redirect_flv_stream_url(url):
    """
    Al qahera al youm's server redirects a video URL to a FLV file
    location in most times. If location is empty, a YouTube URL is being used
    """
    host, path, params, query = urlparse.urlparse(url)[1:5]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path + '?' + query)
        return conn.getresponse().getheader('location')
    except StandardError:
        return None

def _get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path, params, query = urlparse.urlparse(url)[1:5]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path + '?' + query)
        return conn.getresponse().status
    except StandardError:
        return None

def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return _get_server_status_code(url) in good_codes

def extract_youtube_vid(url):
    if isinstance(url, str):
        url = [url]

    ret_list = []
    for item in url:
        item = item[item.find("v=") + 2:]
        if item.find("&") > -1:
            item = item[:item.find("&")]
        ret_list.append(item)

    return ret_list
