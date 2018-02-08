from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from . import models
# =========================================================简单序列化
class UsersSerializer(serializers.Serializer):
    '''
    字段、扩表查询
    '''
    name = serializers.CharField()
    pwd = serializers.CharField()
    group = serializers.CharField(source='group.title')
    menu = serializers.CharField(source='group.menu.name')

class UsersView(APIView):
    def get(self,request,*args,**kwargs):
        # 方式一：
        # user_list = models.UserInfo.objects.all().values('name','pwd','group__id',"group__title")
        # return Response(user_list)
        #方式二：
        user_list = models.UserInfo.objects.all()
        ser = UsersSerializer(instance=user_list,many=True)
        return Response(ser.data)
        # 方式二之单对象
        # user = models.UserInfo.objects.all().first()
        # ser = UsersSerializer(instance=user, many=False)
        # return Response(ser.data)

# =========================================================复杂序列化

class MyCharField(serializers.CharField):
    '''
    自定义to_representation，根据对象获取自己想要的字段
    '''
    def to_representation(self, value):
        values=[]
        for obj in value:
            values.append(obj.name)
        return values

class MyCharField2(serializers.CharField):
    def to_representation(self, value):
        return {'id':value.pk, 'name':value.name}

class IndexSerializer(serializers.Serializer):
    '''
    复杂序列化
    '''
    name = serializers.CharField()  # obj.name
    pwd = serializers.CharField()  # obj.pwd
    group_id = serializers.CharField()  # obj.group_id
    xxxx = serializers.CharField(source="group.title")  # obj.group.title
    x = serializers.CharField(source="group.menu.name")  # obj.menu.name
    x1 = MyCharField(source="roles.all") # obj.mu.name  #第一种方式
    x2 = serializers.ListSerializer(child=MyCharField2(),source="roles.all")  # obj.mu.name #第二种方式
    x3 = serializers.SerializerMethodField() #第三种方式

    def get_x3(self,obj):
        # obj.roles.all()
        role_list = obj.roles.filter(id__gt=0)
        data_list = []
        for row in role_list:
            data_list.append({'pk': row.pk, 'name': row.name})
        return data_list


class IndexView(APIView):
    def get(self,request,*args,**kwargs):

       user_list = models.UserInfo.objects.all()
       ser = IndexSerializer(instance=user_list,many=True)
       return Response(ser.data)

# =========================================================基于Model
class AASerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedIdentityField(view_name='detail') #生成URL
    #需要注意在setting里 ， 版本使用的 DEFAULT_VERSIONING_CLASS
    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        fields = ['name', 'pwd','group']
        depth = 2


class AAView(APIView):
    def get(self,request,*args,**kwargs):
        user_list = models.UserInfo.objects.all()
        # [obj1,obj2,obj3]
        ser = AASerializer(instance=user_list,many=True,context={'request': request})
        #context={'request': request}  ->HyperlinkedIdentityField 它需要用到request
        return Response(ser.data)