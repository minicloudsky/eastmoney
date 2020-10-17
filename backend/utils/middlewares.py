import json
import math
import time
import functools
from json import JSONDecodeError

from django.urls import resolve

from apps.log.models import Log


def SaveLogMiddleware(func):
    @functools.wraps(func)
    def _inner(request, *args, **kwargs):
        start = time.time()
        bdata = request.body
        if bdata:
            try:
                post_params = json.loads(bdata.decode('utf-8'))
            except JSONDecodeError:
                post_params = {}
        else:
            post_params = {}
        res = func(request, *args, **kwargs)
        end = time.time()
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # 这里是真实的ip
            ip_addr = x_forwarded_for.split(',')[0]
        else:
            # 这里是代理ip
            ip_addr = request.META.get('REMOTE_ADDR')
        req_method = request.method
        api_path = request.path
        if api_path == "/log/log/":
            return res
        get_params = request.GET
        comments = resolve(api_path).url_name
        params_list = []
        if get_params:
            for k, v in dict(get_params).items():
                params_list.append(k + ":" + str(v))
        if post_params:
            for x, y in post_params.items():
                params_list.append(x + ":" + str(y))
        keep_time = math.ceil((end - start) * 1000)
        status_content = ""
        try:
            status_content = res.status_text
        except:
            pass
        Log.objects.create(api_name=api_path,
                           method=req_method,
                           params=",".join(params_list),
                           comments=comments,
                           time=keep_time,
                           ip=ip_addr,
                           username=request.user,
                           status_code=res.status_code,
                           status_text=status_content
                           )
        return res

    return _inner
