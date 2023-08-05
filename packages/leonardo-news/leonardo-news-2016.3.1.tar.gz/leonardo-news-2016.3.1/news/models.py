
from django.utils.translation import ugettext_lazy as _


from .widget.news.models import NewsWidget  # noqa

from articles.models import Article

from leonardo.module import media, web
from leonardo.utils.widgets import load_widget_classes

Article.register_extensions('feincms.module.extensions.translations',
                            'feincms.module.extensions.datepublisher',
                            'articles.extensions.thumbnail',
                            )

REGIONS = ('main', 'preview',)

try:
    import taggit  # noqa
except:
    pass
else:
    Article.register_extensions(
        'articles.extensions.tags',
    )

Article.register_regions(
    ('preview', _('Preview area')),
    ('main', _('Main content area')),
)

Article.create_content_type(
    web.models.HtmlTextWidget, regions=REGIONS, optgroup=_('Text'))
Article.create_content_type(
    web.models.MarkupTextWidget, regions=REGIONS, optgroup=_('Text'))
Article.create_content_type(
    web.models.IconWidget, regions=REGIONS, optgroup=_('Text'))

for widget in load_widget_classes(media.default.widgets):
    Article.create_content_type(widget, regions=REGIONS, optgroup=_('Media'))

try:
    from leonardo_oembed.models import OembedWidget
    Article.create_content_type(OembedWidget,
                                regions=REGIONS, optgroup=_('External content'))
except:
    pass

try:
    from leonardo_geo.models import MapLocationWidget
    Article.create_content_type(MapLocationWidget,
                                regions=REGIONS, optgroup=_('Geolocation'))
except:
    pass
