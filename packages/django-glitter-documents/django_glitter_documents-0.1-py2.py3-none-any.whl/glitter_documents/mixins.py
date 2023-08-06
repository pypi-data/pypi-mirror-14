# -*- coding: utf-8 -*-

from .models import Document, Category


class DocumentMixin(object):
    model = Document

    def get_context_data(self, **kwargs):
        context = super(DocumentMixin, self).get_context_data(**kwargs)
        context['documents_categories'] = True
        context['categories'] = Category.objects.all()
        return context
