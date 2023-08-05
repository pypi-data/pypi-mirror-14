from django import template
from virtenviro.news.models import Post
from django.template import loader, Context
from django.conf import settings

register = template.Library()


class LastNewsNode(template.Node):
    def __init__(self, count):
        self.news = Post.objects.last_news()[0:count]

    def render(self, context):
        context['last_news'] = self.news
        return ''

@register.tag
def last_news(parser, token):
    contents = token.split_contents()
    if contents[1]:
        try:
            count = int(contents[0])
        except TypeError:
            try:
                count = settings.LAST_NEWS_COUNT
            except:
                count = 10
    return LastNewsNode(count=count)