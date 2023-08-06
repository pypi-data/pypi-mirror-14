from django.conf import settings
from django.db import models
from facebook_api.utils import get_improperly_configured_field


class PhotableModelMixin(models.Model):

    class Meta:
        abstract = True

    if 'facebook_photos' in settings.INSTALLED_APPS:
        from facebook_photos.models import Album
        albums = get_improperly_configured_field('facebook_photos', True)
        # becouse of this line command
        # ./manage.py sqlflush | grep facebook_photos
        # outputs wrong column
        # SELECT setval(pg_get_serial_sequence('"facebook_photos_album"','id'), 1, false);
#         albums = generic.GenericRelation(
#             Album, content_type_field='owner_content_type', object_id_field='owner_id', verbose_name=u'Albums')

        def fetch_albums(self, *args, **kwargs):
            return Album.remote.fetch_page(page=self, *args, **kwargs)
    else:
        albums = get_improperly_configured_field('facebook_photos', True)
        fetch_albums = get_improperly_configured_field('facebook_photos')
