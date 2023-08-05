from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def adsense_p(content, pnum, ad_template, start_default=False, end_default=False):
    # Render our adsense code placed in html file
    ad_code = render_to_string("adsense/%s.html"%ad_template)

    # Break down content into paragraphs
    paragraphs = content.split('</p>')

    # Check if paragraph we want to post after exists
    if pnum < len(paragraphs):
        # Append our code before the following paragraph
        paragraphs[pnum] = ad_code + paragraphs[pnum]
        # Assemble our text back with injected adsense code
        content = '</p>'.join(paragraphs)
    elif start_default:
        content = ad_code + '</p>'.join(paragraphs)
    elif end_default:
        content = '</p>'.join(paragraphs) + ad_code
    else:
        content = '</p>'.join(paragraphs)
    return content
