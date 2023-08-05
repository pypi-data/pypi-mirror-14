# -*- coding: utf-8 -*-

"""
    Extension for the python ``click`` module to provide
    a group with a git-like *did-you-mean* feature.
"""

import click
import difflib

__version__ = "0.0.1"


class DYMMixin(object):  # pylint: disable=too-few-public-methods
    """
    Mixin class for click MultiCommand inherited classes
    to provide git-like *did-you-mean* functionality when
    a certain command is not registered.
    """
    def __init__(self, name=None, whatever=None, max_suggestions=3, cutoff=0.5, **attrs):
        self.max_suggestions = max_suggestions
        self.cutoff = cutoff
        super(DYMMixin, self).__init__(name, whatever, **attrs)

    def resolve_command(self, ctx, args):
        """
        Overrides clicks ``resolve_command`` method
        and appends *Did you mean ...* suggestions
        to the raised exception message.
        """
        original_cmd_name = click.utils.make_str(args[0])

        try:
            return super(DYMMixin, self).resolve_command(ctx, args)
        except click.exceptions.UsageError as error:
            error_msg = str(error)
            matches = difflib.get_close_matches(original_cmd_name,
                                                self.list_commands(ctx), self.max_suggestions, self.cutoff)
            if matches:
                error_msg += '\n\nDid you mean one of these?\n    %s' % '\n    '.join(matches)  # pylint: disable=line-too-long

            raise click.exceptions.UsageError(error_msg, error.ctx)


class DYMGroup(DYMMixin, click.Group):  # pylint: disable=too-many-public-methods
    """
    click Group to provide git-like
    *did-you-mean* functionality when a certain
    command is not found in the group.
    """
    def __init__(self, name=None, commands=None, max_suggestions=3, cutoff=0.5, **attrs):
        super(DYMGroup, self).__init__(name, commands, max_suggestions, cutoff, **attrs)


class DYMCommandCollection(DYMMixin, click.CommandCollection):  # pylint: disable=too-many-public-methods
    """
    click CommandCollection to provide git-like
    *did-you-mean* functionality when a certain
    command is not found in the group.
    """
    def __init__(self, name=None, sources=None, max_suggestions=3, cutoff=0.5, **attrs):
        super(DYMCommandCollection, self).__init__(name, sources, max_suggestions, cutoff, **attrs)
