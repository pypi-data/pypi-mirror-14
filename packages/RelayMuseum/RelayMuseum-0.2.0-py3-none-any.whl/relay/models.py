import mimetypes

from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User as CalsUser
from django.utils.safestring import mark_for_escaping as _escape
from django.utils.html import escape

try:
    from cals.models import Language as CalsLanguage
except ImportError:
    CalsLanguage = None

from interlinears import make_html_interlinear

__all__ = ('Participant', 'Language', 'Ring', 'Torch', 'Relay', 'TorchFile', 'CalsLanguage')


def re_slugify(queryset):
    for object in queryset.objects.all():
        object.slug = good_slugify(object.name)
        object.save(force_update=True)


def clone_ringtorch(relay, torch):
    pass
    #rings = relay.


class UniqueSlugModel(models.Model):
    slug = models.SlugField(blank=True, null=True, editable=False, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = self.good_slugify()
        super(UniqueSlugModel, self).save(*args, **kwargs)

    def good_slugify(self):
        slug = slugify(self.name)
        try:
            o = self.__class__.objects.get(slug=slug)
            if self.id is not None:
                if self.id == o.id:
                    return slug
                return slug + '-%i' % self.id
        except ObjectDoesNotExist:
            pass
            #slug = slug + '-%i' % self.id
        return slug


class Participant(UniqueSlugModel):
    cals_user = models.ForeignKey(CalsUser, null=True, blank=True, related_name='relays')
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name and self.cals_user:
            # get name from CALS
            name = self.cals_user.username
            profile = getattr(self.cals_user, 'profile', None)
            if profile:
                name = profile.display_name
            self.name = name
        super(Participant, self).save(*args, **kwargs)

    def relays(self):
        return Relay.objects.filter(id__in=[torch.relay.id for torch in self.torches.all()])

    def languages(self):
        return Language.objects.filter(id__in=[torch.language.id for torch in self.torches.all()])

    def rings(self):
        rings = self.ring_mastering.all()
        relays = {}
        for ring in rings:
            relays.setdefault(ring.relay.name, [])
            relays[ring.relay.name].append(ring)
        out = []
        for relayname, rings in relays.items():
            relay = Relay.objects.get(name=relayname) 
            if relay.rings.count() == len(rings):
                out.append(relay)
            else:
                out.append(ring)
        return out


class Language(UniqueSlugModel):
    if CalsLanguage:
        cals_language = models.ForeignKey(CalsLanguage, null=True, blank=True, related_name='relays')
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)

    class Meta:
        ordering = ['name']
        if CalsLanguage:
            unique_together = ('cals_language', 'name', 'slug')
        else:
            unique_together = ('name', 'slug')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name and self.cals_language:
            self.name = self.cals_language.name
        super(Language, self).save(*args, **kwargs)

    def relays(self):
        return Relay.objects.filter(id__in=[torch.relay.id for torch in self.torches.all()])

    def participants(self):
        return Participant.objects.filter(id__in=[torch.participant.id for torch in self.torches.all()])


class Relay(UniqueSlugModel):
    RELAY_SUBTYPES = (
            ('standard', 'Standard'),
            ('inverse', 'Inverse'),
            )
    name = models.CharField(max_length=40)
    relay_master = models.ForeignKey(Participant, related_name='relay_mastering')
    subtype = models.CharField(max_length=20, 
            choices=RELAY_SUBTYPES,
            default='standard')
    homepage = models.URLField(blank=True, null=True)
    rules = models.TextField('Rules specific to this relay', blank=True, null=True)
    notes = models.TextField('Additional notes', blank=True, null=True)
    pos = models.IntegerField('position', default=0, unique=True)
    missing = models.BooleanField(default=True)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['pos']

    def __str__(self):
        return self.name

    @property
    def num_torches(self):
        return sum(ring.num_torches for ring in self.rings.all())

    @property
    def missing_torches(self):
        return self.num_torches - self.torches.count()

    @property
    def next(self):
        try:
            return Relay.objects.filter(pos__gt=self.pos).order_by('pos')[0]
        except IndexError:
            return None

    @property
    def prev(self):
        try:
            return Relay.objects.filter(pos__lt=self.pos).order_by('-pos')[0]
        except IndexError:
            return None


class Ring(models.Model):
    RING_SUBTYPES = (
            ('standard', 'Standard'),
            ('romance', 'Romance'),
            )
    relay = models.ForeignKey(Relay, related_name='rings')
    ring_master = models.ForeignKey(Participant, blank=True, null=True, related_name='ring_mastering')
    name = models.CharField(max_length=10, default='_')
    slug = models.SlugField(blank=True, null=True, editable=False, default='_')
    subtype = models.CharField(max_length=20, 
        choices=RING_SUBTYPES,
        default='standard')
    end = models.DateTimeField(blank=True, null=True)
    num_torches = models.PositiveIntegerField('Number of torches', default=0)

    class Meta:
        #ordering = ['id', 'name']
        unique_together = ('relay', 'name')
        order_with_respect_to = 'relay'

    def __str__(self):
        if self.name != u'_':
            return u'%s, ring %s' % (self.relay.name, self.name)
        else:
            return u'%s' % self.relay.name

    def save(self, *args, **kwargs):
        if not self.ring_master:
            self.ring_master = self.relay.relay_master
        if self.name != '_':
            slug = slugify(self.name)
        super(Ring, self).save(*args, **kwargs)

    @property
    def missing_torches(self):
        return self.num_torches - self.torches.count()


class Torch(models.Model):
    INTERLINEAR_FORMATS = (
        ('monospace', 'WYSIWYG monospace'),
        ('leipzig', 'Leipzig Glossing Rules'),
    )

    relay = models.ForeignKey(Relay, related_name='torches')
    ring = models.ForeignKey(Ring, blank=True, null=True, related_name='torches')
    participant = models.ForeignKey(Participant, related_name='torches')
    language = models.ForeignKey(Language, related_name='torches')
    first = models.BooleanField(default=False)
    last = models.BooleanField(default=False)
    pos = models.IntegerField('position', default=0)
#     torch_title = models.CharField(max_length=128,
#             blank=True,null=True,
#             help_text='Title, if any, of the torch')
    torch = models.TextField(
            help_text='The text that was sent to the next participant')
#     smooth_translation_title = models.CharField(max_length=128,
#             blank=True,null=True,
#             help_text='Title, if any, of the smooth translation')
    smooth_translation = models.TextField(
            blank=True, null=True,
            help_text='Smooth English translation of the torch sent')
#     translation_of_received_title = models.CharField(max_length=128,
#             blank=True,null=True,
#             help_text='Title, if any, of the translation of the received text')
    translation_of_received = models.TextField(
            blank=True, null=True,
            help_text='Translation of the torch received')
    mini_dictionary = models.TextField(
            blank=True, null=True,
            help_text='Mini dictionary covering the expressions, words and affixes in the torch')
    mini_grammar = models.TextField(
            blank=True, null=True,
            help_text='Mini grammar covering the phenomena in the torch')
    abbreviations = models.TextField(
            blank=True, null=True,
            help_text='Abbreviations')
    interlinear = models.TextField('Interlinear', blank=True, null=True, default='', db_column='il_text')
    il_xhtml = models.TextField('Interlinear, formatted', blank=True, null=True, default='', db_column='il_xhtml', editable=False)
    il_format = models.CharField('Interlinear format', max_length=20, choices=INTERLINEAR_FORMATS, blank=True, default='monospace')

    class Meta:
        verbose_name_plural = 'torches'
        unique_together = ('relay', 'ring', 'pos')
        #ordering = ('ring', 'pos',)
        order_with_respect_to = 'ring'

    def __str__(self):
        return u'%s by %s' % (self.language.name, self.participant.name)

    def save(self, *args, **kwargs):
        if self.interlinear.strip():
            self.il_xhtml = make_html_interlinear(escape(self.interlinear), format=self.il_format)
        # Denormalization
        if not self.relay and self.ring:
            self.relay = self.ring.relay
        if not self.ring and self.relay:
            rings = self.relay.rings.all()
            num_rings = rings.count()
            if num_rings in (0, 1):
                # Probably a one-ring relay...
                self.ring, created = Ring.objects.get_or_create(relay=self.relay)
            else:
                # Just pick one
                self.ring = self.relay.rings.all()[0]
        super(Torch, self).save(*args, **kwargs)

    @property
    def next(self):
        try:
            return Torch.objects.exclude(pos=0).filter(ring=self.ring, relay=self.relay, pos__gt=self.pos).order_by('pos')[0]
        except IndexError:
            return None

    @property
    def prev(self):
        try:
            return Torch.objects.exclude(pos=0).filter(ring=self.ring, relay=self.relay, pos__lt=self.pos).order_by('-pos')[0]
        except IndexError:
            return None

    def get_interlinear(self):
        return make_html_interlinear(self.interlinear, self.il_format, _escape)

    def simple_name(self):
        return self.__str__()


class TorchFile(models.Model):
    CATEGORIES = (
            ('alttorch', 'Alternate version'),
            ('recording', 'Recording'),
            ('orthopgraphy', 'Native orthopgraphy'),
            ('print', 'Printable version'),
            ('pronunciation-ascii', 'Pronunciation (ASCII)'),
            ('pronunciation-ipa', 'Pronunciation (IPA)'),
    )

    def upload_to(self, filename):
        return 'files/torches/%i/%s' % (self.torch.id, filename)

    torch = models.ForeignKey(Torch, related_name='files')
    filename = models.FileField(upload_to=upload_to)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    mimetype = models.CharField(max_length=256, default='application/octet-stream', blank=True)

    def __str__(self):
        return u'%s, %s, %s %i' % (self.category_name, self.torch, self.torch.ring, self.torch.pos)

    def save(self, *args, **kwargs):
        filename = self.filename.name
        mimetype, encoding = mimetypes.guess_type(filename)
        if mimetype:
            self.mimetype = mimetype
        super(TorchFile, self).save(*args, **kwargs)

    @property
    def category_name(self):
        return dict(self.CATEGORIES)[self.category]
