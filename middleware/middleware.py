# -*- coding: utf-8 -*-
#钩子和应用的顺序
#process_request() process_view() process_exception() process_template_response() process_response()
#在中间件内部，从process_request 或process_view 中访问request.POST 或request.REQUEST
# 将阻碍该中间件之后的所有视图无法修改请求的上传处理程序，一般情况下要避免这样使用。
#类CsrfViewMiddleware可以被认为是个例外，因为它提供csrf_exempt() 和csrf_protect()两个装饰器，
# 允许视图显式控制在哪个点需要开启CSRF验证。