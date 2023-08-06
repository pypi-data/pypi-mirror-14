from django import template

from ..models import Document

register = template.Library()


@register.assignment_tag
def get_latest_documents(count=5, category=None):
    document_list = Document.objects.published()

    # Optional filter by category
    if category is not None:
        document_list = document_list.filter(category__slug=category)

    return document_list[:count]
