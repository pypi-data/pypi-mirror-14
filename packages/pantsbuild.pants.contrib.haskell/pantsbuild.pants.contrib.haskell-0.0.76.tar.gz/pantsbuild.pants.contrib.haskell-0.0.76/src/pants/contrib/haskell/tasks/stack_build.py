# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from pants.contrib.haskell.tasks.stack_task import StackTask


class StackBuild(StackTask):
  """Build the given Haskell targets."""

  @classmethod
  def register_options(cls, register):
    super(StackBuild, cls).register_options(register)
    register('--watch',
             action='store_true',
             help='Watch for changes in local files and automatically rebuild.')

  def execute(self):
    if self.get_options().watch:
      extra_args = ['--file-watch']
    else:
      extra_args = []
    targets = self.context.targets(predicate=self.is_haskell_project)
    with self.invalidated(targets=targets, invalidate_dependents=True) as invalidated:
      for vt in invalidated.invalid_vts:
        self.stack_task('build', vt, extra_args)
