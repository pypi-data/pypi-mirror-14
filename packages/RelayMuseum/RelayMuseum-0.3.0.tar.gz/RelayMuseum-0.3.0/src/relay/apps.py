from django.apps import apps, AppConfig


class RelayConfig(AppConfig):
    name = 'relay'

    def ready(self):
        if apps.is_installed('actstream'):
            from actstream import registry
            registry.register(self.get_model('Torch'))
            registry.register(self.get_model('TorchFile'))
            registry.register(self.get_model('Relay'))
            registry.register(self.get_model('Ring'))
            registry.register(self.get_model('Participant'))
            registry.register(self.get_model('Language'))
