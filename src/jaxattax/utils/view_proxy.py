import functools
import importlib


class ViewModuleProxy:
    def __init__(self, import_path):
        self.import_path = import_path

    @functools.cached_property
    def module(self):
        return importlib.import_module(self.import_path)

    def get_view_func(self, name):
        return getattr(self.module, name)

    def __getitem__(self, name):
        return ViewMethodProxy(self, name)


class ViewMethodProxy:
    def __init__(self, view_module_proxy, view_name):
        self.view_module_proxy = view_module_proxy
        self.view_name = view_name

    def __call__(self, page, request, *args, **kwargs):
        view = self.view_module_proxy.get_view_func(self.view_name)
        return view(request, page, *args, **kwargs)

    def __get__(self, instance, cls):
        return functools.partial(self.__call__, instance)
