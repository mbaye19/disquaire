from django.contrib import admin

from .models import Booking, Contact, Artist, Album
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


class AdminURLMixin(object):

    def get_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        return reverse("admin:store_%s_change" % (
            content_type.model),
            args=(obj.id,))


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminURLMixin):
    readonly_fields = ["contact_link", "album_link", "created_at"]
    fields = ["album_link", "created_at", "contacted"]
    list_filter = ['created_at', 'contacted']

    def has_add_permission(self, request):
        return False

    def contact_link(self, booking):
        url = self.get_admin_url(booking.contact)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.contact.name))

    def album_link(self, booking):
        url = self.get_admin_url(booking.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))
    
    album_link.short_description = "Album"


class BookingInline(admin.TabularInline, AdminURLMixin):
    readonly_fields = ["album_link", "created_at", "contacted"]

    def album_link(self, booking):
        url = self.get_admin_url(booking.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))

    album_link.short_description = "Album"
    model = Booking
    fieldsets = [
        (None, {'fields': ['album_link', 'contacted']})
    ]  # list columns
    extra = 0
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInline, ]  # list of bookings made by a contact


class AlbumArtistInline(admin.TabularInline):
    # the query goes through an intermediate table.
    model = Album.artists.through
    extra = 1
    verbose_name = "Disque"
    verbose_name_plural= "Disques"


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInline, ]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title']
