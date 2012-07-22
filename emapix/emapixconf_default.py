

DEBUG   = True
ADMINS = (
    ('Alex Dementsov', 'dexity@gmail.com'),
)

# Email
EMAIL_HOST  = ""
EMAIL_PORT  = ""
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS   = ""

# Amazon S3
S3_KEY      = "AMAZONS3KEY"
S3_SECRET   = "AMAZONS3SECRET"
BUCKET_NAME = "emapix_uploads"

API_KEY     = "tempapikey" # test key for api

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3', 
        'NAME':     '/var/emapix/emapix/emapix.db',
        'USER':     '',
        'PASSWORD': '',
        'HOST':     '',                      
        'PORT':     '',                      
    }
}