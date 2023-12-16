#coding=utf-8

settings = dict(
        template_path='../templates', #set model path
        static_path='../static', #set static file path
        debug=True, #debug model
        cookie_secret='Z0Mkq5NPEWSk9fi', #cookie secret type
        login_url='/auth/user_login', #auth path
        xsrf_cookies=False, # again attack
        #ui_methods=admin_uimethods,
        #pycket info
        pycket={
            #'engine': 'redis',
            'engine': 'memcached',
            'storage': {
                'servers': ('localhost:11211',)
            },
            'cookies': {
                'expires_days': 30, #set expire date
                #'max_age':5000,
            }
        }
)

sign=""


