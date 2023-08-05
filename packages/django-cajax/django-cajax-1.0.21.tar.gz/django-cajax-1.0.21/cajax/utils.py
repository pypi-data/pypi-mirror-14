from django.utils.html import strip_spaces_between_tags

def get_secure_html(html):
    return strip_spaces_between_tags(html).replace('\r', '').replace('\n', '').replace('\'', '\\\'')
