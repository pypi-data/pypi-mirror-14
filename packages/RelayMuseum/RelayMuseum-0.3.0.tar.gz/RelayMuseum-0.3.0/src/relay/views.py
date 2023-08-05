from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import render

from relay.models import *


def in_kwargs_or_get(request, kwargs, key, value):
    """If an url has the key-value-pair key=<value> in kwargs or
    the key <value> in GET, return the value, else return False."""
    assert value, '"value" cannot be empty/false'
    if kwargs.get(key, '') == value or value in request.GET:
        return True
    return False


def show_ring(request, *args, **kwargs):
    if in_kwargs_or_get(request, kwargs, u'action', 'smooth'):
        return torch_smooth_translation_list(request, *args, **kwargs)
    return torch_list(request, *args, **kwargs)


class RelayMixin(object):
    def get_context_data(self, **kwargs):
        kwargs['me'] = 'relay'
        return super(RelayMixin, self).get_context_data(**kwargs)


class TorchListView(RelayMixin, ListView):

    def get_queryset(self):
        self.relay = Relay.objects.get(slug=self.kwargs['relay'])
        self.ring = Ring.objects.get(relay=self.relay, slug=self.kwargs['ring'])
        queryset = Torch.objects.filter(ring=self.ring).order_by('pos')
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['ring'] = self.ring
        kwargs['relay'] = self.relay
        return super(TorchListView, self).get_context_data(**kwargs)
torch_list = TorchListView.as_view()


class RelayListView(RelayMixin, ListView):
    queryset = Relay.objects.order_by('pos')
relay_list = RelayListView.as_view()


class ParticipantMixin(object):
    queryset = Participant.objects.all()

    def get_context_data(self, **kwargs):
        kwargs['me'] = 'participant'
        return super(ParticipantMixin, self).get_context_data(**kwargs)


class ParticipantDetailView(ParticipantMixin, DetailView):
    pass
participant_detail = ParticipantDetailView.as_view()


class ParticipantListView(ParticipantMixin, ListView):

    def get_context_data(self, **kwargs):
        kwargs['relay_masters'] = self.queryset.filter(relay_mastering__isnull=False).distinct()
        kwargs['ring_masters'] = self.queryset.filter(ring_mastering__isnull=False).distinct()
        return super(ParticipantListView, self).get_context_data(**kwargs)
participant_list = ParticipantListView.as_view()


class TorchSmoothTranslationListView(TorchListView):
    template_name = 'relay/ring_smooth_translation.html'
torch_smooth_translation_list = TorchSmoothTranslationListView.as_view()


class RelayDetailView(RelayMixin, DetailView):

    def get_queryset(self):
        self.relay = Relay.objects.get(slug=self.kwargs['slug'])
        self.rings = Ring.objects.filter(relay=self.relay)
        queryset = Relay.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['rings'] = self.rings
        kwargs['relay'] = self.relay
        kwargs['num_rings'] = self.rings.count()
        return super(RelayDetailView, self).get_context_data(**kwargs)
relay_detail = RelayDetailView.as_view()


class TorchDetailView(RelayMixin, DetailView):
    def get_queryset(self):
        queryset = Torch.objects.filter(id=self.kwargs['pk'])
        self.relay = Relay.objects.get(slug=self.kwargs['relay'])
        self.ring = Ring.objects.get(relay=self.relay, torches=queryset)
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['ring'] = self.ring
        kwargs['relay'] = self.relay
        return super(TorchDetailView, self).get_context_data(**kwargs)
torch_detail = TorchDetailView.as_view()


class LanguageMixin(object):
    queryset = Language.objects.all()

    def get_context_data(self, **kwargs):
        kwargs['me'] = 'language'
        return super(LanguageMixin, self).get_context_data(**kwargs)


class LanguageDetailView(LanguageMixin, DetailView):
    pass
language_detail = LanguageDetailView.as_view()

class LanguageListView(LanguageMixin, ListView):
    pass
language_list = LanguageListView.as_view()

def show_statistics(request, *args, **kwargs):
    num_langs = Language.objects.count()
    num_participants = Participant.objects.count()
    num_relays = Relay.objects.count()
    num_rings = Ring.objects.count()
    num_torches = sum(relay.num_torches for relay in Relay.objects.filter(missing=False))

    avg_rings_per_relay = (num_rings - 1) / float(num_relays - Relay.objects.filter(missing=True).count())
    avg_torches_per_ring = float(num_torches) / num_rings - 1
    avg_torches_per_relay = float(num_torches) / num_relays
    avg_participants_per_language = num_participants / float(num_langs)
    if CalsLanguage:
        avg_calslanguages = Language.objects.filter(cals_language__isnull=False).count() / float(num_langs) * 100
    else:
        avg_calslanguages = None
    avg_calsparticipants = Participant.objects.filter(cals_user__isnull=False).count() / float(num_participants) * 100

    all_missing_torches = sum(relay.missing_torches for relay in Relay.objects.all())
    all_missing_relays = Relay.objects.filter(missing=True)

    langstats = {
        'num': num_langs,
        'avg_participants': avg_participants_per_language,
        'avg_calslang': avg_calslanguages,
    }
    participantstats = {
        'num': num_participants,
        'avg_calsuser': avg_calsparticipants,
    }
    relaystats = {
        'num': num_relays,
        'avg_rings': avg_rings_per_relay,
        'avg_torches': avg_torches_per_relay,
        'avg_torches_per_ring': avg_torches_per_ring,
    }
    missingstats = {
        'torches': all_missing_torches,
        'relays': all_missing_relays,
    }
    data = {
        'relay': relaystats,
        'lang': langstats,
        'participant': participantstats,
        'missing': missingstats,
        'me': 'statistics',
    }

    return render(request, 'relay/statistics.html', data)
