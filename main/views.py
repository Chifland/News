from rest_framework.decorators import api_view  # [GET, POST, PUT, DELETE]
from rest_framework.response import Response  #Return Result
from main.serializers import NewsSerializer, NewsValidateSerializer
from main.models import News


@api_view(['GET', 'POST'])
def news_list_api_view(request):
    if request.method == 'GET':
        search = request.query_params.get('search', '')

        # 1. Get list of news
        news = News.objects.select_related('category')\
            .prefetch_related('tags', 'news_comments').filter(title__icontains=search)

        # 2. Convert list of news to list of dictionary
        data = NewsSerializer(instance=news, many=True).data

        # 3. Return Dictionary as JSON

        return Response(data=data)
    elif request.method == "POST":
        # Step 0: Validation
        serializer = NewsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)

        # Step 1: Request data from body
        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        amount = serializer.validated_data.get('amount')
        is_active = serializer.validated_data.get('is_active')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')


        # Step 2: Create news  by this
        news = News.objects.create(
            title=title, text=text,
            view_amount=amount, is_active=is_active,
            category_id=category_id
        )
        news.tags.set(tags)
        news.save()
        # Step 3: Return created news
        return Response(data=NewsSerializer(news).data)


@api_view(['GET','PUT', 'DELETE'])
def news_detail_api_view(request, news_id):
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response(data={'message': 'News object does ot exists!'},
                        status=404)
    if request.method == 'GET':
        data = NewsSerializer(instance=news, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = NewsValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        news.title = request.data.get('title')
        news.category_id = request.data.get('category_id')
        news.text = request.data.get('text')
        news.is_active = request.data.get('is_active')
        news.view_amount = request.data.get('amount')
        news.tags.set(request.data.get('tags'))
        news.save()
        return Response(data=NewsSerializer(news).data)
    else:
        news.delete()
        return Response(status=204)



@api_view(['GET'])
def test_api_view(request):
    dict_ = {
        'text': 'Hello World'
    }
    return Response(data=dict_)





