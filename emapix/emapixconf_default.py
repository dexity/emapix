

DEBUG   = True
ADMINS = (
    ('Alex Dementsov', 'dexity@gmail.com'),
)
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