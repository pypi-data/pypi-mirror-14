from rest_framework import serializers
from microbot.models import User, Chat, Message, Update, Bot, EnvironmentVar, Handler, Request, UrlParam, HeaderParam
from datetime import datetime
import time


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')
        
class ChatSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Chat
        fields = ('id', 'type', 'title', 'username', 'first_name', 'last_name')
        
class TimestampField(serializers.Field):

    def to_internal_value(self, data):
        return datetime.fromtimestamp(data)
    
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))

        
class MessageSerializer(serializers.HyperlinkedModelSerializer):
    message_id = serializers.IntegerField()
    # reserved word field 'from' changed dynamically
    from_ = UserSerializer(many=False, source="from_user")
    chat = ChatSerializer(many=False)
    date = TimestampField()
    
    def __init__(self, *args, **kwargs):
        super(MessageSerializer, self).__init__(*args, **kwargs)
        self.fields['from'] = self.fields['from_']
        del self.fields['from_']

    class Meta:
        model = Message
        fields = ('message_id', 'from_', 'date', 'chat', 'text')
        
class UpdateSerializer(serializers.HyperlinkedModelSerializer):
    update_id = serializers.IntegerField()
    message = MessageSerializer(many=False)
    
    class Meta:
        model = Update
        fields = ('update_id', 'message')
        
    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data['message']['from_user'])
        
        chat, _ = Chat.objects.get_or_create(**validated_data['message']['chat'])           
        
        message, _ = Message.objects.get_or_create(message_id=validated_data['message']['message_id'],
                                                   from_user=user,
                                                   date=validated_data['message']['date'],
                                                   chat=chat,
                                                   text=validated_data['message']['text'])
        update, _ = Update.objects.get_or_create(update_id=validated_data['update_id'],
                                                 message=message)

        return update
    
class UserAPISerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
    
class BotSerializer(serializers.ModelSerializer):
    info = UserAPISerializer(many=False, source='user_api', read_only=True)
    
    class Meta:
        model = Bot
        fields = ('token', 'created', 'enabled', 'info')
        read_only_fields = ('created', 'info')
        
class EnvironmentVarSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentVar
        fields = ('key', 'value')
        
class AbsParamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UrlParam
        fields = ('key', 'value_template')        
        
class RequestSerializer(serializers.HyperlinkedModelSerializer):
    url_parameters = AbsParamSerializer(many=True)
    header_parameters = AbsParamSerializer(many=True)
    class Meta:
        model = Request
        fields = ('url_template', 'method', 'data', 'url_parameters', 'header_parameters')
        
class HandlerSerializer(serializers.ModelSerializer):
    request = RequestSerializer(many=False)
    class Meta:
        model = Handler
        fields = ('pattern', 'response_text_template', 'response_keyboard_template', 'enabled', 'request')
        
    def _create_params(self, params, model, request):
        for param in params:
            model.objects.get_or_create(key=param['key'],
                                        value_template=param['value_template'],
                                        request=request)  
                
    def _update_params(self, params, query_get):
        for param in params:
            instance_param = query_get(key=param['key'])
            instance_param.key = param['key']
            instance_param.value_template = param['value_template']
            instance_param.save()
                   
    def create(self, validated_data):
        request, _ = Request.objects.get_or_create(**validated_data['request'])
        
        handler, _ = Handler.objects.get_or_create(pattern=validated_data['pattern'],
                                                   response_text_template=validated_data['response_text_template'],
                                                   response_keyboard_template=validated_data['response_keyboard_template'],
                                                   enabled=validated_data['enabled'],
                                                   request=request)
        
        self._create_params(validated_data['request']['url_parameters'], UrlParam, request)
        self._create_params(validated_data['request']['header_parameters'], HeaderParam, request)
            

        return handler
    
    def update(self, instance, validated_data):
        instance.pattern = validated_data.get('pattern', instance.pattern)
        instance.response_text_template = validated_data.get('response_text_template', instance.response_text_template)
        instance.response_keyboard_template = validated_data.get('response_keyboard_template', instance.response_keyboard_template)
        instance.enabled = validated_data.get('enabled', instance.enabled)

        instance.request.url_template = validated_data['request'].get('url_template', instance.request.url_template)
        instance.request.method = validated_data['request'].get('method', instance.request.method)
        instance.request.data = validated_data['request'].get('data', instance.request.data)
        instance.request.save()
        
        self._update_params(validated_data['request']['url_parameters'], instance.request.url_parameters.get)
        self._update_params(validated_data['request']['header_parameters'], instance.request.header_parameters.get)
            
        instance.save()
        return instance
    
    