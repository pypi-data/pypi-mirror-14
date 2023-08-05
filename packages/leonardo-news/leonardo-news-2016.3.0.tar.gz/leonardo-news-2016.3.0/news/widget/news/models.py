
from django.db import models
from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import ListWidget

from articles.models import Article


class NewsWidget(ListWidget):

    number = models.IntegerField()
    show_archive_button = models.BooleanField(
        default=True, verbose_name=_("show archive button"))

    def get_items(self):
        return Article.objects.all()[0:self.number]

    class Meta:
        abstract = True
        verbose_name = _("last news")
        verbose_name_plural = _("last news")
