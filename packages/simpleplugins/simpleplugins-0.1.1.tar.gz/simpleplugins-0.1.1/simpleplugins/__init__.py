import fnmatch
import inspect
import os
from importlib.util import spec_from_file_location

import logging
import sys

__dirname, __init_python_script = os.path.split(os.path.abspath(__file__))

logger = logging.getLogger("SimplePlugins")

formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
console_log_handler = logging.StreamHandler(stream=sys.stdout)
console_log_handler.setFormatter(formatter)
console_log_handler.setLevel(logging.DEBUG)

logger.addHandler(console_log_handler)
logger.setLevel(logging.DEBUG)


def get_files_recursive(path, match='*.py'):
    """
    Perform a recursive search to find all the files matching the
    specified search criteria.
    :param path: Path to begin the recursive search.
    :param match: String/Regex used to match files with a pattern.
    :return: Full path of all the files found.
    :rtype: list
    """
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, match):
            matches.append(os.path.join(root, filename))

    return matches


def get_filename(file):
    """
    Safe method to retrieve only the name of the file.
    :param file: Path of the file to retrieve the name from.
    :return: None if the file is non-existant, otherwise the filename (extension included)
    :rtype: None, str
    """
    if not os.path.exists(file):
        return None
    return "%s%s" % os.path.splitext(file)


def import_module_from_file(full_path_to_module):
    """
    Import a module given the full path/filename of the .py file
    Python 3.4
    """
    if inspect.ismodule(full_path_to_module):
        return full_path_to_module

    module = None

    try:

        # Get module name and path from full path
        module_dir, module_file = os.path.split(full_path_to_module)
        module_name, module_ext = os.path.splitext(module_file)

        # Get module "spec" from filename
        spec = spec_from_file_location(module_name, full_path_to_module)

        module = spec.loader.load_module()

    except Exception as ec:
        # Simple error printing
        # Insert "sophisticated" stuff here
        print(ec)

    finally:
        return module


class PluginException(Exception):
    pass


class Plugin(object):
    """
    Base class that all plugins derive from.
    """

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', self.__class__.__name__)
        self.version = kwargs.pop('version', "1.0.0")
        self.description = kwargs.pop('description', "No Description Available")
        self.active = False

    def activate(self):
        """
        Operations to perform whenever the plugin is activated.
        :return:
        """
        raise NotImplementedError("Activation for %s is not implemented" % self.name)

    def deactivate(self):
        """
        Operations to perform whenever the plugin is deactivated.
        :return:
        """
        raise NotImplementedError("Deactivation for %s is not implemented" % self.name)

    def perform(self, **kwargs):
        """
        Operations that will be performed when invoked.
        This method is where the actual "use" logic of plugins will be defined.
        :param kwargs:
        :return:
        """
        raise NotImplementedError("Perform for %s is not implemented" % self.name)


class PluginManager(object):
    """
    Holds instances, and information for each plugin.
    Provides functionality to interact, activate, deactivate, perform, and operate with or on plugins.
    """

    def __init__(self):
        self.plugins = {}

    def register(self, plugin=None, plugin_file=None, directory=None, skip_types=None, override=False, activate=True):
        """
        Register a plugin, or plugins to be managed and recognized by the plugin manager.
        Will take a plugin instance, file where a plugin / plugin(s) reside, parent directory
        that holds plugin(s), or sub-folders with plugin(s).

        Will optionally "activate" the plugins, and perform any operations defined in their "activate" method.

        :param plugin: Plugin Instance to register.
        :param plugin_file: str: File (full path) to scan for Plugins.
        :param directory: str: Directory to perform a recursive scan on for Plugins.
        :param skip_types: list: Types of plugins to skip when found, during a scan / search.
        :param override: bool: Whether or not to override registered plugin when it's being registered again.
        :param activate: bool: Whether or not to activate the plugins upon registration.
        :return: Does not Return.
        """
        # Double verify that there's types to skip. We don't want to register "Base" types (Plugin)

        if not isinstance(skip_types, list):
            skip_types = [skip_types]
            logger.debug("Skip Types must be a list. Created list with values passed.")

        if skip_types is None:
            skip_types = [Plugin]
        else:
            skip_types.append(Plugin)

        # Check if they've passed a method of registration!
        if plugin is None and plugin_file is None and directory is None:
            raise PluginException("Unable to perform registration without a plugin, module, or directory.")

        # First we'll check if they're registering via directory (Scanning)
        # as it might be best for bigger applications / apps with many plugins to register them via
        # a folder, where plugins are expected!
        if directory is not None:
            plugins_in_dir = PluginManager.scan_for_plugins(directory)
            # Loop through all the plugins in the directory, associated by file -> list[] (or none)
            for file, plugins in plugins_in_dir.items():
                # If there's no plugins in that file then just continue.
                if plugins is None:
                    continue

                for plugin in plugins:
                    # If there's a duplicate plugin and we're not overriding, then we'll skip it.
                    if plugin.name in self.plugins:
                        if not override:
                            logger.warn("Failed to register %s: Duplicate plugin found!" % plugin.name)
                            continue

                    # Now verify if we're supposed to skip the type of the plugin that's being attempted to register.
                    # Useful when plugins classes extend a base-class (Plugin, for example)
                    # but you don't want to register the base class.
                    if type(plugin) in skip_types:
                        logger.warn(
                            "Skipping registration of %s, as it's not to be registered." % plugin.__class__.__name__)
                        continue

                    # Assign the plugin (via name) to the dictionary of registered plugins
                    self.plugins[plugin.name] = plugin
                    # Give a little output of the plugin!
                    logger.debug("Registered plugin %s from %s in %s" % (plugin.name, file, directory))

                    # Then if we're going to activate the plugin, do so!
                    if activate:
                        self.plugins[plugin.name].activate()

        # Now we're going to check if they're registering the plugins
        # either by file, or module
        if plugin_file is not None:
            # If the plugin_file is not a module, then we're going to verify the file actually exists!
            if not inspect.ismodule(plugin_file):
                # Verify if there's a ~ (Home dir call) inside the path, and if so then expand it.
                plugin_file = os.path.expanduser(plugin_file)
                # Then verify if the path of the plugin exists, raising an exception if not!
                if not os.path.exists(plugin_file):
                    raise FileNotFoundError("Unable to locate file %s" % plugin_file)

            # Next after verifying, we get all the plugins inside the file or module.`
            plugins_in_file = PluginManager.get_plugins_in_module(plugin_file)
            # If there's no plugins inside, then we're going to throw an exception. There's nothing to register in here.
            if plugins_in_file is None or len(plugins_in_file) == 0:
                raise PluginException("Unable to locate plugins inside %s" % plugin_file)

            # Loop through every plugin inside the file/module and attempt to register it.
            for fplugin in plugins_in_file:
                # If there's a duplicate plugin and we're not overriding, then we'll skip it.
                if fplugin.name in self.plugins:
                    if not override:
                        logger.warn("Failed to register %s: Duplicate plugin found!" % fplugin.name)
                        continue

                # Now verify if we're supposed to skip the type of the plugin that's being attempted to register.
                # Useful when plugins classes extend a base-class (Plugin, for example)
                # but you don't want to register the base class.
                if type(fplugin) in skip_types:
                    logger.warn(
                        "Skipping registration of %s, as it's not to be registered." % fplugin.__class__.__name__)
                    continue

                # Assign the plugin (via name) to the dictionary of registered plugins
                self.plugins[fplugin.name] = fplugin
                # Give a little output of the plugin!
                logger.debug("Registered plugin %s from %s %s" % (
                    fplugin.name, "module" if inspect.ismodule(plugin_file) else "file",
                    get_filename(plugin_file) if not inspect.ismodule(plugin_file) else plugin_file.__name__)
                             )

                # Then if we're going to activate the plugin, do so!
                if activate:
                    self.plugins[fplugin.name].activate()

        # Now we're checking if they actually passed a plugin instance to register.
        if plugin is not None:
            # If it's already in the plugins and we're not overriding, then we'll skip it.
            if plugin.name in self.plugins:
                if override is False:
                    return

            # Otherwise register the plugin, and (potentially) activate it!
            self.plugins[plugin.name] = plugin
            logger.debug("Registered plugin %s" % plugin.name)
            if activate:
                self.plugins[plugin.name].activate()

    def activate(self, plugins=[]):
        # If there's no plugins passed as a list, then we'll just assume
        # That all the plugins are to be registered.
        if len(plugins) == 0:
            if not self.has_plugin():
                raise PluginException("Unable to perform activation as no plugins have been registered")

            for plugin in self.get_plugins():
                if not plugin.active:
                    plugin.activate()

            return

        # Otherwise, we're going to loop through all the values in the list.
        for plugin in plugins:
            # Check if the value they've passed is a string (plugin name, presumably)
            if isinstance(plugin, str):
                if plugin not in self.plugins:
                    continue

                pl = self.plugins[plugin]
                # We don't want to activate plugins that are already active.
                if pl.active:
                    continue

                pl.activate()
            elif isinstance(plugin, Plugin):
                if plugin.active:
                    continue

                if plugin.name not in self.plugins:
                    continue
                plugin.activate()

    def unregister(self, plugin=None, plugin_file=None):
        """
        Unregister all plugins, or a specific plugin, via an instance, or file (path) containing plugin(s).
        When this method is called without any arguments then all plugins will be deactivated.
        :param plugin: Plugin to unregister.
        :param plugin_file: File containing plugin(s) to unregister.
        :return: Does not Return.
        """
        if plugin is None and plugin_file is None:
            for name, plugin in self.plugins.items():
                plugin.deactivate()
                del self.plugins[name]

            return

        if plugin is not None:
            if plugin.name in self.plugins:
                plugin.deactivate()
                del self.plugins[plugin.name]

        if plugin_file is not None:
            plugs_in_file = PluginManager.get_plugins_in_module(plugin_file)
            if plugs_in_file is None:
                return

            for classPlugin in plugs_in_file:
                if not self.has_plugin(classPlugin.name, classPlugin):
                    continue

                self.get_plugin(classPlugin.name).deactivate()
                del self.plugins[classPlugin.name]

    def get_plugins(self, plugin_type=None):
        """
        Retrieve a list of plugins in the PluginManager.
        All plugins if no arguments are provides, or of the specified type.
        :param plugin_type: list: Types of plugins to retrieve from the plugin manager.
        :return: Plugins being managed by the Manager (optionally of the desired plugin_type).
        :rtype: list
        """
        if plugin_type is None:
            return self.plugins.values()

        plugin_list = []
        for name, plugin in self.plugins.items():
            if isinstance(plugin, plugin_type if inspect.isclass(plugin_type) else type(plugin_type)):
                plugin_list.append(plugin)

        return plugin_list

    def get_plugin(self, name):
        """
        Retrieve a registered plugin by its name.
        :param name: Name of the plugin to retrieve.
        :return: None if the manager has no plugin of the given name, otherwise the plugin instance matching the given name.
        :rtype: None / Plugin
        """
        if not self.has_plugin(name):
            return None

        return self.plugins[name]

    def has_plugin(self, name=None, plugin_type=None):
        """
        Check if the manager has a plugin / plugin(s), either by its name, type, or simply checking if the
        manager has any plugins registered in it.

        Utilizing the name argument will check if a plugin with that name exists in the manager.
        Using both the name and plugin_type arguments will check if a plugin with that name, and type, exists.

        Using only the plugin_type argument will check if any plugins matching the type specified are registered
        in the plugin manager.
        :param name: Name of the plugin to check for.
        :param plugin_type: Plugin Type to check for.
        :return:
        """
        # If there's no arguments passed to this, then we check if there's simply any plugins
        # Registered in the plugin manager.
        if name is None and plugin_type is None:
            return len(self.plugins) > 0

        # If there's a name and plugin type, we just want to verify the manager
        # Has a plugin with that name, and that plugin is of the given type!
        if name is not None and plugin_type is not None:
            return name in self.plugins and isinstance(self.plugins[name],
                                                       plugin_type if inspect.isclass(plugin_type) else type(
                                                           plugin_type))

        # If only the type is given, then just assure we have atleast one plugin with the
        # desired type registered in the manager
        if plugin_type is not None:
            return len(
                self.get_plugins(plugin_type=plugin_type if inspect.isclass(plugin_type) else type(plugin_type))) > 0

        # Lastly, however, we're doing a simple name check; Assuring the manager
        # has a plugin registered with the given name!
        return name in self.plugins

    @staticmethod
    def scan_for_plugins(directory):
        """
        Scan a directory for modules that contains plugin(s).
        :param directory: Path of the folder/directory to scan.
        :return: Dictionary of file (key) and plugins (value), where the key is the path of the module and value is a list of plugins inside that module.
        :rtype: dict
        """
        if not os.path.exists(os.path.expanduser(directory)):
            raise FileNotFoundError("Unable to locate directory %s" % directory)

        files_in_dir = get_files_recursive(directory)
        plugins = {}
        for file in files_in_dir:
            plugins_in_module = PluginManager.get_plugins_in_module(file, supress=True)

            if plugins_in_module is None:
                continue

            plugins[file] = plugins_in_module

        return plugins

    @staticmethod
    def get_plugins_in_module(module_path, suppress=False):
        """
        Inspect a module, via its path, and retrieve a list of the plugins inside the module.
        :param module_path: Path of the module to inspect.
        :param suppress: Whether or not to suppresss exceptions.
        :raises: PluginException
        :return: A list of all the plugins inside the specified module.
        :rtype: list
        """
        module = module_path if inspect.ismodule(module_path) else import_module_from_file(module_path)
        if module is None:
            # CHeck if we're repressing errors.. Sometimes, such in the case of scanning a dir,
            # This is BOUND to return none.
            if suppress is False:
                raise PluginException("Unable to find plugins inside module at %s" % module)
            return None

        plugin_list = []
        for name, obj in inspect.getmembers(module):
            attr = getattr(module, name)
            if isinstance(attr, Plugin):
                plugin_list.append(attr)

        return plugin_list
