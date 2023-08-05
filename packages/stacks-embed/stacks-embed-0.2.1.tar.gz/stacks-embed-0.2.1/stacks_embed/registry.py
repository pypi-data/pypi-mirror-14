import copy

from django.conf import settings


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class AlreadyRegisteredDomain(Exception):
    pass


class StacksEmbedServiceRegistry(object):
    """
    A StacksEmbedServiceRegistry object allows Embed Services to be
    registered on an app-by-app basis.
    """

    def __init__(self):
        self._registry = {}
        self._allowed_domains = {}

    def add_embed_service(self, short_name, verbose_name,
                          allowed_domains, process_instance_func):
        """
        Registers an embed service.
        * short_name: What will be stored in the database for
                      StacksEmbed.service
        * verbose_name: The human-readable name of the service (what will be
                        shown to users for StacksEmbed.service)
        * process_instance_func: A function that accepts an instance of
                                 StacksEmbed and does any necessary pre_save
                                 processing to properly build an embed code
                                 and assign it to StacksEmbed.embed_code
        """
        if short_name in self._registry:
            raise AlreadyRegistered(
                'A service with the short_name {} is already registered with '
                'the Stacks Embed Service Registry.'.format(short_name)
            )
        else:
            for domain in allowed_domains:
                if domain not in self._allowed_domains:
                    self._allowed_domains[domain] = short_name
                else:
                    raise AlreadyRegisteredDomain(
                        "'{}' has been already registered with "
                        "the '{}' service.".format(
                            domain,
                            self._registry[self._allowed_domains[domain]][0]
                        )
                    )
            self._registry[short_name] = (
                verbose_name, process_instance_func
            )

    def remove_embed_service(self, short_name):
        """
        Unregisters an embed service.

        If an embed service isn't already registered to `short_name`
        NotRegistered will raise.
        """
        if short_name not in self._registry:
            raise NotRegistered(
                'No Embed Service is registered to {}' % short_name
            )
        else:
            del self._registry[short_name]

stacks_embed_service_registry = StacksEmbedServiceRegistry()


def find_stacks_embed_services():
    """
    Auto-discover INSTALLED_APPS stacks_embed_service.py modules and fail
    silently when not present. This forces an import on them (thereby
    registering them)

    This is a near 1-to-1 copy of how django's admin application registers
    models.
    """
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's sizedimage module.
        try:
            before_import_registry = copy.copy(
                stacks_embed_service_registry._registry
            )
            import_module('{}.stacks_embed_service'.format(app))
        except:
            # Reset the stacks_embed_service_registry to the state before the
            # last import as this import will have to reoccur on the next
            # request and this could raise NotRegistered and AlreadyRegistered
            # exceptions (see django ticket #8245).
            stacks_embed_service_registry.\
                _modelstacks_embed_service_registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have a stuff module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'stacks_embed_service'):
                raise


find_stacks_embed_services()
