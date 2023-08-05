# coding=utf-8
#
# Copyright 2014 Sascha Schirra
#
# This file is part of Ropper.
#
# Ropper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ropper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ctypes import *
from ropper.loaders.loader import *
from ropper.loaders.elf_intern.elf_gen import *
from ropper.common.error import LoaderError
import importlib
import os


class EhdrData(DataContainer):
    """
    struct = SectionHeader
    bytes = c_byte_array (section bytes)
    """

class ShdrData(DataContainer):

    """
    struct = SectionHeader
    name = string (section name)
    bytes = c_byte_array (section bytes)
    """


class PhdrData(DataContainer):

    """
    struct = ProgrammHeader
    bytes = c_byte_array (section bytes)
    """


class SymbolData(DataContainer):

    """
    struct = Symbol
    name = string
    type = int
    """


class RelocationData(DataContainer):

    """
    struct = RelocationStruct
    symbol = SymbolData
    """


class ELF(Loader):

    def __init__(self, filename):

        self.ehdr = None
        self.phdrs = []
        self.shdrs = []
        self.symbols = {}
        self.relocations = {}
        self.__elf_module = None
        self.__execSections = None
        self.__dataSections = None

        super(ELF, self).__init__(filename)

    def __loadElfModule(self):
        modName = None
        if self._bytes[EI.CLASS] == ELFCLASS.BITS_32:
            modName = 'ropper.loaders.elf_intern.elf32_'
        elif self._bytes[EI.CLASS] == ELFCLASS.BITS_64:
            modName = 'ropper.loaders.elf_intern.elf64_'
        else:
            raise LoaderError('Bad architecture')
        self.__elf_module = importlib.import_module(
            modName + str(ELFDATA[self._bytes[EI.DATA]]))

    def __parsePhdrs(self, p_bytes):
        p_tmp = c_void_p(p_bytes.value + self.ehdr.e_phoff)

        for i in range(self.ehdr.e_phnum):
            self.assertFileRange(p_tmp.value)
            phdr = cast(p_tmp, POINTER(self.__elf_module.Phdr)).contents
            phdrData = PhdrData(struct=phdr)
            self.phdrs.append(phdrData)

            p_tmp.value += self.ehdr.e_phentsize


    def __parseShdrs(self, p_bytes):
        p_tmp = c_void_p(p_bytes.value + self.ehdr.e_shoff)
        hdrs = []
        for i in range(self.ehdr.e_shnum):
            self.assertFileRange(p_tmp.value)
            shdr = cast(p_tmp, POINTER(self.__elf_module.Shdr)).contents
            hdrs.append(shdr)

            p_tmp.value += self.ehdr.e_shentsize

        self.__parseSections(hdrs, p_bytes)

    def __parseSections(self, hdrs, p_bytes):
        for hdr in hdrs:
            p_tmp = c_void_p(p_bytes.value + hdr.sh_offset)
            self.assertFileRange(p_tmp.value)
            ibytes = cast(p_tmp, POINTER(c_ubyte * hdr.sh_size)).contents
            self.shdrs.append(ShdrData(name='', struct=hdr, bytes=ibytes))

        self.__parseSectionNames(self.shdrs)

    def __parseSectionNames(self, shdrs):
        if self.ehdr.e_shstrndx != SHN.UNDEF:
            strtab = self.shdrs[self.ehdr.e_shstrndx]
            strtab_p = cast(pointer(strtab.bytes), c_void_p)
            strtab_tmp = c_void_p(strtab_p.value)

            for hdr in shdrs:

                strtab_tmp.value = strtab_p.value + hdr.struct.sh_name
                self.assertFileRange(strtab_tmp.value)
                name = cast(strtab_tmp, c_char_p).value
                hdr.name = name

    def __getName(self, strtab, idx):
        strtab_p = cast(pointer(strtab.bytes), c_void_p)
        strtab_p.value += idx
        self.assertFileRange(strtab_p.value)
        name = cast(strtab_p, c_char_p).value
        return name

    def __parseSymbols(self):

        for hdr in self.shdrs:
            if hdr.struct.sh_type == SHT.DYNSYM or hdr.struct.sh_type == SHT.SYMTAB:
                symbols = self.__parseSymbolEntries(
                    hdr, self.shdrs[hdr.struct.sh_link])
                self.symbols[hdr.name] = symbols

    def __parseSymbolEntries(self, shdr, strtab):
        entries = []
        bytes_p = cast(pointer(shdr.bytes), c_void_p)

        for i in range(int(shdr.struct.sh_size / sizeof(self.__elf_module.Sym))):
            self.assertFileRange(bytes_p.value)
            entry = cast(bytes_p, POINTER(self.__elf_module.Sym)).contents
            name = self.__getName(strtab, entry.st_name)

            entries.append(SymbolData(
                struct=entry, name=name, type=entry.st_info & 0xf, bind=entry.st_info >> 4))

            bytes_p.value += sizeof(self.__elf_module.Sym)

        return entries

    def __parseRelocations(self):
        if len(self.symbols) == 0:
            self.__parseSymbols()

        for hdr in self.shdrs:
            if hdr.struct.sh_link != SHN.UNDEF and (hdr.struct.sh_type == SHT.REL or hdr.struct.sh_type == SHT.RELA):
                symbols = self.symbols[self.shdrs[hdr.struct.sh_link].name]
                relocations = self.__parseRelocationEntries(hdr, symbols)
                self.relocations[hdr.name] = relocations

    def __parseRelocationEntries(self, shdr, symbols):
        struct = self.__elf_module.Rel if shdr.struct.sh_type == SHT.REL else self.__elf_module.Rela
        bytes_p = cast(pointer(shdr.bytes), c_void_p)
        entries = []

        for i in range(int(shdr.struct.sh_size / sizeof(struct))):
            self.assertFileRange(bytes_p.value)
            entry = cast(bytes_p, POINTER(struct)).contents
            sym = symbols[self.__elf_module.R_SYM(entry.r_info)]
            entries.append(
                RelocationData(struct=entry, symbol=sym, type=self.__elf_module.R_TYPE(entry.r_info)))
            bytes_p.value += sizeof(struct)
        return entries

    def __parse(self, p_bytes):
        p_tmp = c_void_p(p_bytes.value)
        self.assertFileRange(p_tmp.value)
        self.ehdr = cast(p_tmp, POINTER(self.__elf_module.Ehdr)).contents

        self.__parsePhdrs(p_bytes)
        self.__parseShdrs(p_bytes)
        self.__parseSymbols()
        self.__parseRelocations()

    def _parseFile(self):
        self.__loadElfModule()
        self.__parse(self._bytes_p)

    @property
    def entryPoint(self):
        return self.ehdr.e_entry

    
    def _getImageBase(self):
        return self.phdrs[0].struct.p_vaddr - self.phdrs[0].struct.p_offset


    def _loadDefaultArch(self):
        try:
            return self.__elf_module.getArch( (EM[self.ehdr.e_machine], ELFCLASS[self.ehdr.e_ident[EI.CLASS]]),self.ehdr.e_entry)
        except:
            return None

    @property
    def executableSections(self):
        if not self.__execSections:
            self.__execSections = []
            for phdr in self.phdrs:
                if phdr.struct.p_flags & PF.EXEC > 0:
                    p_tmp = c_void_p(self._bytes_p.value + phdr.struct.p_offset)
                    self.assertFileRange(p_tmp.value)
                    self.assertFileRange(p_tmp.value+phdr.struct.p_memsz)
                    execBytes = cast(p_tmp, POINTER(c_ubyte * phdr.struct.p_memsz)).contents
                    self.__execSections.append(Section(name=str(PT[phdr.struct.p_type]), sectionbytes=execBytes, virtualAddress=phdr.struct.p_vaddr, offset=phdr.struct.p_offset))

        return self.__execSections

    @property
    def dataSections(self):
        if not self.__dataSections:
            self.__dataSections = []
            for shdr in self.shdrs:
                if shdr.struct.sh_flags & SHF.ALLOC and not (shdr.struct.sh_flags & SHF.EXECINSTR) and not(shdr.struct.sh_type & SHT.NOBITS):
                    p_tmp = c_void_p(self._bytes_p.value + shdr.struct.sh_offset)
                    self.assertFileRange(p_tmp.value)
                    self.assertFileRange(p_tmp.value + shdr.struct.sh_size)
                    dataBytes = cast(p_tmp, POINTER(c_ubyte * shdr.struct.sh_size)).contents
                    self.__dataSections.append(Section(shdr.name, dataBytes, shdr.struct.sh_addr, shdr.struct.sh_offset, shdr.struct))
        return self.__dataSections

    @property
    def codeVA(self):

        for phdr in self.phdrs:
            if phdr.struct.p_type == PT.INTERP:
                return phdr.struct.p_vaddr
        return 0

    @property
    def type(self):
        return Type.ELF

    def setASLR(self, enable):
        raise LoaderError('Not available for elf files')

    def setNX(self, enable):
        perm = PF.READ | PF.WRITE  if enable else PF.READ | PF.WRITE | PF.EXEC
        phdrs = self.phdrs

        for phdr in phdrs:
            if phdr.struct.p_type == PT.GNU_STACK:
                phdr.struct.p_flags = perm

        self.save()

    def getSection(self, name):
        for shdr in self.shdrs:
            if str(shdr.name) == name:
                p_tmp = c_void_p(self._bytes_p.value + shdr.struct.sh_offset)
                dataBytes = cast(p_tmp, POINTER(c_ubyte * shdr.struct.sh_size)).contents
                return Section(shdr.name, dataBytes, shdr.struct.sh_addr, shdr.struct.sh_offset)
        raise RopperError('No such section: %s' % name)

    def checksec(self):
        return {}

    @classmethod
    def isSupportedFile(cls, fileName):
        try:
            with open(fileName, 'rb') as f:
                return f.read(4) == b'\x7fELF'
        except BaseException as e:
            raise LoaderError(e)
