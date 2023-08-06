# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from glitter.mixins import GlitterDetailMixin

from .mixins import DocumentMixin
from .models import Category, Document


class DocumentListView(DocumentMixin, ListView):
    paginate_by = 10
    queryset = Document.objects.published()


class DocumentDetailView(DocumentMixin, GlitterDetailMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['current_category'] = self.object.category
        return context


class CategoryDocumentListView(DocumentMixin, ListView):
    template_name_suffix = '_category_list'
    paginate_by = 10
    queryset = Document.objects.published()

    def get_queryset(self):
        qs = super(CategoryDocumentListView, self).get_queryset()
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return qs.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(CategoryDocumentListView, self).get_context_data(**kwargs)
        context['current_category'] = self.category
        return context
