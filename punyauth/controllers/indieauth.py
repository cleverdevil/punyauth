from urllib.parse import urlencode
from datetime import datetime
from pecan import expose, redirect, abort, request, response, conf
from .. import storage

import jwt
import uuid


class AuthorizationController:
    '''
    IndieAuth Authorization Endpoint
    '''

    @expose(template='auth.html', generic=True)
    def index(self, me, client_id, redirect_uri,
              state=None, response_type='id', scope='create'):
        '''
        HTTP GET /indieauth/auth

        An external application identified by `client_id` is requesting
        authorization to perform the actions in `scope` on behalf of the
        user identified by the URL `me`. Once the process is complete,
        we should redirect to the specified `redirect_uri`.

        The external application may optionally provide a `state` parameter
        for its own purposes.

        If the application is only wanting identification, not authorization,
        then it will pass `response_type` as "id." If the application wants
        full authorization, then it will pass `response_type` as "code."
        '''

        return dict(
            me=me,
            client_id=client_id,
            redirect_uri=redirect_uri,
            state=state,
            response_type=response_type,
            scope=scope
        )

    @index.when(method='POST')
    @expose('json')
    @expose(content_type='application/x-www-form-urlencoded', template='urlencode.html')
    def index_post(self, me=None, client_id=None, redirect_uri=None,
                state=None, response_type='id', scope=None,
                approve=None, code=None):
        '''
        If a `code` is passed into this endpoint, then we are to validate
        that authorization code against our database with the `redirect_uri`
        and `client_id` parameters. If we find a match, we are to return
        the `me` URL that is associated with the authorization code.

        If a `code` is not passed into this endpoint, but `approve` is passed
        along as "Approve," then we generate an authorization token, and
        store it in our database, before finally redirecting to the provided
        `redirect_uri`, passing along the `code` and `state`.
        '''

        # verify auth code, if it is provided
        if code is not None:
            found_code = storage.get(dict(
                code=code,
                redirect_uri=redirect_uri,
                client_id=client_id
            ))
            if found_code is not None:
                data = {'me': found_code['me']}
                return data
            abort(401, 'Invalid auth code.')

        # otherwise approve request for auth code
        if approve == 'Approve':
            # generate auth code
            code = str(uuid.uuid4())

            # store code in our storage
            storage.set(dict(
                me=me,
                client_id=client_id,
                redirect_uri=redirect_uri,
                state=state,
                response_type=response_type,
                scope=scope,
                code=code
            ))

            # redirect to the requesting application
            values = urlencode({'code': code, 'state': state})
            uri = redirect_uri + '?' + values
            redirect(uri)


class TokenController:
    '''
    IndieAuth Token Endpoint
    '''

    @expose(generic=True)
    @expose('json')
    @expose(content_type='application/x-www-form-urlencoded', template='urlencode.html')
    def index(self):
        '''
        GET /indieauth/token

        Verify an access token that is provided in the `Authorization`
        header as a `Bearer` token.
        '''

        # pull the token off the Authorization header
        token = request.headers.get(
            'Authorization', 'Bearer XYZ'
        ).split(' ')[1]

        # validate token
        try:
            payload = jwt.decode(
                token,
                conf.token.secret,
                algorithms=[conf.token.algorithm]
            )
            return {
                'me': payload['me'],
                'client_id': payload['client_id'],
                'scope': payload['scope']
            }
        except:
            abort(403, 'Invalid token.')

    @index.when(method='POST')
    @expose('json')
    @expose(content_type='application/x-www-form-urlencoded', template='urlencode.html')
    def index_post(self, code=None, me=None, redirect_uri=None, client_id=None):
        '''
        POST /indieauth/token

        An external application is requesting an access token. They have
        an authorization `code` for the user identified by `me`. We will
        verify the code, and then redirect to the `redirect_uri`, providing
        the verified `me` and `scope` associated with the access `code`.
        '''

        # look for a matching authorization code
        found_code = storage.get(dict(
            code=code,
            redirect_uri=redirect_uri,
            client_id=client_id
        ))

        # if we found one, generate and store a token
        if found_code is not None and found_code['me'] == me:
            # generate a token
            token = jwt.encode({
                'me': me,
                'client_id': client_id,
                'scope': found_code['scope'],
                'date_issued': str(datetime.utcnow()),
                'nonce': str(uuid.uuid4())
            }, conf.token.secret, conf.token.algorithm).decode('utf-8')

            # construct the return payload
            data = {
                'me': found_code['me'],
                'scope': found_code['scope'],
                'access_token': token
            }

            return data

        # if we didn't find one, reject the request
        abort(401, 'Invalid auth code.')


class IndieAuthController:
    auth = AuthorizationController()
    token = TokenController()
