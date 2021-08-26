from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView

from articleapp.models import Article
from likeapp.models import LikeRecord


@transaction.atomic
def db_transaction(user, article):
    article.like += 1
    article.save()

    like_record = LikeRecord.objects.filter(user=user,
                                            article=article)
    if like_record.exists():
        raise ValidationError('like already exists.')
    else:
        LikeRecord(user=user, article=article).save()


@method_decorator(login_required, 'get')
class LikeArticleView(RedirectView):
    def get(self, request, *args, **kwargs):
        user = request.user
        article = Article.objects.get(pk=kwargs['article_pk'])

        try:
            db_transaction(user, article)
            # 좋아요 반영 O
            messages.add_message(request, messages.SUCCESS, '이 게시물을 좋아합니다.')
        except ValidationError:
            # 좋아요 반영 X
            messages.add_message(request, messages.ERROR, '이미 좋아한 게시물입니다.')
            return HttpResponseRedirect(reverse('articleapp:detail',
                                                kwargs={'pk': kwargs['article_pk']}))
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('articleapp:detail', kwargs={'pk': kwargs['article_pk']})