import gi 
import shutil
import subprocess

gi.require_version('Nautilus', '4.0')

from gi.repository import Nautilus, GObject
from typing import List

class openFolderMPV(GObject.GObject, Nautilus.MenuProvider):

    def __init__(self):
        super().__init__()

    def menu_activate_cb(
         self,
         menu: Nautilus.MenuItem,
         file: Nautilus.FileInfo,
     ) -> None:
        if file.is_gone():
            return
        
        subprocess.Popen(["mpv",file.get_uri()],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT,start_new_session=True)

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
        ) -> List[Nautilus.MenuItem]:
        if len(files) != 1:
            return []

        file = files[0]

        if not file.is_directory():
            return []

        if not shutil.which("mpv"):
            return[]
        
        item = Nautilus.MenuItem(
            name="abrirConMPV",
            label="Abrir con MPV: %s" % file.get_name(),
        )
        item.connect("activate", self.menu_activate_cb, file)

        return [
            item,
        ]

    def get_background_items(
         self,
         current_folder: Nautilus.FileInfo,
     ) -> List[Nautilus.MenuItem]:
         return []
