from rest_framework.views import APIView
from rest_framework.parsers import BaseParser
from rest_framework.response import Response
from rest_framework.request import Request
class IndexView(APIView):
    '''
    #根据请求头 content-type 选择对应的解析器就请求体内容进行处理。

    读取客户端发送的Content-Type的值 application/json

    parser_classes = [JSONParser,]
    media_type_list = ['application/json',]

    如果客户端的Content-Type的值和 application/json 匹配：JSONParser处理数据
    如果客户端的Content-Type的值和 application/x-www-form-urlencoded 匹配：FormParser处理数据
    '''
    # parser_classes = [JSONParser, ]  仅处理请求头content-type为application/json的请求体
    # parser_classes = [FormParser, ] 仅处理请求头content-type为application/x-www-form-urlencoded 的请求体
    # parser_classes = [FileUploadParser, ] 仅上传文件
    # parser_classes = [MultiPartParser, ] 仅处理请求头content-type为multipart/form-data的请求体

    # parser_classes = [JSONParser, FormParser, MultiPartParser, ]  当同时使用多个parser时，
    #                   rest framework会根据请求头content-type自动进行比对，并使用对应parser
    def get(self, request, *args, **kwargs):
        self.dispatch
        # 获取请求的值，并使用对应的JSONParser进行处理
        print(request.data)
        # application/x-www-form-urlencoded 或 multipart/form-data时，request.POST中才有值
        print(request.POST)
        print(request.FILES) #  <form action="http://127.0.0.1:8000/test/" method="post" enctype="multipart/form-data">
        return Response('...')