import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Nautilus', '3.0')
from gi.repository import (
    Nautilus,
    GObject,
    Gtk,
    Gdk
)
import subprocess


class NautilusDownloadExtension(
        GObject.GObject,
        Nautilus.FileInfo,
        Nautilus.MenuProvider
):
    def __init__(self):
        pass

    @staticmethod
    def get_clipboard():
        return Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def get_file_items(self, window, files):
        return ()

    def get_background_items(self, window, current_folder):
        top_menuitem = Nautilus.MenuItem(name='NautilusDownloadExtension::NautilusDownload',
                                         label='Download URL',
                                         tip='Download URL')
        top_menuitem.connect('activate', self.download_url_activate_cb, current_folder)
        return (top_menuitem,)

    def download_url_activate_cb(self, menu, current_folder):
        folder_name = current_folder.get_location().get_path()
        print folder_name
        clipboard = self.get_clipboard()
        url = clipboard.wait_for_text()
        try:
            subprocess.check_call(['wget', '-P', folder_name, url])
            mb = Gtk.MessageDialog(
                None,
                Gtk.DialogFlags.DESTROY_WITH_PARENT,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.CLOSE,
                "Download successful"
            )
            mb.run()
            mb.destroy()
        except subprocess.CalledProcessError as e:
            mb = Gtk.MessageDialog(
                None,
                Gtk.DialogFlags.DESTROY_WITH_PARENT,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CLOSE,
                "Can't download from %s" % url
            )
            mb.run()
            mb.destroy()
            print(e)

    def list_copy(self, files):
        print(files)
