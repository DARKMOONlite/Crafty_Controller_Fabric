def BuildModuleUrls(module_url_defs: list, logger):
    """Build a handler list for every module passed.

    Expected input format is a list of module names such as,

    ```
    module_url_lists = [
        'module_name',
    ]
    ```

    An API path is then constructed according to, global_api_module_prefix/module_name/
    It is expected that each module defines a url submodule with a "handlers" mapping structure.
    """
    
    # TODO: Make this a config in settings!!
    global_api_module_prefix = "app.api"
    url_list_name = "handlers"
    built_handlers = []

    for module_url_def in module_url_defs:
        module_name = module_url_def
        prefix = fr"/{module_name}"

        url_module = importer(f"{global_api_module_prefix}.{module_name}.urls", from_packages=url_list_name)
        url_list = url_module.__dict__[url_list_name] if url_module else []

        for handler_def in url_list:
            built_handler = (prefix + handler_def[0], handler_def[1])
            
            if built_handler:
                built_handlers.append(built_handler)

        if url_module:
            del(url_module) 

    logger.info(f"{len(built_handlers)} URL Handlers were Associated for {len(module_url_defs)} modules.")
    return built_handlers


def importer(name, root_package=False, relative_globals=None, from_packages=[], level=0,):
    module = None

    try:
        module = __import__(name, locals=None,
                            globals=relative_globals, 
                            fromlist=[] if root_package else from_packages,
                            level=level)
    except ModuleNotFoundError as e:
        raise HandlerBuilderImporterError(e, name)
    finally:
        return module

class HandlerBuilderImporterError(Exception):
    '''Raise when importing modules for the handler builder throws underlying errors.'''

    def __init__(self, original_error, module_name):
        self.original_error = original_error
        self.module_name = module_name
        super().__init__(self.module_name)

    def __str__(self):
        return f"Attempted import of module: {self.module_name} was unable to determine a module with the given name. Original error thrown was {self.original_error}"