#!/usr/bin/env python3

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
gi.require_version('Gegl', '0.4')
from gi.repository import Gegl
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio
import sys

def N_(message): return message
def _(message): return GLib.dgettext(None, message)

def entry_point(procedure, run_mode, image, n_drawables, drawables, args, data):
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

class Pictonode (Gimp.PlugIn):

    ## GimpPlugIn virtual methods ##
    def do_set_i18n(self, procname):
        return True, 'gimp30-python', None

    def do_query_procedures(self):
        return [ 'pictonode' ]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)
        procedure.set_image_types("RGB*, GRAY*");
        procedure.set_sensitivity_mask (Gimp.ProcedureSensitivityMask.DRAWABLE |
                                        Gimp.ProcedureSensitivityMask.DRAWABLES)
        procedure.set_documentation (_("Pictonode"),
                                     _("Launches Pictonode plugin"),
                                     name)
        procedure.set_menu_label(_("Launch"))
        procedure.set_attribution("Stephen Foster",
                                  "Team Picto",
                                  "2022")
        procedure.add_menu_path ("<Image>/Pictonode")

        procedure.add_argument_from_property(self, "name")

        return procedure

    def run(self, procedure, run_mode, image, n_drawables, drawables, args, run_data):
        if n_drawables != 1:
            msg = _("Procedure '{}' only works with one drawable.").format(procedure.get_name())
            error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), msg, 0)
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, error)
        else:
            drawable = drawables[0]

        if run_mode == Gimp.RunMode.INTERACTIVE:
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
            gi.require_version('Gdk', '3.0')
            from gi.repository import Gdk

            GimpUi.init("pictonode.py")

            print(drawable.get_buffer())

            dialog = GimpUi.Dialog(use_header_bar=True,
                                   title=_("Pictonode"),
                                   role="es1-Python3")

            dialog.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
            dialog.add_button(_("_Source"), Gtk.ResponseType.APPLY)
            dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
            
            win = Gtk.ApplicationWindow()
            win.set_title("Pictonode")
            win.set_default_size(1000, 500)

            grid = Gtk.Grid()

            image_display = Gtk.Image()
            image_path = image.get_file().get_path()
            image_display.set_from_file(image_path)

            button = Gtk.Button(label="Button 1")

            grid.attach(button, 0, 2, 20, 10)
            grid.attach(image_display, 0, 1, 1000, 500)

            win.add(grid)
            win.show_all()

            ''' geometry = Gdk.Geometry()
            geometry.min_aspect = 0.5
            geometry.max_aspect = 1.0
            dialog.set_geometry_hints(None, geometry, Gdk.WindowHints.ASPECT)
            '''

            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            img = Gtk.Image.new_from_file('C:/Users/parke/Pictures/Camera Roll/example.jpg')

            frame_rgb = Gtk.Frame(label='RGB image')
            box.pack_start(frame_rgb, True, True, 0)
            
            dialog.get_content_area().add(box)
            box.show()

            while (True):
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    position = Gimp.get_pdb().run_procedure('gimp-image-get-item-position',
                                 [image,
                                  drawable]).index(1)

                    # close dialog
                    dialog.destroy()
                    break
                else:
                    dialog.destroy()
                    return procedure.new_return_values(Gimp.PDBStatusType.CANCEL,
                                                       GLib.Error())
        
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(Pictonode.__gtype__, sys.argv)