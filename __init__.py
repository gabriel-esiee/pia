from authlib.integrations.flask_client import OAuth

oauth = OAuth()

google = oauth.register(
    name='google',
    client_id='72701988235-3bqpnaugrhnl6ktte3ub4i6le7osc9lg.apps.googleusercontent.com',
    client_secret='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',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
