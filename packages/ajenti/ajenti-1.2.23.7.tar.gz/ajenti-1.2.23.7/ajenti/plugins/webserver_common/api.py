import logging
import os

from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.ui.binder import Binder


class AvailabilitySymlinks(object):
    """
    Manage directories of following style::

        --sites.available
         |-a.site
         --b.site
        --sites.enabled
         --a.site -> ../sites.available/a.site
    """

    def __init__(self, dir_a, dir_e, supports_activation, ignore_ext=[]):
        self.dir_a, self.dir_e, self.ignore_ext = dir_a, dir_e, ignore_ext
        self.supports_activation = supports_activation

    def list_available(self):
        return [x for x in sorted(os.listdir(self.dir_a)) if
                not os.path.isdir(os.path.join(self.dir_a, x))
                and not os.path.splitext(os.path.join(self.dir_a, x))[-1] in self.ignore_ext]

    def is_enabled(self, entry):
        if not self.supports_activation:
            return True
        return self.find_link(entry) is not None

    def get_path(self, entry):
        return os.path.abspath(os.path.join(self.dir_a, entry))

    def find_link(self, entry):
        path = self.get_path(entry)

        for e in os.listdir(self.dir_e):
            if os.path.abspath(os.path.realpath(os.path.join(self.dir_e, e))) == path:
                return e

    def enable(self, entry):
        if not self.supports_activation:
            return
        e = self.find_link(entry)
        if not e:
            link_path = os.path.join(self.dir_e, entry)
            if not os.path.exists(link_path):
                os.symlink(self.get_path(entry), link_path)

    def disable(self, entry):
        if not self.supports_activation:
            return
        e = self.find_link(entry)
        if e:
            os.unlink(os.path.join(self.dir_e, e))

    def rename(self, old, new):
        on = self.is_enabled(old)
        self.disable(old)
        os.rename(self.get_path(old), self.get_path(new))
        if on:
            self.enable(new)

    def delete(self, entry):
        self.disable(entry)
        os.unlink(self.get_path(entry))

    def open(self, entry, mode='r'):
        return open(os.path.join(self.dir_a, entry), mode)

    def exists(self):
        return os.path.exists(self.dir_a) and os.path.exists(self.dir_e)


class WebserverConf(object):
    def __init__(self, owner, dir, entry):
        self.name = entry
        self.owner = owner
        self.dir = dir
        self.active = dir.is_enabled(entry)
        self.config = dir.open(entry).read()

    def save(self):
        self.dir.open(self.name, 'w').write(self.config)
        if self.active:
            self.dir.enable(self.name)
        else:
            self.dir.disable(self.name)


class WebserverMainConf(object):
    def __init__(self, filename):
        self.name = os.path.basename(filename)
        self.configfile = filename
        self.config = ''

    def save(self):
        try:
            open(self.configfile, 'w').write(self.config)
        except IOError as e:
            logging.error(e.message)
        return self

    def update(self):
        try:
            self.config = ''.join(open(self.configfile).readlines())
        except IOError as e:
            logging.error(e.message)
        return self


class WebserverPlugin(SectionPlugin):
    service_name = ''
    service_buttons = []
    hosts_available_dir = ''
    hosts_enabled_dir = ''
    hosts_dir = None
    template = ''
    supports_host_activation = True
    configurable = False
    main_conf_files = []
    configurations = []

    def log(self, msg):
        logging.info('[%s] %s' % (self.service_name, msg))

    def init(self):
        self.append(self.ui.inflate('webserver_common:main'))
        self.binder = Binder(None, self)
        self.find_type('servicebar').buttons = self.service_buttons

        # Hosts preperation

        self.hosts_dir = AvailabilitySymlinks(
            self.hosts_available_dir,
            self.hosts_enabled_dir,
            self.supports_host_activation
        )

        def delete_host(host, c):
            self.log('removed host %s' % host.name)
            c.remove(host)
            self.hosts_dir.delete(host.name)

        def on_host_bind(o, c, host, u):
            host.__old_name = host.name

        def on_host_update(o, c, host, u):
            if host.__old_name != host.name:
                self.log('renamed host %s to %s' % (host.__old_name, host.name))
                self.hosts_dir.rename(host.__old_name, host.name)
            host.save()

        def new_host(c):
            name = 'untitled'
            while os.path.exists(self.hosts_dir.get_path(name)):
                name += '_'
            self.log('created host %s' % name)
            self.hosts_dir.open(name, 'w').write(self.template)
            return WebserverConf(self, self.hosts_dir, name)

        self.find('hosts').delete_item = delete_host
        self.find('hosts').new_item = new_host
        self.find('hosts').post_item_bind = on_host_bind
        self.find('hosts').post_item_update = on_host_update
        self.find('header-active-checkbox').visible = \
            self.find('body-active-line').visible = \
            self.supports_host_activation

        def on_conf_bind(o, c, conf, u):
            conf.__old_name = conf.name

        def on_conf_update(o, c, conf, u):
            conf.save()

        self.find('configurations').post_item_bind = on_conf_bind
        self.find('configurations').post_item_update = on_conf_update

        self.tabs = self.find('tabs')

    def on_page_load(self):
        self.refresh()

    @on('save-button', 'click')
    def save(self):
        self.log('saving hosts')
        self.binder.update()
        self.refresh()
        self.context.notify('info', 'Saved')

    def refresh(self):
        self.hosts = [WebserverConf(self, self.hosts_dir, x) for x in self.hosts_dir.list_available()]
        self.configurations = [WebserverMainConf(y).update() for y in
                               self.main_conf_files] if self.configurable else []

        self.binder.setup(self).populate()
        self.find_type('servicebar').reload()
