from flask import request
from werkzeug.datastructures import ImmutableMultiDict


class JWTVerificationMiddleware():
    '''
    Simple JWT verification middleware for a flask app.
    '''

    def __init__(self, app, decoder):
        """
        Input:
            app:                           Flask app handle
            decoder_verifier_handler:      JWT decoder and verifier
                                            This object should have a method called verify() which
                                            takes an argument/variable called <token> and
                                            and an instance variable call <claims> which is updated
                                            after a call to verify is completed
        """
        self.app = app
        self.app.logger.info("initializing jwt decoder middleware")
        self.decoder = decoder

        self.app.before_request(self._before_request)

    def _before_request(self):
        access_token = self.extract_access_token(request.headers)
        request_args = request.args.to_dict()

        if access_token == "null":  # empty accesstoken
            request_args['claims'] = {}
            request_args["claims_error"] = True
            request_args["claims_error_message"] = "Empty Access Token"
            request.args = ImmutableMultiDict(request_args)
            return

        try:
            self.decoder.verify(access_token)
            request_args['claims'] = self.decoder.claims
            request_args["claims_error"] = False
            request_args["claims_error_message"] = ""

        except Exception as e:
            request_args['claims'] = {}
            request_args["claims_error"] = True
            request_args["claims_error_message"] = repr(e)

        request.args = ImmutableMultiDict(request_args)

    @staticmethod
    def extract_access_token(request_headers):
        access_token = None
        auth_header = request_headers.get("Authorization")
        if auth_header and " " in auth_header:
            _, access_token = auth_header.split()
        return access_token