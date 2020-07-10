
CSRF_COOKIE_SECURE = False



#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_PROXY_SSL_HEADER = None 
#https://docs.djangoproject.com/en/3.0/ref/settings/#secure-proxy-ssl-header
#A tuple representing a HTTP header/value combination that 
# signifies a request is secure.
# This controls the behavior of the request object’s is_secure() method.