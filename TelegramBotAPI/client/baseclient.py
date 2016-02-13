from TelegramBotAPI.types.compound import Error


class BaseClient(object):
    def __init__(self, token):
        self.__token = token

    def _get_post_url(self, method):
        return 'https://api.telegram.org/bot%s/%s' % (self.__token, method._name)

    def _interpret_response(self, value, method):
        if value['ok'] is not True:
            e = Error()
            e._from_raw(value)
            raise Exception("method: %s\nresponse: %s" % (method, e,))

        if isinstance(value['result'], list):
            responses = []
            for result in value['result']:
                m = method._response()
                m._from_raw(result)
                responses.append(m)
            return responses
        else:
            try:
                m = method._response()
            except TypeError:
                raise Exception('%s._response not defined' % method.__class__.__name__)
            m._from_raw(value['result'])
            return m

    def _check_response_status(self, status, url, proxy, get_body):
        if status != 200:
            raise Exception("Server error: %s: %s\n%s\n%s" %
                            (status, url, proxy, get_body()))
