from flask import Blueprint
from werkzeug.routing import BaseConverter
static_bp = Blueprint('static', __name__, static_folder='../assets', static_url_path='/assets')


def init_app(app):
    # add regex route rule
    """
    #forward request
    @api_bp.route('/<regex(".*"):path>', methods=HTTP_METHODS)
    def remote(path):
        return forward_request(base_url + path)
    """

    class RegexConverter(BaseConverter):
        def __init__(self, url_map, regex):
            super(RegexConverter, self).__init__(url_map)
            self.regex = regex

    app.url_map.converters['regex'] = RegexConverter
