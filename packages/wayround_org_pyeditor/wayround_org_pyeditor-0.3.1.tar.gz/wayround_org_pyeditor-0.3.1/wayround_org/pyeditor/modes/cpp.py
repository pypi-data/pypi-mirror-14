
import io
import os.path
import subprocess
import re
import modulefinder

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GtkSource
from gi.repository import Pango
from gi.repository import GLib

import wayround_org.utils.path
import wayround_org.utils.timer
import wayround_org.utils.gtk

import wayround_org.pyeditor.buffer
import wayround_org.pyeditor.module_commons


MODE_NAME = 'cpp'

SUPPORTED_MIME = ['text/x-c++']

SUPPORTED_FNM = [
    '*.cc', '*.cp', '*.cxx', '*.cpp', '*.CPP', '*.c++', '*.C'

    '*.hh', '*.H', '*.hp', '*.hxx', '*.hpp', '*.HPP', '*.h++', '*.tcc'
    ]


METHOD_REGEXP = re.compile(
    r'(\@\w+\s*)?'
    r'((public|protected|private|abstract|static|final|strictfp)\s+)*'
    r'\w+\s*(?!(new|catch|if|for|while)\s+)\(.*?\).*?[{;]',
    flags=re.S
    )


class Buffer(wayround_org.pyeditor.module_commons.Buffer):

    @staticmethod
    def get_mode_interface():
        return ModeInterface


class View(wayround_org.pyeditor.module_commons.View):

    @staticmethod
    def get_language_name():
        return MODE_NAME

    def apply_spec_view_settings(self):
        self.view.set_auto_indent(True)
        self.view.set_draw_spaces(GtkSource.DrawSpacesFlags.ALL)
        self.view.set_highlight_current_line(True)
        self.view.set_indent_on_tab(True)
        self.view.set_indent_width(4)
        self.view.set_insert_spaces_instead_of_tabs(True)
        self.view.set_right_margin_position(80)
        self.view.set_show_line_marks(True)
        self.view.set_show_line_numbers(True)
        self.view.set_show_right_margin(True)
        self.view.set_smart_home_end(True)
        self.view.set_tab_width(4)

        return


class SourceMenu:

    def __init__(self, mode_interface):

        self.mode_interface = mode_interface
        self.main_window = mode_interface.main_window

        main_window = self.main_window

        source_me = Gtk.Menu()

        # source_toggle_comment_mi = Gtk.MenuItem.new_with_label(
        #     "Toggle Comment"
        #     )
        # source_comment_mi = Gtk.MenuItem.new_with_label("Comment")
        # source_uncomment_mi = Gtk.MenuItem.new_with_label("Uncomment")

        source_indent_mi = Gtk.MenuItem.new_with_label("Indent")
        source_indent_mi.add_accelerator(
            'activate',
            main_window.accel_group,
            Gdk.KEY_I,
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE
            )
        source_indent_mi.connect(
            'activate',
            self.on_indent_mi,
            False
            )

        source_dedent_mi = Gtk.MenuItem.new_with_label("Dedent")
        source_dedent_mi.add_accelerator(
            'activate',
            main_window.accel_group,
            Gdk.KEY_I,
            Gdk.ModifierType.CONTROL_MASK
            | Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE
            )
        source_dedent_mi.connect(
            'activate',
            self.on_indent_mi,
            True
            )

        source_astyle_mi = Gtk.MenuItem.new_with_label("Use astyle")
        source_astyle_mi.add_accelerator(
            'activate',
            main_window.accel_group,
            Gdk.KEY_F,
            Gdk.ModifierType.CONTROL_MASK
            | Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE
            )
        source_astyle_mi.connect(
            'activate',
            self.on_source_astyle_mi
            )

        edit_delete_line_mi = Gtk.MenuItem.new_with_label("Delete Line")
        edit_delete_line_mi.add_accelerator(
            'activate',
            main_window.accel_group,
            Gdk.KEY_D,
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE
            )
        edit_delete_line_mi.connect(
            'activate',
            self.on_edit_delete_line_mi
            )

        navigate_refresh_outline_mi = \
            Gtk.MenuItem.new_with_label("Refresh Outline")

        navigate_refresh_outline_mi.add_accelerator(
            'activate',
            main_window.accel_group,
            Gdk.KEY_R,
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE
            )
        navigate_refresh_outline_mi.connect(
            'activate',
            self.on_navigate_refresh_outline_mi
            )
        edit_delete_trailing_whitespace_mi = Gtk.MenuItem.new_with_label(
            "Delete Trailing Whitespace"
            )
        edit_delete_trailing_whitespace_mi.add_accelerator(
            'activate',
            main_window.accel_group,
            Gdk.KEY_F,
            Gdk.ModifierType.CONTROL_MASK
            | Gdk.ModifierType.SHIFT_MASK
            | Gdk.ModifierType.MOD1_MASK,
            Gtk.AccelFlags.VISIBLE
            )
        edit_delete_trailing_whitespace_mi.connect(
            'activate',
            self.on_delete_trailing_whitespace_mi
            )

        # source_me.append(source_toggle_comment_mi)
        # source_me.append(source_comment_mi)
        # source_me.append(source_uncomment_mi)
        # source_me.append(Gtk.SeparatorMenuItem())

        source_me.append(edit_delete_line_mi)
        source_me.append(Gtk.SeparatorMenuItem())

        source_me.append(source_indent_mi)
        source_me.append(source_dedent_mi)
        source_me.append(Gtk.SeparatorMenuItem())

        source_me.append(source_astyle_mi)
        source_me.append(edit_delete_trailing_whitespace_mi)
        source_me.append(Gtk.SeparatorMenuItem())

        source_me.append(navigate_refresh_outline_mi)

        self._source_me = source_me

        return

    def get_widget(self):
        return self._source_me

    def destroy(self):
        self.get_widget().destroy()
        return

    def on_source_astyle_mi(self, mi):

        buff = self.main_window.current_buffer
        buff.save_state()

        astyle_params = []

        b = buff.get_buffer()

        t = b.get_text(
            b.get_start_iter(),
            b.get_end_iter(),
            False
            )

        ts = t.split('\n')

        for i in range(2):
            if i < len(ts):
                if (ts[i].startswith('// -*- astyle: ')
                        and ts[i].endswith('-*-')):
                    astyle_params = ts[i].split(' ')[3:-1]

        cmd = ['astyle'] + astyle_params  # + [fn]

        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
        stdout, stderr = p.communicate(bytes(t, 'utf-8'))

        pres = p.wait()
        if pres == 0:
            b.set_text(str(stdout, 'utf-8'))

        else:
            d = Gtk.MessageDialog(
                self.main_window.get_widget(),
                Gtk.DialogFlags.MODAL,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK,
                "error: {}\n{}\n\n{}".format(
                    pres,
                    str(stdout, 'utf-8'),
                    str(stderr, 'utf-8')
                    ),
                )
            res = d.run()
            d.destroy()

        buff.restore_state()

        return

    def on_edit_delete_line_mi(self, mi):
        b = self.main_window.current_buffer.get_buffer()
        wayround_org.pyeditor.module_commons.delete_selected_lines(b)
        return

    def on_navigate_refresh_outline_mi(self, mi):
        mi = self.main_window.mode_interface
        if mi is not None and hasattr(mi, 'outline'):
            mi.outline.reload()
        return

    def _get_selected_lines(self):
        b = self.main_window.current_buffer.get_buffer()
        return wayround_org.pyeditor.module_commons.get_selected_lines(b)

    def on_indent_mi(self, mi, de=False):
        b = self.main_window.current_buffer.get_buffer()
        wayround_org.pyeditor.module_commons.indent_buffer(b, de, 4)
        return

    def on_delete_trailing_whitespace_mi(self, mi):
        buff = self.main_window.current_buffer
        b = buff.get_buffer()

        t = b.get_text(
            b.get_start_iter(),
            b.get_end_iter(),
            False
            )

        buff.save_state()

        t = wayround_org.pyeditor.module_commons.delete_trailing_whitespace(t)

        b.set_text(t)

        buff.restore_state()
        return


class Outline(wayround_org.pyeditor.module_commons.Outline):

    def search(self, buff):

        res = {}

        t = buff.get_text(
            buff.get_start_iter(),
            buff.get_end_iter(),
            False
            )

        excluded_ranges = []

        comments = wayround_org.pyeditor.module_commons.find_c_comments(t)

        excluded_ranges += comments

        last_start = 0
        while True:

            i = METHOD_REGEXP.search(t, last_start)

            if not i:
                break

            m_start = i.start()
            m_end = i.end()

            last_start = m_end + 1

            i_r = range(m_start, m_end)

            in_excluded_ranges = False
            for j in excluded_ranges:

                if i_r.start in j or i_r.stop in j:
                    in_excluded_ranges = True
                    break

                if j.start in i_r or j.stop in i_r:
                    in_excluded_ranges = True
                    break

            if not in_excluded_ranges:
                line = buff.get_iter_at_offset(m_start).get_line()
                s = buff.get_iter_at_line(line)
                e = buff.get_iter_at_offset(m_end)

                t2 = buff.get_text(s, e, False)
                # t2 = t[m_start: m_end]

                # res[line] = t2.strip()
                t2s = t2.strip()
                if (not t2s.endswith(';')
                        and not t2s.startswith('if')
                        and not t2s.startswith('for')
                        and not t2s.startswith('with')):
                    res[line] = t2
                    excluded_ranges.append(i_r)

        return res


class ModeInterface:

    @staticmethod
    def get_menu_name():
        return "C++"

    def __init__(self, main_window):
        self.main_window = main_window

        self.source_menu = SourceMenu(self)
        self.view = View(self)

        self.outline = Outline(self)

        self.lang_mgr = GtkSource.LanguageManager.get_default()

        #self.completion = self.view.get_view_widget().get_completion()
        #self.completion_provider = SourceCompletionProvider()
        #res = self.completion.add_provider(self.completion_provider)
        #print("add_provider: {}".format(res))

        # self.completion.create_context(None)
        return

    def destroy(self):
        self.source_menu.destroy()
        self.view.destroy()
        return

    def get_menu(self):
        return self.source_menu.get_widget()

    def get_view_widget(self):
        return self.view.get_view_widget()

    def get_view_widget_sw(self):
        return self.view.get_view_widget_sw()

    def get_widget(self):
        return self.view.get_widget()

    def set_buffer(self, buff):

        if not isinstance(buff, Buffer):
            raise Exception(
                "`buff' must be an instance of "
                "wayround_org.pyeditor.modes.python.Buffer"
                )

        buff.set_mode_interface(self)
        buff.set_language(self.lang_mgr.get_language('cpp'))
        self.view.set_buffer(buff)
        self.outline.reload()
        return

    def get_view(self):
        return self.view


def indent(txt, de=False):
    return wayround_org.pyeditor.module_commons.indent_text(txt, de, 4)
