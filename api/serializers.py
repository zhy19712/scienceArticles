from rest_framework import serializers
from api.models import Keyword, ScrapedUrls, Article, Target


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段

        def create(self, validated_data):
            source = validated_data['source']
            url = validated_data['url']
            title = validated_data['title']
            time = validated_data['time']
            text = validated_data['text']
            article = Article.objects.create(
                source=source,
                url=url,
                title=title,
                time=time,
                text=text
            )
            return article

        def update(self, instance, validated_data):
            source = validated_data['source']
            url = validated_data['url']
            title = validated_data['title']
            time = validated_data['time']
            text = validated_data['text']
            instance.source = source
            instance.title = title
            instance.url = url
            instance.time = time
            instance.text = text
            instance.save()
            return instance


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段

        def create(self, validated_data):
            keyword = validated_data['keyword']
            type = validated_data['type']
            article = Article.objects.create(
                keyword=keyword,
                type=type,
            )
            return article

        def update(self, instance, validated_data):
            keyword = validated_data['url']
            type = validated_data['title']
            instance.keyword = keyword
            instance.type = type
            instance.save()
            return instance


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段

        def create(self, validated_data):
            url = validated_data['url']
            name = validated_data['name']
            type = validated_data['type']
            remark = validated_data['remark']
            target = Target.objects.create(
                url=url,
                name=name,
                type=type,
                remark=remark
            )
            return target

        def update(self, instance, validated_data):
            url = validated_data['url']
            name = validated_data['name']
            type = validated_data['type']
            remark = validated_data['remark']

            instance.name = name
            instance.url = url
            instance.type = type
            instance.remark = remark
            instance.save()
            return instance


class ScrapedUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedUrls  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段
