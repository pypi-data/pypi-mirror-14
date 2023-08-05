# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import logging
import os
import re
import traceback
from collections import defaultdict

import six
from pathspec import PathSpec
from pathspec.gitignore import GitIgnorePattern
from twitter.common.collections import OrderedSet

from pants.base.build_environment import get_buildroot
from pants.base.build_file import BuildFile
from pants.base.deprecated import deprecated, deprecated_conditional
from pants.base.project_tree import ProjectTree
from pants.base.specs import DescendantAddresses, SiblingAddresses, SingleAddress
from pants.build_graph.address import Address, parse_spec
from pants.build_graph.address_lookup_error import AddressLookupError
from pants.build_graph.build_file_parser import BuildFileParser
from pants.util.dirutil import fast_relpath


logger = logging.getLogger(__name__)


# Note: Significant effort has been made to keep the types BuildFile, BuildGraph, Address, and
# Target separated appropriately.  The BuildFileAddressMapper is intended to have knowledge
# of just BuildFile, BuildFileParser and Address.
#
# Here are some guidelines to help maintain this abstraction:
#  - Use the terminology 'address' instead of 'target' in symbols and user messages
#  - Wrap exceptions from BuildFile and BuildFileParser with a subclass of AddressLookupError
#     so that callers do not have to reference those modules
#
# Note: 'spec' should not be a user visible term, substitute 'address' instead.
class BuildFileAddressMapper(object):
  """Maps addresses in the pants virtual address space to corresponding BUILD file declarations."""

  class AddressNotInBuildFile(AddressLookupError):
    """Indicates an address cannot be found in an existing BUILD file."""

  class EmptyBuildFileError(AddressLookupError):
    """Indicates no addresses are defined in a BUILD file."""

  class InvalidBuildFileReference(AddressLookupError):
    """Indicates no BUILD file exists at the address referenced."""

  class InvalidAddressError(AddressLookupError):
    """Indicates an address cannot be parsed."""

  class BuildFileScanError(AddressLookupError):
    """Indicates a problem was encountered scanning a tree of BUILD files."""

  class InvalidRootError(BuildFileScanError):
    """Indicates an invalid scan root was supplied."""

  # Target specs are mapped to the patterns which match them, if any. This variable is a key for
  # specs which don't match any exclusion regexps. We know it won't already be in the list of
  # patterns, because the asterisks in its name make it an invalid regexp.
  _UNMATCHED_KEY = '** unmatched **'

  def __init__(self, build_file_parser, project_tree, build_ignore_patterns=None, exclude_target_regexps=None):
    """Create a BuildFileAddressMapper.

    :param build_file_parser: An instance of BuildFileParser
    :param build_file_type: A subclass of BuildFile used to construct and cache BuildFile objects
    """
    self._build_file_parser = build_file_parser
    self._spec_path_to_address_map_map = {}  # {spec_path: {address: addressable}} mapping
    if isinstance(project_tree, ProjectTree):
      self._project_tree = project_tree
    else:
      # If project_tree is BuildFile class actually.
      # TODO(tabishev): Remove after transition period.
      self._project_tree = project_tree._get_project_tree(self.root_dir)
    self._build_ignore_patterns = PathSpec.from_lines(GitIgnorePattern, build_ignore_patterns or [])

    self._exclude_target_regexps = exclude_target_regexps or []
    self._exclude_patterns = [re.compile(pattern) for pattern in self._exclude_target_regexps]

  @property
  def root_dir(self):
    return self._build_file_parser.root_dir

  def _raise_incorrect_address_error(self, spec_path, wrong_target_name, targets):
    """Search through the list of targets and return those which originate from the same folder
    which wrong_target_name resides in.

    :raises: A helpful error message listing possible correct target addresses.
    """
    was_not_found_message = '{target_name} was not found in BUILD files from {spec_path}'.format(
      target_name=wrong_target_name, spec_path=os.path.join(self._project_tree.build_root, spec_path))

    if not targets:
      raise self.EmptyBuildFileError(
        '{was_not_found_message}, because that directory contains no BUILD files defining addressable entities.'
          .format(was_not_found_message=was_not_found_message))

    # Print BUILD file extensions if there's more than one BUILD file with targets only.
    if len(set([target.build_file for target in targets])) == 1:
      specs = [':{}'.format(target.target_name) for target in targets]
    else:
      specs = [':{} (from {})'.format(target.target_name, os.path.basename(target.build_file.relpath))
               for target in targets]

    # Might be neat to sort by edit distance or something, but for now alphabetical is fine.
    specs = [''.join(pair) for pair in sorted(specs)]

    # Give different error messages depending on whether BUILD file was empty.
    one_of = ' one of' if len(specs) > 1 else ''  # Handle plurality, just for UX.
    raise self.AddressNotInBuildFile(
      '{was_not_found_message}. Perhaps you '
      'meant{one_of}: \n  {specs}'.format(was_not_found_message=was_not_found_message,
                                          one_of=one_of,
                                          specs='\n  '.join(specs)))

  def resolve(self, address):
    """Maps an address in the virtual address space to an object.

    :param Address address: the address to lookup in a BUILD file
    :raises AddressLookupError: if the path to the address is not found.
    :returns: A tuple of the natively mapped BuildFileAddress and the Addressable it points to.
    """
    address_map = self._address_map_from_spec_path(address.spec_path)
    if address not in address_map:
      self._raise_incorrect_address_error(address.spec_path, address.target_name, address_map)
    else:
      return address_map[address]

  def resolve_spec(self, spec):
    """Converts a spec to an address and maps it using `resolve`"""
    try:
      address = Address.parse(spec)
    except ValueError as e:
      raise self.InvalidAddressError(e)
    _, addressable = self.resolve(address)
    return addressable

  def _address_map_from_spec_path(self, spec_path):
    """Returns a resolution map of all addresses in a "directory" in the virtual address space.
    :returns {Address: (Address, <resolved Object>)}:
    """
    if spec_path not in self._spec_path_to_address_map_map:
      try:
        build_files = list(BuildFile.get_build_files_family(self._project_tree, spec_path,
                                                            self._build_ignore_patterns))
        if not build_files:
          raise self.BuildFileScanError("{spec_path} does not contain any BUILD files."
                                        .format(spec_path=os.path.join(self.root_dir, spec_path)))
        mapping = self._build_file_parser.address_map_from_build_files(build_files)
      except BuildFileParser.BuildFileParserError as e:
        raise AddressLookupError("{message}\n Loading addresses from '{spec_path}' failed."
                                 .format(message=e, spec_path=spec_path))

      address_map = {address: (address, addressed) for address, addressed in mapping.items()}
      self._spec_path_to_address_map_map[spec_path] = address_map
    return self._spec_path_to_address_map_map[spec_path]

  def addresses_in_spec_path(self, spec_path):
    """Returns only the addresses gathered by `address_map_from_spec_path`, with no values."""
    return self._address_map_from_spec_path(spec_path).keys()

  def spec_to_address(self, spec, relative_to=''):
    """A helper method for mapping a spec to the correct build file address.

    :param string spec: A spec to lookup in the map.
    :param string relative_to: Path the spec might be relative to
    :raises :class:`pants.build_graph.address_lookup_error.AddressLookupError`
            If the BUILD file cannot be found in the path specified by the spec.
    :returns: A new Address instance.
    :rtype: :class:`pants.build_graph.address.BuildFileAddress`
    """
    spec_path, name = parse_spec(spec, relative_to=relative_to)
    address = Address(spec_path, name)
    try:
      build_file_address, _ = self.resolve(address)
      return build_file_address
    except AddressLookupError as e:
      raise self.InvalidBuildFileReference('{message}\n  when translating spec {spec}'
                                           .format(message=e, spec=spec))

  def scan_build_files(self, base_path, spec_excludes=None):
    deprecated_conditional(lambda: spec_excludes is not None,
                           '0.0.75',
                           'Use build_ignore_patterns consturctor parameter instead.')
    return BuildFile.scan_build_files(self._project_tree, base_path, spec_excludes,
                                      build_ignore_patterns=self._build_ignore_patterns)

  def specs_to_addresses(self, specs, relative_to=''):
    """The equivalent of `spec_to_address` for a group of specs all relative to the same path.

    :param spec: iterable of Addresses.
    :raises AddressLookupError: if the BUILD file cannot be found in the path specified by the spec
    """
    for spec in specs:
      yield self.spec_to_address(spec, relative_to=relative_to)

  def scan_addresses(self, root=None, spec_excludes=None):
    """Recursively gathers all addresses visible under `root` of the virtual address space.

    :param string root: The absolute path of the root to scan; defaults to the root directory of the
                        pants project.
    :rtype: set of :class:`pants.build_graph.address.Address`
    :raises AddressLookupError: if there is a problem parsing a BUILD file
    """
    deprecated_conditional(lambda: spec_excludes is not None,
                           '0.0.75',
                           'Use build_ignore_patterns constructor parameter instead.')

    root_dir = get_buildroot()
    base_path = None

    if root:
      try:
        base_path = fast_relpath(root, root_dir)
      except ValueError as e:
        raise self.InvalidRootError(e)

    addresses = set()
    try:
      for build_file in BuildFile.scan_build_files(self._project_tree,
                                                   base_relpath=base_path,
                                                   spec_excludes=spec_excludes,
                                                   build_ignore_patterns=self._build_ignore_patterns):
        for address in self.addresses_in_spec_path(build_file.spec_path):
          addresses.add(address)
    except BuildFile.BuildFileError as e:
      # Handle exception from BuildFile out of paranoia.  Currently, there is no way to trigger it.
      raise self.BuildFileScanError("{message}\n while scanning BUILD files in '{root}'."
                                    .format(message=e, root=root))
    return addresses

  def scan_specs(self, specs, fail_fast=True, spec_excludes=None):
    """Execute a collection of `specs.Spec` objects and return an ordered set of Addresses."""
    excluded_target_map = defaultdict(set)  # pattern -> targets (for debugging)
    deprecated_conditional(lambda: spec_excludes is not None,
                           '0.0.75',
                           'Use build_ignore_patterns in address_mapper instead.')

    def exclude_spec(spec):
      for pattern in self._exclude_patterns:
        if pattern.search(spec) is not None:
          excluded_target_map[pattern.pattern].add(spec)
          return True
      excluded_target_map[self._UNMATCHED_KEY].add(spec)
      return False

    def exclude_address(address):
      return exclude_spec(address.spec)

    addresses = OrderedSet()
    for spec in specs:
      for address in self._scan_spec(spec, fail_fast, spec_excludes, exclude_spec):
        if not exclude_address(address):
          addresses.add(address)

    # Print debug information about the excluded targets
    if logger.getEffectiveLevel() <= logging.DEBUG and excluded_target_map:
      logger.debug('excludes:\n  {excludes}'
                   .format(excludes='\n  '.join(self._exclude_target_regexps)))
      targets = ', '.join(excluded_target_map[self._UNMATCHED_KEY])
      logger.debug('Targets after excludes: {targets}'.format(targets=targets))
      excluded_count = 0
      for pattern, targets in six.iteritems(excluded_target_map):
        if pattern != self._UNMATCHED_KEY:
          logger.debug('Targets excluded by pattern {pattern}\n  {targets}'
                       .format(pattern=pattern,
                               targets='\n  '.join(targets)))
          excluded_count += len(targets)
      logger.debug('Excluded {count} target{plural}.'
                   .format(count=excluded_count,
                           plural=('s' if excluded_count != 1 else '')))
    return addresses

  def _scan_spec(self, spec, fail_fast, spec_excludes, exclude_spec):
    """Scans the given address spec."""

    errored_out = []

    if type(spec) is DescendantAddresses:
      addresses = set()
      try:
        build_files = self.scan_build_files(base_path=spec.directory,
                                            spec_excludes=spec_excludes)
      except BuildFile.BuildFileError as e:
        raise AddressLookupError(e)

      for build_file in build_files:
        try:
          addresses.update(self.addresses_in_spec_path(build_file.spec_path))
        except (BuildFile.BuildFileError, AddressLookupError) as e:
          # This attempts to filter out broken BUILD files before we parse them.
          if exclude_spec(build_file.spec_path):
            deprecated_conditional(lambda: True,
                                   '0.0.75',
                                   'Filtering broken BUILD files based on exclude_target_regexp is deprecated '
                                   'and will be removed. Use ignore_patterns instead.')
          else:
            if fail_fast:
              raise AddressLookupError(e)
            errored_out.append('--------------------')
            errored_out.append(traceback.format_exc())
            errored_out.append('Exception message: {0}'.format(e))

      if errored_out:
        error_msg = '\n'.join(errored_out + ["Invalid BUILD files for [{0}]".format(spec.to_spec_string())])
        raise AddressLookupError(error_msg)
      return addresses
    elif type(spec) is SiblingAddresses:
      return set(self.addresses_in_spec_path(spec.directory))
    elif type(spec) is SingleAddress:
      return {self.spec_to_address(spec.to_spec_string())}
    else:
      raise ValueError('Unsupported Spec type: {}'.format(spec))
