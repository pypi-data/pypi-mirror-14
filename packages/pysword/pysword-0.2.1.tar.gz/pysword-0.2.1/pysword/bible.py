###############################################################################
# PySword - A native Python reader of the SWORD Project Bible Modules         #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 Various developers:                                 #
# Kenneth Arnold, Joshua Gross, Ryan Hiebert, Matthew Wardrop, Tomas Groth    #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 51  #
# Franklin St, Fifth Floor, Boston, MA 02110-1301 USA                         #
###############################################################################

import os
import struct
import zlib

from pysword.books import BibleStructure
from pysword.cleaner import OSISCleaner, GBFCleaner, ThMLCleaner


class SwordModuleType:
    RAWTEXT = u'rawtext'
    ZTEXT = u'ztext'
    RAWTEXT4 = u'rawtext4'
    ZTEXT4 = u'ztext4'


class SwordBible(object):

    def __init__(self, module_path, module_type=SwordModuleType.ZTEXT, versification=u'default', encoding=None,
                 source_type=u'OSIS'):
        """
        Initialize the SwordBible object.
        :param module_path: Path to SWORD modules datapath.
        :param module_type: Types as defined by SwordModuleType, defaults to 'ztext'.
        :param versification: Versification used for bible, defaults to 'default'.
        :param encoding: Encoding used by the bible, should be either 'utf-8' or 'latin1'.
        :param source_type: Type of (possible) tags in the text, can be 'OSIS', 'GBF' or 'ThML'.
        :raise IOError: If files cannot be opened.
        :raise ValueError: If unknown module_type is supplied.
        """
        self._module_type = module_type.lower()
        self._module_path = module_path
        self._files = {}

        # Open the files needed to read from the module
        if self._module_type in (SwordModuleType.ZTEXT, SwordModuleType.ZTEXT4):
            try:
                self._files[u'ot'] = self._get_ztext_files(u'ot')
            except IOError:
                pass
            try:
                self._files[u'nt'] = self._get_ztext_files(u'nt')
            except IOError:
                pass
        elif self._module_type in (SwordModuleType.RAWTEXT, SwordModuleType.RAWTEXT4):
            try:
                self._files[u'ot'] = self._get_rawtext_files(u'ot')
            except IOError:
                pass
            try:
                self._files[u'nt'] = self._get_rawtext_files(u'nt')
            except IOError:
                pass
        else:
            raise ValueError(u'Invalid module type: %s' % module_type)
        if u'ot' not in self._files and u'nt' not in self._files is None:
            raise IOError(u'Could not open OT or NT for module')

        # Load the bible structure
        testaments = self._files.keys()
        self._structure = BibleStructure(versification, testaments)

        # Set verse record format and size
        if self._module_type == SwordModuleType.ZTEXT:
            self._verse_record_format = u'<IIH'
            self._verse_record_size = 10
        elif self._module_type == SwordModuleType.ZTEXT4:
            self._verse_record_format = u'<III'
            self._verse_record_size = 12
        elif self._module_type == SwordModuleType.RAWTEXT:
            self._verse_record_format = u'<IH'
            self._verse_record_size = 6
        elif self._module_type == SwordModuleType.RAWTEXT4:
            self._verse_record_format = u'<II'
            self._verse_record_size = 8

        # Detect text-encoding if none given
        if encoding is None:
            # pick the first available testament for testing
            testament = self._files.keys()[0]
            if self._module_type in (SwordModuleType.ZTEXT, SwordModuleType.ZTEXT4):
                undecoded_text = self._uncompressed_text(testament, 0)
            else:
                undecoded_text = self._files[testament][1].read(4096)
            # Try to decode to utf-8, if it fails we fallback to latin1
            try:
                undecoded_text.decode()
                self._encoding = u'utf-8'
            except UnicodeDecodeError:
                self._encoding = u'latin1'
        else:
            self._encoding = encoding
        # Create cleaner to remove OSIS or GBF tags
        if source_type:
            if source_type.upper() == u'THML':
                self._cleaner = ThMLCleaner()
            elif source_type.upper() == u'GBF':
                self._cleaner = GBFCleaner()
            else:
                self._cleaner = OSISCleaner()
        else:
            self._cleaner = OSISCleaner()

    def _get_ztext_files(self, testament):
        """
        Given a testament ('ot' or 'nt'), returns a tuple of files (verse_to_buf, buf_to_loc, text)
        :param testament: 'ot' or 'nt'
        :return: returns a tuple of files (verse_to_buf, buf_to_loc, text)
        """
        v2b_name, b2l_name, text_name = [os.path.join(self._module_path,
                                                      u'%s.bz%s' % (testament, code))
                                         for code in (u'v', u's', u'z')]
        return [open(name, u'rb') for name in (v2b_name, b2l_name, text_name)]

    def _get_rawtext_files(self, testament):
        """
        "Given a testament ('ot' or 'nt'), returns a tuple of files (verse_to_loc, text)
        :param testament: 'ot' or 'nt'
        :return: returns a tuple of files (verse_to_loc, text)
        """
        v2l_name = os.path.join(self._module_path, u'%s.vss' % testament)
        text_name = os.path.join(self._module_path, u'%s' % testament)
        return [open(name, u'rb') for name in (v2l_name, text_name)]

    def _ztext_for_index(self, testament, index):
        """
        Get the ztext for a given index.
        :param testament: 'ot' or 'nt'
        :param index: Verse buffer to read
        :return: the text.
        """
        verse_to_buf, buf_to_loc, text = self._files[testament]

        # Read the verse record.
        verse_to_buf.seek(self._verse_record_size*index)
        buf_num, verse_start, verse_len = struct.unpack(self._verse_record_format,
                                                        verse_to_buf.read(self._verse_record_size))
        uncompressed_text = self._uncompressed_text(testament, buf_num)
        return uncompressed_text[verse_start:verse_start+verse_len].decode(self._encoding, errors=u'replace')

    def _uncompressed_text(self, testament, buf_num):
        """
        Decompress ztext at given position.
        :param testament: 'ot' or 'nt'
        :param buf_num: Buffer to read
        :return: The decompressed text
        """
        verse_to_buf, buf_to_loc, text = self._files[testament]

        # Determine where the compressed data starts and ends.
        buf_to_loc.seek(buf_num*12)
        offset, size, uc_size = struct.unpack(u'<III', buf_to_loc.read(12))

        # Get the compressed data.
        text.seek(offset)
        compressed_data = text.read(size)
        return zlib.decompress(compressed_data)

    def _rawtext_for_index(self, testament, index):
        """
        Get the rawtext for a given index.
        :param testament: 'ot' or 'nt'
        :param index: Verse buffer to read
        :return: the text.
        """
        verse_to_loc, text = self._files[testament]

        # Read the verse record.
        verse_to_loc.seek(self._verse_record_size*index)
        verse_start, verse_len = struct.unpack(self._verse_record_format, verse_to_loc.read(self._verse_record_size))
        text.seek(verse_start)
        return text.read(verse_len).decode(self._encoding, errors=u'replace')

    # USER FACING #################################################################################
    def get_iter(self, books=None, chapters=None, verses=None, clean=True):
        """
        Retrieve the text for a given reference as a dict.
        :param books: Single book name or an array of book names
        :param chapters: Single chapter number or an array of chapter numbers
        :param verses: Single verse number or an array of verse numbers
        :param clean: True for cleaning text for tags, False to keep them.
        :return: iterator for the dict that contains the text
        """
        indicies = self._structure.ref_to_indicies(books=books, chapters=chapters, verses=verses)

        for testament, idxs in indicies.items():
            for idx in idxs:
                if self._module_type in (SwordModuleType.ZTEXT, SwordModuleType.ZTEXT4):
                    text = self._ztext_for_index(testament, idx)
                else:
                    text = self._rawtext_for_index(testament, idx)
                if text is None:
                    continue
                if clean and self._cleaner and '<' in text:
                    text = self._cleaner.clean(text)
                yield text

    def get(self, books=None, chapters=None, verses=None, clean=True, join='\n'):
        """
        Retrieve the text for a given reference.
        :param books: Single book name or an array of book names
        :param chapters: Single chapter number or an array of chapter numbers
        :param verses: Single verse number or an array of verse numbers
        :param clean: True for cleaning text for tags, False to keep them.
        :param join: The char/string that should be used to mark a new verse, defaults to '\n'
        :return: the text for the reference.
        """
        output = []
        output.extend(list(self.get_iter(books=books, chapters=chapters, verses=verses, clean=clean)))
        return join.join(output)

    def get_structure(self):
        """
        Retrieve the structure of this bible.
        :return: BibleStructure of this bible
        """
        return self._structure
