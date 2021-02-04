from rest_framework import serializers
from api.models import Keyword, ScrapedUrls, Article, Target, Center, Category, KeywordArticle


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段

        def create(self, validated_data):
            target = validated_data['target']
            url = validated_data['url']
            title = validated_data['title']
            time = validated_data['time']
            text = validated_data['text']
            filepath = validated_data['filepath']
            article = Article.objects.create(
                target=target,
                url=url,
                title=title,
                time=time,
                text=text,
                filepath=filepath,
            )
            return article

        def update(self, instance, validated_data):
            target = validated_data['target']
            url = validated_data['url']
            title = validated_data['title']
            time = validated_data['time']
            text = validated_data['text']
            filepath = validated_data['filepath']
            instance.target = target
            instance.title = title
            instance.url = url
            instance.time = time
            instance.text = text
            instance.filepath = filepath
            instance.save()
            return instance


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段

        def create(self, validated_data):
            center_id = validated_data['center_id']
            category_id = validated_data['category_id']
            keyword = validated_data['keyword']
            type = validated_data['type']
            status = validated_data['status']

            article = Article.objects.create(
                center_id=center_id,
                category_id=category_id,
                keyword=keyword,
                type=type,
                status=status,
            )
            return article

        def update(self, instance, validated_data):
            center_id = validated_data['center_id']
            category_id = validated_data['category_id']
            keyword = validated_data['keyword']
            type = validated_data['type']
            status = validated_data['status']

            instance.center_id = center_id
            instance.category_id = category_id
            instance.keyword = keyword
            instance.type = type
            instance.status = status
            instance.save()
            return instance


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段

        def create(self, validated_data):
            center_id = validated_data['center_id']
            target = validated_data['target']
            type = validated_data['type']
            remark = validated_data['remark']
            status = validated_data['status']

            target = Target.objects.create(
                center_id=center_id,
                target=target,
                type=type,
                remark=remark,
                status=status
            )
            return target

        def update(self, instance, validated_data):
            center_id = validated_data['center_id']
            target = validated_data['target']
            type = validated_data['type']
            remark = validated_data['remark']
            status = validated_data['status']

            instance.center_id = center_id
            instance.target = target
            instance.type = type
            instance.remark = remark
            instance.status = status
            instance.save()
            return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段

        def create(self, validated_data):
            center_id = validated_data['center_id']
            category = validated_data['category']

            category = Category.objects.create(
                center_id=center_id,
                category=category
            )
            return category

        def update(self, instance, validated_data):
            center_id = validated_data['center_id']
            category = validated_data['category']

            instance.center_id = center_id
            instance.category = category
            instance.save()
            return instance


class ScrapedUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedUrls  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段


class KeywordArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordArticle  # 要序列化的模型
        fields = '__all__'  # 要序列化的字段

