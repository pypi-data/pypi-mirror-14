===
django-wechat-web
===

django-wechat-web is a simple Django app to conduct Wechat-web-based helper. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the 'docs' directory.

Quick start
-----------

1. Add 'django_wechat_web' to to your INSTALLED_APPS setting like this::
   
   INSTALLED_APPS = [
        ...
        'django_wechat_web',
   ]

2. Add WECHAT to your settings file::

   WECHAT = {
        'appid': 'YOUR APPID',
        'appsecret': 'YOUR APP Secret',
   }

3. Run `python manage.py makemigrations django_wechat_web; python manage.py migrate` to create the django_wechat_web models.

4. In your app view where your need get wechat user openid, do like this::

   from django_wechat_web import WechatView

   class YourViewName(WechatView):
        '''
            Extends WechatView and over get method
            Here WechatView extends django.views.generic.View
        '''
        scope = 'snsapi_base' # default

        ...


        def get(self, request, *args, **kwargs):
            # your code ....

        ...

5. Now you can do anything the same as `django.views.generic.View`.

6. More:
   django_wechat_web:
    model:
        WechatBase
        WechatUserInfo

    wechat:
        WechatView
