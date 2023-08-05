import os
import sys

from app.lookups import base as lookups
from app.drivers.options import shared_options


class BaseDriver(object):
    def __init__(self):
        self.lookupfn = None
        self.infiletype = ''

    def set_lookup(self):
        if self.lookupfn is not None and hasattr(self, 'lookuptype'):
            self.lookup = lookups.get_lookup(self.lookupfn, self.lookuptype)
        else:
            self.lookup = None

    def set_options(self):
        self.options = self.define_options(['fn', 'outdir'], {})
        self.options['-i']['help'].format(self.infiletype)

    def get_commandhelp(self):
        return self.commandhelp

    def get_options(self):
        return self.options.values()

    def define_options(self, names, parser_options):
        """Given a list of option names, this returns a list of dicts
        defined in all_options and self.shared_options. These can then
        be used to populate the argparser with"""
        def copy_option(options, name):
            return {k: v for k, v in options[name].items()}
        options = {}
        for name in names:
            try:
                option = copy_option(parser_options, name)
            except KeyError:
                option = copy_option(shared_options, name)
            try:
                options.update({option['clarg']: option})
            except TypeError:
                options.update({option['clarg'][0]: option})
        return options

    def parse_input(self, **kwargs):
        for option in self.get_options():
            opt_argkey = option['driverattr']
            opt_val = kwargs.get(opt_argkey)
            if 'type' in option and option['type'] == 'pick':
                if not option.get('required') and not opt_val:
                    pass
                else:
                    try:
                        assert opt_val in option['picks']
                    except AssertionError:
                            print('Option {} should be one of [{}]'.format(
                                option['clarg'], ','.join(option['picks'])))
                            sys.exit(1)
            setattr(self, opt_argkey, opt_val)

    def start(self, **kwargs):
        self.parse_input(**kwargs)
        self.set_lookup()
        self.run()

    def finish(self):
        """Cleans up after work"""
        pass

    def create_outfilepath(self, fn, suffix=None):
        basefn = os.path.basename(fn)
        outfn = basefn + suffix
        return os.path.join(self.outdir, outfn)

    def get_column_header_for_number(self, column_var_names, header=False):
        """This function subtracts 1 from inputted column number to comply
        with programmers counting (i.e. from 0, not from 1). For TSV data."""
        if not header:
            header = self.oldheader
        for col in column_var_names:
            value = getattr(self, col)
            if not value or value is None:
                continue
            setattr(self, col, header[int(value) - 1])

    def get_commandname(self):
        return self.command
