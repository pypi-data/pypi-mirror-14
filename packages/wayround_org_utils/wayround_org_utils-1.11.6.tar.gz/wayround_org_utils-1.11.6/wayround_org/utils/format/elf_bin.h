#ifndef ELF_BIN_H
#define ELF_BIN_H

PyObject *
PyObjectAddToDelQueue(PyObject ** queue, PyObject * obj);

void
PyObjectDelQueue(PyObject ** queue);

PyObject *
endianness_to_name(long in);

PyObject *
class_switch(long val);

PyObject *
PyLong_FromPyBytes(PyObject *bytes, PyObject *byteorder, PyObject *sign);

PyObject *
ReadLong(
    PyObject * data,
    PyObject * offset,
    PyObject * end,
    PyObject * endianness,
    PyObject * sign);

PyObject *
convert_virtual_to_file(PyObject *self, PyObject *args);

PyObject *
read_e_ident(PyObject *self, PyObject *args);

PyObject *
is_elf(PyObject *self, PyObject *args);

PyObject *
e_ident_bitness(PyObject *self, PyObject *args);

PyObject *
e_ident_dict_bitness(PyObject *self, PyObject *args);

PyObject *
e_ident_endianness(PyObject *self, PyObject *args);

PyObject *
e_ident_dict_endianness(PyObject *self, PyObject *args);

PyObject *
e_ident_to_dict(PyObject *self, PyObject *args);

PyObject *
read_elf_ehdr_x(PyObject *self, PyObject *args);

PyObject *
read_elf_ehdr(PyObject *self, PyObject *args);

PyObject *
elf32_ehdr_to_dict(PyObject *self, PyObject *args);

PyObject *
elf64_ehdr_to_dict(PyObject *self, PyObject *args);

PyObject *
elf_ehdr_to_dict(PyObject *self, PyObject *args);

PyObject *
read_elf_shdr_x(PyObject *self, PyObject *args);

PyObject *
read_elf_shdr(PyObject *self, PyObject *args);

PyObject *
shdr32_to_dict(PyObject *self, PyObject *args);

PyObject *
shdr64_to_dict(PyObject *self, PyObject *args);

PyObject *
read_elf_section_header_table(PyObject *self, PyObject *args);

PyObject *
read_elf_phdr_x(PyObject *self, PyObject *args);

PyObject *
read_elf_phdr(PyObject *self, PyObject *args);

PyObject *
phdr32_to_dict(PyObject *self, PyObject *args);

PyObject *
phdr64_to_dict(PyObject *self, PyObject *args);

PyObject *
read_elf_program_header_table(PyObject *self, PyObject *args);

PyObject *
get_ehdr_string_table_slice(PyObject *self, PyObject *args);

PyObject *
get_dyn_string_table_slice(PyObject *self, PyObject *args);

PyObject *
read_elf_section_header_table_names(PyObject *self, PyObject *args);

PyObject *
read_dynamic_section(PyObject *self, PyObject *args);

PyObject *
get_dynamic_libs_names(PyObject *self, PyObject *args);

PyMODINIT_FUNC
PyInit_elf_bin(void);

#endif
