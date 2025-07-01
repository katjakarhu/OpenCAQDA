import re

HTML_TAG_REGEX = re.compile('<.*?>')


def remove_html_tags(raw_html):
    cleantext = re.sub(HTML_TAG_REGEX, '', raw_html)
    return cleantext
