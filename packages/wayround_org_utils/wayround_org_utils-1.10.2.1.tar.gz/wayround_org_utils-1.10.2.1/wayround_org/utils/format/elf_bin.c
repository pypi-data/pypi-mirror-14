#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <elf.h>

#include "Python.h"
#include "elf_bin.h"

#define member_size(type, member) sizeof(((type *)0)->member)

const char *e_indent_names[] =
    {
        "e_i_s_mag0",
        "e_i_s_mag1",
        "e_i_s_mag2",
        "e_i_s_mag3",
        "e_i_s_class",
        "e_i_s_data",
        "e_i_s_version",
        "e_i_s_osabi",
        "e_i_s_abiversion",
        "e_i_s_pad",
        "e_i_s_r10",
        "e_i_s_r11",
        "e_i_s_r12",
        "e_i_s_r13",
        "e_i_s_r14",
        "e_i_s_r15",
        NULL };

PyObject *
PyObjectAddToDelQueue(PyObject ** queue, PyObject * obj)
{
    if (obj != NULL)
    {
        if (*queue == NULL)
        {
            *queue = PyList_New(0);
        }

        PyList_Append(*queue, obj);
    }

    return obj;
}

void
PyObjectDelQueue(PyObject ** queue)
{
    PyObject * t;

    if (*queue != NULL)
    {
        while (PySequence_Length(*queue) != 0)
        {
            t = PyList_GetItem(*queue, 0);
            PySequence_DelItem(*queue, 0);

            Py_XDECREF(t);
        }

        Py_XDECREF(*queue);

        *queue = NULL;
    }

    return;
}

PyObject *
endianness_to_name(long in)
{
    PyObject * ret = NULL;

    switch (in)
    {
        case ELFDATANONE:
        {
            PyErr_SetString(PyExc_ValueError, "EI_DATA is ELFDATANONE");
            ret = NULL;
            break;
        }
        case ELFDATA2LSB:
        {
            ret = PyUnicode_FromString("little");
            break;
        }
        case ELFDATA2MSB:
        {
            ret = PyUnicode_FromString("big");
            break;
        }
        default:
        {
            PyErr_SetString(PyExc_ValueError, "EI_DATA value is unknown");
            ret = NULL;
            break;
        }
    }

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
class_switch(long val)
{
    PyObject * ret = NULL;

//    printf("val: %ld\n", val);

    switch (val)
    {
        case ELFCLASS32:
        {
            ret = PyLong_FromLong(32);
            break;
        }
        case ELFCLASS64:
        {
            ret = PyLong_FromLong(64);
            break;
        }
        default:
        {
            PyErr_SetString(
                PyExc_ValueError,
                "Wrong parameter value to function class_switch");
            ret = NULL;
            break;
        }
    }

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

/*
 * Convert PyBytes to PyLong
 */
PyObject *
PyLong_FromPyBytes(PyObject *bytes, PyObject *byteorder, PyObject *sign)
{

    PyObject * builtins = NULL;
    PyObject * from_bytes = NULL;
    PyObject * ret = NULL;

    PyObject * args2 = NULL;
    PyObject * kwargs2 = NULL;
    PyObject * ret2 = NULL;

    PyObject * q = NULL;

    builtins = PyImport_ImportModule("builtins");

    PyObjectAddToDelQueue(&q, builtins);

    if (builtins == NULL)
    {
        ret = NULL;
    }
    else
    {
        from_bytes = PyObject_GetAttr(
            builtins,
            PyObjectAddToDelQueue(&q, PyUnicode_FromString("int")));

        PyObjectAddToDelQueue(&q, from_bytes);

        if (from_bytes == NULL)
        {
            ret = NULL;
        }
        else
        {

            from_bytes = PyObject_GetAttr(
                from_bytes,
                PyUnicode_FromString("from_bytes"));

            PyObjectAddToDelQueue(&q, from_bytes);

            if (from_bytes == NULL)
            {
                ret = NULL;
            }
            else
            {

                kwargs2 = PyDict_New();

                PyObjectAddToDelQueue(&q, kwargs2);

                PyDict_SetItem(
                    kwargs2,
                    PyObjectAddToDelQueue(
                        &q,
                        PyUnicode_FromString("byteorder")),
                    byteorder);
                PyDict_SetItem(
                    kwargs2,
                    PyObjectAddToDelQueue(&q, PyUnicode_FromString("signed")),
                    sign);

                args2 = Py_BuildValue("(O)", bytes);

                PyObjectAddToDelQueue(&q, args2);

                ret2 = PyObject_Call(from_bytes, args2, kwargs2);

                if (ret2 == NULL)
                {
                    ret = NULL;
                }
                else
                {
                    ret = ret2;
                }

            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
ReadLong(
    PyObject * data,
    PyObject * offset,
    PyObject * end,
    PyObject * endianness,
    PyObject * sign)
{
    PyObject * ret = NULL;

    PyObject * data_length = NULL;
    PyObject * ts = NULL;

    PyObject * q = NULL;

    if (PySequence_Check(data) == 0 || PyLong_Check(offset) == 0
        || PyLong_Check(end) == 0 || PyUnicode_Check(endianness) == 0
        || PyBool_Check(sign) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters in function ReadLong");

        ret = NULL;
    }
    else
    {
        data_length = PyLong_FromSsize_t(PySequence_Length(data));

        PyObjectAddToDelQueue(&q, data_length);

        if (PyObject_RichCompareBool(offset, data_length, Py_GT) == 1)
        {
            PyErr_SetString(
                PyExc_IndexError,
                "Wrong parameter `offset' in function ReadLong");

            ret = NULL;
        }
        else
        {
            if ((PyObject_RichCompareBool(end, offset, Py_LT) == 1)
                || (PyObject_RichCompareBool(end, data_length, Py_GT) == 1))
            {
                PyErr_SetString(
                    PyExc_IndexError,
                    "Wrong parameter `end' in function ReadLong");

                ret = NULL;
            }
            else
            {
                if ((PyObject_RichCompareBool(
                    endianness,
                    PyObjectAddToDelQueue(&q, PyUnicode_FromString("little")),
                    Py_NE) == 1)
                    && (PyObject_RichCompareBool(
                        endianness,
                        PyObjectAddToDelQueue(&q, PyUnicode_FromString("big")),
                        Py_NE) == 1))
                {
                    PyErr_SetString(
                        PyExc_ValueError,
                        "Wrong parameter `endianness' in function ReadLong");
                    ret = NULL;
                }
                else
                {
                    ts = PySequence_GetSlice(
                        data,
                        PyLong_AsSsize_t(offset),
                        PyLong_AsSsize_t(end));

                    PyObjectAddToDelQueue(&q, ts);

                    ret = PyLong_FromPyBytes(ts, endianness, sign);
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

/*
 * Converts virtual address to offset
 */
PyObject *
convert_virtual_to_file(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * program_section_table = NULL;
    PyObject * value = NULL;
    PyObject * byteorder = NULL;

    PyObject * item = NULL;

    PyObject * p_vaddr = NULL;

    PyObject * shift = NULL;

    PyObject * q = NULL;

    unsigned long long i = 0;
    unsigned long long program_section_table_size = 0;

    if (PyArg_ParseTuple(
        args,
        "OOO",
        &program_section_table,
        &value,
        &byteorder) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function convert_virtual_to_file");

        ret = NULL;
    }
    else
    {

        if (PySequence_Check(program_section_table) != 1
            || PyLong_Check(value) != 1 || PyUnicode_Check(byteorder) != 1)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter type to function read_e_ident");

            ret = NULL;
        }
        else
        {

            program_section_table_size = PySequence_Length(
                program_section_table);

            for (i = 0; i != program_section_table_size; i++)
            {
                item = PyList_GetItem(program_section_table, i);

                Py_XINCREF(item);

                PyObjectAddToDelQueue(&q, item);

                if (item == NULL)
                {
                    ret = NULL;
                }
                else
                {

                    p_vaddr = PyLong_FromPyBytes(
                        PyDict_GetItem(
                            item,
                            PyObjectAddToDelQueue(
                                &q,
                                PyUnicode_FromString("p_vaddr"))),
                        byteorder,
                        Py_False);

                    PyObjectAddToDelQueue(&q, p_vaddr);

                    if (p_vaddr == NULL)
                    {
                        ret = NULL;
                    }
                    else
                    {

                        if ((PyObject_RichCompareBool(value, p_vaddr, Py_GE)
                            == 1)
                            && (PyObject_RichCompareBool(
                                value,
                                (PyObjectAddToDelQueue(
                                    &q,
                                    PyNumber_Add(
                                        p_vaddr,
                                        PyObjectAddToDelQueue(
                                            &q,
                                            PyLong_FromPyBytes(
                                                PyDict_GetItem(
                                                    item,
                                                    PyObjectAddToDelQueue(
                                                        &q,
                                                        PyUnicode_FromString(
                                                            "p_memsz"))),
                                                byteorder,
                                                Py_False))))),
                                Py_LT)))

                        {
                            shift = PyNumber_Add(
                                PyObjectAddToDelQueue(
                                    &q,
                                    PyNumber_Subtract(value, p_vaddr)),
                                PyObjectAddToDelQueue(
                                    &q,
                                    PyLong_FromPyBytes(
                                        PyDict_GetItem(
                                            item,
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyUnicode_FromString(
                                                    "p_offset"))),
                                        byteorder,
                                        Py_False)));

                            ret = shift;
                            break;
                        }
                    }
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

/*
 * Reads e_ident from sequence parameter
 */
PyObject *
read_e_ident(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * bytes_data = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "O", &bytes_data) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_e_ident");

        ret = NULL;
    }
    else
    {

        if (PySequence_Check(bytes_data) != 1)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter type to function read_e_ident");

            ret = NULL;
        }
        else
        {
            if (PySequence_Length(bytes_data) < EI_NIDENT)
            {
                ret = Py_None;
                Py_XINCREF(ret);
            }
            else
            {
                ret = PySequence_GetSlice(bytes_data, 0, EI_NIDENT);
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
is_elf(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * bytes_data = NULL;
    PyObject * bytes_data_slice = NULL;
    char * bytes_data_c = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "O", &bytes_data) == 0)
    {
        PyErr_SetString(PyExc_TypeError, "Wrong parameters to function is_elf");

        ret = NULL;
    }
    else
    {

        ret = Py_False;

        bytes_data_slice = PySequence_GetSlice(bytes_data, 0, SELFMAG);
        PyObjectAddToDelQueue(&q, bytes_data_slice);

        if (PySequence_Length(bytes_data_slice) < SELFMAG)
        {
            ret = Py_False;
            Py_XINCREF(ret);
        }
        else
        {
            bytes_data_c = PyBytes_AsString(bytes_data_slice);

            if (bytes_data_c[0] != ELFMAG0 || bytes_data_c[1] != ELFMAG1
                || bytes_data_c[2] != ELFMAG2 || bytes_data_c[3] != ELFMAG3)
            {
                ret = Py_False;
                Py_XINCREF(ret);
            }
            else
            {
                ret = Py_True;
                Py_XINCREF(ret);
            }
        }

    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
e_ident_bitness(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;

    PyObject * e_ident = NULL;

    PyObject * q = NULL;

    unsigned char * t;

    if (PyArg_ParseTuple(args, "O", &e_ident) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameter to function e_ident_bitness");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(e_ident) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter to function e_ident_bitness");

            ret = NULL;
        }
        else
        {
            if (PySequence_Length(e_ident) != EI_NIDENT)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong length of e_ident in e_ident_bitness");
                ret = NULL;
            }
            else
            {
                t = (unsigned char *) (PyBytes_AsString(e_ident));

                ret = class_switch(t[EI_CLASS]);
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
e_ident_dict_bitness(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;

    PyObject * e_ident_dict = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "O", &e_ident_dict) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameter to function e_ident_dict_bitness");
        ret = NULL;
    }
    else
    {
        if (PyDict_Check(e_ident_dict) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter to function e_ident_dict_bitness");
            ret = NULL;
        }
        else
        {

            ret = class_switch(
                PyLong_AsLong(
                    PyDict_GetItem(
                        e_ident_dict,
                        PyObjectAddToDelQueue(
                            &q,
                            PyUnicode_FromString("e_i_s_class")))));
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
e_ident_endianness(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;

    PyObject * e_ident = NULL;

    PyObject * q = NULL;

    unsigned char * t;

    if (PyArg_ParseTuple(args, "O", &e_ident) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameter to function e_ident_endianness");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(e_ident) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter to function e_ident_endianness");

            ret = NULL;
        }
        else
        {
            if (PySequence_Length(e_ident) != EI_NIDENT)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong length of e_ident in e_ident_endianness");
                ret = NULL;
            }
            else
            {
                t = (unsigned char *) PyBytes_AsString(e_ident);

                ret = endianness_to_name(t[EI_DATA]);
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
e_ident_dict_endianness(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;

    PyObject * e_ident_dict = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "O", &e_ident_dict) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameter to function e_ident_dict_endianness");
        ret = NULL;
    }
    else
    {
        if (PyDict_Check(e_ident_dict) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter to function e_ident_dict_endianness");
            ret = NULL;
        }
        else
        {

            ret = endianness_to_name(
                PyLong_AsLong(
                    PyDict_GetItem(
                        e_ident_dict,
                        PyObjectAddToDelQueue(
                            &q,
                            PyUnicode_FromString("e_i_s_data")))));
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
e_ident_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * e_ident_bytes = NULL;

    PyObject * q = NULL;

    unsigned char * t;

    int i = 0;

    e_ident_bytes = read_e_ident(self, args);

    PyObjectAddToDelQueue(&q, e_ident_bytes);

    if (PySequence_Check(e_ident_bytes) == 0)
    {
        PyErr_SetString(
            PyExc_TypeError,
            "Wrong parameter to function e_ident_to_dict");
        ret = NULL;
    }
    else
    {

        if (PySequence_Length(e_ident_bytes) != EI_NIDENT)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong input data sequence length in function e_ident_to_dict");
            ret = NULL;
        }
        else
        {
            t = (unsigned char *) PyBytes_AsString(e_ident_bytes);

            ret = PyDict_New();

            i = 0;
            while (1)
            {
                if (e_indent_names[i] == NULL)
                {
                    break;
                }

                PyDict_SetItem(
                    ret,
                    PyObjectAddToDelQueue(
                        &q,
                        PyUnicode_FromString(e_indent_names[i])),
                    PyObjectAddToDelQueue(&q, PyLong_FromUnsignedLong(t[i])));

                i++;
            }

        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
read_elf_ehdr_x(PyObject *self, PyObject *args)
{

    PyObject * ret = Py_None;

    PyObject * data = NULL;
    PyObject * index = NULL;
    PyObject * x = NULL;

    PyObject * q = NULL;

    long elf_x_ehdr_i_size = 0;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &x) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_elf_ehdr_x");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data) == 0 || PyLong_Check(index) == 0
            || PyLong_Check(x) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function read_elf_ehdr_x");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsLongLong(index) < 0
                || (PyLong_AsLongLong(x) != 32 && PyLong_AsLongLong(x) != 64))
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function read_elf_ehdr_x");
                ret = NULL;
            }
            else
            {
                switch (PyLong_AsLong(x))
                {
                    case 32:
                    {
                        elf_x_ehdr_i_size = sizeof(Elf32_Ehdr);
                        break;
                    }
                    case 64:
                    {
                        elf_x_ehdr_i_size = sizeof(Elf64_Ehdr);
                        break;
                    }
                    default:
                        PyErr_SetString(
                            PyExc_ValueError,
                            "Wrong bitness number in function read_elf_ehdr_x");
                        ret = NULL;
                        elf_x_ehdr_i_size = 0;
                        break;
                }

                if (elf_x_ehdr_i_size != 0)
                {
                    ret = PySequence_GetSlice(
                        data,
                        PyLong_AsSize_t(index),
                        PyLong_AsSize_t(
                            PyObjectAddToDelQueue(
                                &q,
                                PyLong_FromLong(elf_x_ehdr_i_size))));
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
read_elf_ehdr(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;

    PyObject * data = NULL;
    PyObject * index = NULL;
    PyObject * e_ident = NULL;

    PyObject * args2 = NULL;
    PyObject * x = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &e_ident) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_elf_ehdr");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data) == 0 || PyLong_Check(index) == 0
            || PyDict_Check(e_ident) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function read_elf_ehdr");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsLongLong(index) < 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function read_elf_ehdr");
                ret = NULL;
            }
            else
            {

                args2 = Py_BuildValue("(O)", e_ident);

                PyObjectAddToDelQueue(&q, args2);

                x = e_ident_dict_bitness(self, args2);

                PyObjectAddToDelQueue(&q, x);

                if (x == NULL)
                {
                    ret = NULL;
                }
                else
                {
                    args2 = Py_BuildValue("(OOO)", data, index, x);

                    PyObjectAddToDelQueue(&q, args2);

                    ret = read_elf_ehdr_x(self, args2);
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyObjectAddToDelQueue(&q,PyUnicode_FromString(#v)), \
    PyObjectAddToDelQueue(&q,PySequence_GetSlice( \
        data2, \
        PyLong_AsLong(index)+offsetof(Elf32_Ehdr, v), \
        PyLong_AsLong(index)+offsetof(Elf32_Ehdr, v)+t)));

PyObject *
elf32_ehdr_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data = NULL;
    PyObject * index = NULL;

    PyObject * data2 = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "OO", &data, &index) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function elf32_ehdr_to_dict");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data) == 0 || PyLong_Check(index) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function elf32_ehdr_to_dict");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsLongLong(index) < 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function elf32_ehdr_to_dict");
                ret = NULL;
            }
            else
            {

                data2 = PySequence_GetSlice(
                    data,
                    PyLong_AsLong(index),
                    PyLong_AsLong(index) + sizeof(Elf32_Ehdr));

                PyObjectAddToDelQueue(&q, data2);

                ret = PyDict_New();

                PyDict_SetItem(
                    ret,
                    PyObjectAddToDelQueue(&q, PyUnicode_FromString("e_ident")),
                    PyObjectAddToDelQueue(
                        &q,
                        PySequence_GetSlice(
                            data2,
                            offsetof(Elf32_Ehdr, e_ident),
                            offsetof(Elf32_Ehdr, e_ident) + EI_NIDENT)));

                PYDICT_SETITEM(e_type, member_size(Elf32_Ehdr, e_type))
                PYDICT_SETITEM(e_machine, member_size(Elf32_Ehdr, e_machine))
                PYDICT_SETITEM(e_version, member_size(Elf32_Ehdr, e_version))
                PYDICT_SETITEM(e_entry, member_size(Elf32_Ehdr, e_entry))
                PYDICT_SETITEM(e_phoff, member_size(Elf32_Ehdr, e_phoff))
                PYDICT_SETITEM(e_shoff, member_size(Elf32_Ehdr, e_shoff))
                PYDICT_SETITEM(e_flags, member_size(Elf32_Ehdr, e_flags))
                PYDICT_SETITEM(e_ehsize, member_size(Elf32_Ehdr, e_ehsize))
                PYDICT_SETITEM(
                    e_phentsize,
                    member_size(Elf32_Ehdr, e_phentsize))
                PYDICT_SETITEM(e_phnum, member_size(Elf32_Ehdr, e_phnum))
                PYDICT_SETITEM(
                    e_shentsize,
                    member_size(Elf32_Ehdr, e_shentsize))
                PYDICT_SETITEM(e_shnum, member_size(Elf32_Ehdr, e_shnum))
                PYDICT_SETITEM(e_shstrndx, member_size(Elf32_Ehdr, e_shstrndx))
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

#undef PYDICT_SETITEM

#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyObjectAddToDelQueue(&q,PyUnicode_FromString(#v)), \
    PyObjectAddToDelQueue(&q,PySequence_GetSlice( \
        data2, \
        PyLong_AsLong(index)+offsetof(Elf64_Ehdr, v), \
        PyLong_AsLong(index)+offsetof(Elf64_Ehdr, v)+t)));

PyObject *
elf64_ehdr_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data = NULL;
    PyObject * index = NULL;

    PyObject * data2 = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "OO", &data, &index) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function elf64_ehdr_to_dict");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data) == 0 || PyLong_Check(index) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function elf64_ehdr_to_dict");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsLongLong(index) < 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function elf64_ehdr_to_dict");
                ret = NULL;
            }
            else
            {

                data2 = PySequence_GetSlice(
                    data,
                    PyLong_AsLong(index),
                    PyLong_AsLong(index) + sizeof(Elf64_Ehdr));

                PyObjectAddToDelQueue(&q, data2);

                ret = PyDict_New();

                PyDict_SetItem(
                    ret,
                    PyObjectAddToDelQueue(&q, PyUnicode_FromString("e_ident")),
                    PyObjectAddToDelQueue(
                        &q,
                        PySequence_GetSlice(
                            data2,
                            offsetof(Elf64_Ehdr, e_ident),
                            offsetof(Elf64_Ehdr, e_ident) + EI_NIDENT)));

                PYDICT_SETITEM(e_type, member_size(Elf64_Ehdr, e_type))
                PYDICT_SETITEM(e_machine, member_size(Elf64_Ehdr, e_machine))
                PYDICT_SETITEM(e_version, member_size(Elf64_Ehdr, e_version))
                PYDICT_SETITEM(e_entry, member_size(Elf64_Ehdr, e_entry))
                PYDICT_SETITEM(e_phoff, member_size(Elf64_Ehdr, e_phoff))
                PYDICT_SETITEM(e_shoff, member_size(Elf64_Ehdr, e_shoff))
                PYDICT_SETITEM(e_flags, member_size(Elf64_Ehdr, e_flags))
                PYDICT_SETITEM(e_ehsize, member_size(Elf64_Ehdr, e_ehsize))
                PYDICT_SETITEM(
                    e_phentsize,
                    member_size(Elf64_Ehdr, e_phentsize))
                PYDICT_SETITEM(e_phnum, member_size(Elf64_Ehdr, e_phnum))
                PYDICT_SETITEM(
                    e_shentsize,
                    member_size(Elf64_Ehdr, e_shentsize))
                PYDICT_SETITEM(e_shnum, member_size(Elf64_Ehdr, e_shnum))
                PYDICT_SETITEM(e_shstrndx, member_size(Elf64_Ehdr, e_shstrndx))
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

#undef PYDICT_SETITEM

PyObject *
elf_ehdr_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data = NULL;
    PyObject * index = NULL;
    PyObject * e_ident = NULL;

    PyObject * args2 = NULL;
    PyObject * x = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &e_ident) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function elf_ehdr_to_dict");

        ret = NULL;
    }
    else
    {

        if (PySequence_Check(data) == 0 || PyLong_Check(index) == 0
            || PyDict_Check(e_ident) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function elf_ehdr_to_dict");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsLongLong(index) < 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function elf_ehdr_to_dict");
                ret = NULL;
            }
            else
            {
                args2 = Py_BuildValue("(O)", e_ident);

                PyObjectAddToDelQueue(&q, args2);

                x = e_ident_dict_bitness(self, args2);

                PyObjectAddToDelQueue(&q, x);

                if (x == NULL)
                {
                    ret = NULL;
                }
                else
                {

                    args2 = Py_BuildValue("OO", data, index);

                    PyObjectAddToDelQueue(&q, args2);

                    switch (PyLong_AsLong(x))
                    {
                        case 32:
                        {
                            ret = elf32_ehdr_to_dict(self, args2);
                            break;
                        }
                        case 64:
                        {
                            ret = elf64_ehdr_to_dict(self, args2);
                            break;
                        }
                        default:
                            PyErr_SetString(
                                PyExc_ValueError,
                                "Wrong bitness value in function elf_ehdr_to_dict");
                            ret = NULL;
                            break;
                    }
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
read_elf_shdr_x(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data = NULL;
    PyObject * index = NULL;
    PyObject * x = NULL;

    PyObject * q = NULL;

    long elf_x_shdr_i_size = 0;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &x) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_elf_shdr_x");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data) == 0 || PyLong_Check(index) == 0
            || PyLong_Check(x) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function read_elf_shdr_x");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsLongLong(index) < 0
                || (PyLong_AsLongLong(x) != 32 && PyLong_AsLongLong(x) != 64))
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function read_elf_shdr_x");
                ret = NULL;
            }
            else
            {

                switch (PyLong_AsLong(x))
                {
                    case 32:
                    {
                        elf_x_shdr_i_size = sizeof(Elf32_Shdr);
                        break;
                    }
                    case 64:
                    {
                        elf_x_shdr_i_size = sizeof(Elf64_Shdr);
                        break;
                    }
                    default:
                        PyErr_SetString(
                            PyExc_ValueError,
                            "Wrong bitness value in function read_elf_shdr_x");
                        ret = NULL;
                        elf_x_shdr_i_size = 0;
                        break;
                }

                if (elf_x_shdr_i_size != 0)
                {
                    ret = PySequence_GetSlice(
                        data,
                        PyLong_AsSize_t(index),
                        PyLong_AsSize_t(
                            PyObjectAddToDelQueue(
                                &q,
                                PyLong_FromLong(elf_x_shdr_i_size))));
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
read_elf_shdr(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;

    PyObject * data = NULL;
    PyObject * index = NULL;
    PyObject * e_ident = NULL;

    PyObject * args2 = NULL;
    PyObject * x = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &e_ident) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_elf_shdr");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data) == 0 || PyLong_Check(index) == 0
            || PyDict_Check(e_ident) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function read_elf_shdr");

            ret = NULL;
        }
        else
        {
            if (PyLong_AsLongLong(index) < 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function read_elf_shdr");
                ret = NULL;
            }
            else
            {
                args2 = Py_BuildValue("(O)", e_ident);

                PyObjectAddToDelQueue(&q, args2);

                x = e_ident_dict_bitness(self, args2);

                PyObjectAddToDelQueue(&q, x);

                if (x == NULL)
                {
                    ret = NULL;
                }
                else
                {
                    args2 = Py_BuildValue("(OOO)", data, index, x);

                    PyObjectAddToDelQueue(&q, args2);

                    ret = read_elf_shdr_x(self, args2);
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyObjectAddToDelQueue(&q,PyUnicode_FromString(#v)), \
    PyObjectAddToDelQueue(&q,PySequence_GetSlice( \
        data_seq, \
        PyLong_AsLong(index)+offsetof(Elf32_Shdr, v), \
        PyLong_AsLong(index)+offsetof(Elf32_Shdr, v)+t)));

PyObject *
shdr32_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data_seq = NULL;
    PyObject * index = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "OO", &data_seq, &index) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function shdr32_to_dict");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data_seq) == 0 || PyLong_Check(index) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function shdr32_to_dict");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsUnsignedLongLong(index) < 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function shdr32_to_dict");
                ret = NULL;
            }
            else
            {
                ret = PyDict_New();

                PYDICT_SETITEM(sh_name, member_size(Elf32_Shdr, sh_name))
                PYDICT_SETITEM(sh_type, member_size(Elf32_Shdr, sh_type))
                PYDICT_SETITEM(sh_flags, member_size(Elf32_Shdr, sh_flags))
                PYDICT_SETITEM(sh_addr, member_size(Elf32_Shdr, sh_addr))
                PYDICT_SETITEM(sh_offset, member_size(Elf32_Shdr, sh_offset))
                PYDICT_SETITEM(sh_size, member_size(Elf32_Shdr, sh_size))
                PYDICT_SETITEM(sh_link, member_size(Elf32_Shdr, sh_link))
                PYDICT_SETITEM(sh_info, member_size(Elf32_Shdr, sh_info))
                PYDICT_SETITEM(
                    sh_addralign,
                    member_size(Elf32_Shdr, sh_addralign))
                PYDICT_SETITEM(sh_entsize, member_size(Elf32_Shdr, sh_entsize))
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

#undef PYDICT_SETITEM

#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyObjectAddToDelQueue(&q,PyUnicode_FromString(#v)), \
    PyObjectAddToDelQueue(&q,PySequence_GetSlice( \
        data_seq, \
        PyLong_AsLong(index)+offsetof(Elf64_Shdr, v), \
        PyLong_AsLong(index)+offsetof(Elf64_Shdr, v)+t)));

PyObject *
shdr64_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data_seq = NULL;
    PyObject * index = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "OO", &data_seq, &index) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function shdr64_to_dict");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data_seq) == 0 || PyLong_Check(index) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function shdr64_to_dict");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsUnsignedLongLong(index) < 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function shdr64_to_dict");
                ret = NULL;
            }
            else
            {
                ret = PyDict_New();

                PYDICT_SETITEM(sh_name, member_size(Elf64_Shdr, sh_name))
                PYDICT_SETITEM(sh_type, member_size(Elf64_Shdr, sh_type))
                PYDICT_SETITEM(sh_flags, member_size(Elf64_Shdr, sh_flags))
                PYDICT_SETITEM(sh_addr, member_size(Elf64_Shdr, sh_addr))
                PYDICT_SETITEM(sh_offset, member_size(Elf64_Shdr, sh_offset))
                PYDICT_SETITEM(sh_size, member_size(Elf64_Shdr, sh_size))
                PYDICT_SETITEM(sh_link, member_size(Elf64_Shdr, sh_link))
                PYDICT_SETITEM(sh_info, member_size(Elf64_Shdr, sh_info))
                PYDICT_SETITEM(
                    sh_addralign,
                    member_size(Elf64_Shdr, sh_addralign))
                PYDICT_SETITEM(sh_entsize, member_size(Elf64_Shdr, sh_entsize))
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

#undef PYDICT_SETITEM

PyObject *
read_elf_section_header_table(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data_seq = NULL;
    PyObject * e_ident_dict = NULL;
    PyObject * ehdr_dict = NULL;

    PyObject * args2 = NULL;
    PyObject * bits = NULL;

    PyObject * sheader_size = NULL;
    PyObject * sheaders_count = NULL;

    PyObject * td = NULL;

    PyObject * index = NULL;
    PyObject * offset = NULL;

    PyObject * endianness = NULL;

    PyObject * q = NULL;

    unsigned long long i = 0;

    if (PyArg_ParseTuple(args, "OOO", &data_seq, &e_ident_dict, &ehdr_dict)
        == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_elf_section_header_table");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data_seq) == 0 || PyDict_Check(e_ident_dict) == 0
            || PyDict_Check(ehdr_dict) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function read_elf_section_header_table");

            ret = NULL;
        }
        else
        {

            args2 = Py_BuildValue("(O)", e_ident_dict);

            PyObjectAddToDelQueue(&q, args2);

            bits = e_ident_dict_bitness(self, args2);

            PyObjectAddToDelQueue(&q, bits);

            if (bits == NULL)
            {
                ret = NULL;
            }
            else
            {

                endianness = endianness_to_name(
                    PyLong_AsLong(
                        PyDict_GetItem(
                            e_ident_dict,
                            PyObjectAddToDelQueue(
                                &q,
                                PyUnicode_FromString("e_i_s_data")))));

                PyObjectAddToDelQueue(&q, endianness);

                if (endianness == NULL)
                {
                    ret = NULL;
                }
                else
                {
                    sheader_size = PyLong_FromPyBytes(
                        PyDict_GetItem(
                            ehdr_dict,
                            PyObjectAddToDelQueue(
                                &q,
                                PyUnicode_FromString("e_shentsize"))),
                        endianness,
                        Py_False);

                    PyObjectAddToDelQueue(&q, sheader_size);

                    offset = PyLong_FromPyBytes(
                        PyDict_GetItem(
                            ehdr_dict,
                            PyObjectAddToDelQueue(
                                &q,
                                PyUnicode_FromString("e_shoff"))),
                        endianness,
                        Py_False);

                    PyObjectAddToDelQueue(&q, offset);

                    sheaders_count = PyLong_FromPyBytes(
                        PyDict_GetItem(
                            ehdr_dict,
                            PyObjectAddToDelQueue(
                                &q,
                                PyUnicode_FromString("e_shnum"))),
                        endianness,
                        Py_False);

                    PyObjectAddToDelQueue(&q, sheaders_count);

                    ret = PyList_New(0);

                    for (i = 0; i != PyLong_AsLong(sheaders_count); i++)
                    {
                        index = PyObjectAddToDelQueue(
                            &q,
                            PyNumber_Add(
                                offset,
                                PyObjectAddToDelQueue(
                                    &q,
                                    PyNumber_Multiply(
                                        sheader_size,
                                        PyObjectAddToDelQueue(
                                            &q,
                                            PyLong_FromUnsignedLongLong(i))))));

                        args2 = Py_BuildValue("OO", data_seq, index);

                        PyObjectAddToDelQueue(&q, args2);

                        switch (PyLong_AsLong(bits))
                        {
                            case 32:
                            {
                                td = shdr32_to_dict(self, args2);
                                break;
                            }
                            case 64:
                            {
                                td = shdr64_to_dict(self, args2);
                                break;
                            }
                            default:
                                PyErr_SetString(
                                    PyExc_ValueError,
                                    "Wrong bitness in function read_elf_section_header_table");

                                ret = NULL;
                        }

                        PyObjectAddToDelQueue(&q, td);

                        if (td == NULL)
                        {
                            ret = NULL;
                        }

                        if (td == NULL)
                        {
                            break;
                        }

                        if (td != NULL)
                        {
                            PyList_Append(ret, td);
                        }
                    }
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
read_elf_phdr_x(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;

    PyObject * data = NULL;
    PyObject * index = NULL;

    PyObject * x = NULL;

    PyObject * q = NULL;

    unsigned long long elf_x_phdr_i_size = 0;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &x) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_elf_phdr_x");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data) == 0 || PyLong_Check(index) == 0
            || PyLong_Check(x) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function read_elf_phdr_x");

            ret = NULL;
        }
        else
        {

            if ((PyObject_RichCompareBool(
                index,
                PyObjectAddToDelQueue(&q, PyLong_FromLong(0)),
                Py_LT) == 1)
                || (((PyObject_RichCompareBool(
                    x,
                    PyObjectAddToDelQueue(&q, PyLong_FromLong(32)),
                    Py_NE)) == 1)
                    && ((PyObject_RichCompareBool(
                        x,
                        PyObjectAddToDelQueue(&q, PyLong_FromLong(64)),
                        Py_NE)) == 1)))
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function read_elf_phdr_x");
                ret = NULL;
            }
            else
            {
                switch (PyLong_AsLong(x))
                {
                    case 32:
                    {
                        elf_x_phdr_i_size = sizeof(Elf32_Phdr);
                        break;
                    }
                    case 64:
                    {
                        elf_x_phdr_i_size = sizeof(Elf64_Phdr);
                        break;
                    }
                }

                if (PyLong_Check(ret) == 0)
                {
                    ret = PySequence_GetSlice(
                        data,
                        PyLong_AsSize_t(index),
                        PyLong_AsSize_t(
                            PyObjectAddToDelQueue(
                                &q,
                                PyLong_FromLong(elf_x_phdr_i_size))));
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
read_elf_phdr(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;

    PyObject * data = NULL;
    PyObject * index = NULL;
    PyObject * e_ident = NULL;

    PyObject * args2 = NULL;
    PyObject * x = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &e_ident) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_elf_phdr");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data) == 0 || PyLong_Check(index) == 0
            || PyDict_Check(e_ident) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function read_elf_phdr");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsLongLong(index) < 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function read_elf_phdr");
                ret = NULL;
            }
            else
            {
                args2 = Py_BuildValue("(O)", e_ident);

                PyObjectAddToDelQueue(&q, args2);

                x = e_ident_dict_bitness(self, args2);

                PyObjectAddToDelQueue(&q, x);

                if (x == NULL)
                {
                    ret = NULL;
                }
                else
                {
                    args2 = Py_BuildValue("(OOO)", data, index, x);

                    PyObjectAddToDelQueue(&q, args2);

                    ret = read_elf_phdr_x(self, args2);
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyObjectAddToDelQueue(&q, PyUnicode_FromString(#v)), \
    PyObjectAddToDelQueue(&q, PySequence_GetSlice( \
        data_seq, \
        PyLong_AsLong(index)+offsetof(Elf32_Phdr, v), \
        PyLong_AsLong(index)+offsetof(Elf32_Phdr, v)+t)));

PyObject *
phdr32_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data_seq = NULL;
    PyObject * index = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "OO", &data_seq, &index) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function phdr32_to_dict");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data_seq) == 0 || PyLong_Check(index) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function phdr32_to_dict");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsLongLong(index) < 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function phdr32_to_dict");
                ret = NULL;
            }
            else
            {

                ret = PyDict_New();

                PYDICT_SETITEM(p_type, member_size(Elf32_Phdr, p_type))
                PYDICT_SETITEM(p_offset, member_size(Elf32_Phdr, p_offset))
                PYDICT_SETITEM(p_vaddr, member_size(Elf32_Phdr, p_vaddr))
                PYDICT_SETITEM(p_paddr, member_size(Elf32_Phdr, p_paddr))
                PYDICT_SETITEM(p_filesz, member_size(Elf32_Phdr, p_filesz))
                PYDICT_SETITEM(p_memsz, member_size(Elf32_Phdr, p_memsz))
                PYDICT_SETITEM(p_flags, member_size(Elf32_Phdr, p_flags))
                PYDICT_SETITEM(p_align, member_size(Elf32_Phdr, p_align))
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

#undef PYDICT_SETITEM

#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyObjectAddToDelQueue(&q, PyUnicode_FromString(#v)), \
    PyObjectAddToDelQueue(&q, PySequence_GetSlice( \
        data_seq, \
        PyLong_AsLong(index)+offsetof(Elf64_Phdr, v), \
        PyLong_AsLong(index)+offsetof(Elf64_Phdr, v)+t)));

PyObject *
phdr64_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data_seq = NULL;
    PyObject * index = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(args, "OO", &data_seq, &index) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function phdr64_to_dict");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data_seq) == 0 || PyLong_Check(index) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function phdr64_to_dict");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsLongLong(index) < 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function phdr64_to_dict");
                ret = NULL;
            }
            else
            {

                ret = PyDict_New();

                PYDICT_SETITEM(p_type, member_size(Elf64_Phdr, p_type))
                PYDICT_SETITEM(p_offset, member_size(Elf64_Phdr, p_offset))
                PYDICT_SETITEM(p_vaddr, member_size(Elf64_Phdr, p_vaddr))
                PYDICT_SETITEM(p_paddr, member_size(Elf64_Phdr, p_paddr))
                PYDICT_SETITEM(p_filesz, member_size(Elf64_Phdr, p_filesz))
                PYDICT_SETITEM(p_memsz, member_size(Elf64_Phdr, p_memsz))
                PYDICT_SETITEM(p_flags, member_size(Elf64_Phdr, p_flags))
                PYDICT_SETITEM(p_align, member_size(Elf64_Phdr, p_align))
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

#undef PYDICT_SETITEM

PyObject *
read_elf_program_header_table(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;

    PyObject * data_seq = NULL;
    PyObject * e_ident_dict = NULL;
    PyObject * ehdr_dict = NULL;

    PyObject * args2 = NULL;
    PyObject * bits = NULL;

    PyObject * sheader_size = NULL;
    PyObject * sheaders_count = NULL;

    PyObject * td = NULL;

    PyObject * index = NULL;
    PyObject * offset = NULL;

    PyObject * endianness = NULL;

    PyObject * q = NULL;

    long i = 0;

    if (PyArg_ParseTuple(args, "OOO", &data_seq, &e_ident_dict, &ehdr_dict)
        == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_elf_program_header_table");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data_seq) == 0 || PyDict_Check(e_ident_dict) == 0
            || PyDict_Check(ehdr_dict) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function read_elf_program_header_table");

            ret = NULL;
        }
        else
        {
            args2 = Py_BuildValue("(O)", e_ident_dict);

            PyObjectAddToDelQueue(&q, args2);

            bits = e_ident_dict_bitness(self, args2);

            PyObjectAddToDelQueue(&q, bits);

            if (bits == NULL)
            {
                ret = NULL;
            }
            else
            {
                endianness = endianness_to_name(
                    PyLong_AsLong(
                        PyDict_GetItem(
                            e_ident_dict,
                            PyObjectAddToDelQueue(
                                &q,
                                PyUnicode_FromString("e_i_s_data")))));

                PyObjectAddToDelQueue(&q, endianness);

                if (endianness == NULL)
                {
                    ret = NULL;
                }
                else
                {

                    sheader_size = PyLong_FromPyBytes(
                        PyDict_GetItem(
                            ehdr_dict,
                            PyObjectAddToDelQueue(
                                &q,
                                PyUnicode_FromString("e_phentsize"))),
                        endianness,
                        Py_False);

                    PyObjectAddToDelQueue(&q, sheader_size);

                    offset = PyLong_FromPyBytes(
                        PyDict_GetItem(
                            ehdr_dict,
                            PyObjectAddToDelQueue(
                                &q,
                                PyUnicode_FromString("e_phoff"))),
                        endianness,
                        Py_False);

                    PyObjectAddToDelQueue(&q, offset);

                    sheaders_count = PyLong_FromPyBytes(
                        PyDict_GetItem(
                            ehdr_dict,
                            PyObjectAddToDelQueue(
                                &q,
                                PyUnicode_FromString("e_phnum"))),
                        endianness,
                        Py_False);

                    PyObjectAddToDelQueue(&q, sheaders_count);

                    ret = PyList_New(0);

                    for (i = 0; i != PyLong_AsLong(sheaders_count); i++)
                    {
                        index = PyObjectAddToDelQueue(
                            &q,
                            PyNumber_Add(
                                offset,
                                PyObjectAddToDelQueue(
                                    &q,
                                    PyNumber_Multiply(
                                        sheader_size,
                                        PyObjectAddToDelQueue(
                                            &q,
                                            PyLong_FromLong(i))))));

                        args2 = Py_BuildValue("OO", data_seq, index);

                        PyObjectAddToDelQueue(&q, args2);

                        switch (PyLong_AsLong(bits))
                        {
                            case 32:
                            {
                                td = phdr32_to_dict(self, args2);
                                break;
                            }
                            case 64:
                            {
                                td = phdr64_to_dict(self, args2);
                                break;
                            }
                            default:
                            {
                                PyErr_SetString(
                                    PyExc_ValueError,
                                    "Wrong bitness number in read_elf_program_header_table");

                                ret = NULL;
                            }
                        }

                        if (td == NULL)
                        {
                            ret = NULL;
                        }

                        if (td == NULL)
                        {
                            break;
                        }

                        if (td != NULL)
                        {
                            PyList_Append(ret, td);
                        }
                    }
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
get_ehdr_string_table_slice(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;

    PyObject * data_seq = NULL;
    PyObject * elf_section_header_table = NULL;
    PyObject * ehdr_dict = NULL;

    PyObject * string_table_record = NULL;
    PyObject * string_table_offset = NULL;
    PyObject * string_table_size = NULL;
    PyObject * header_bytes = NULL;

    PyObject * endianness = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(
        args,
        "OOOO",
        &data_seq,
        &elf_section_header_table,
        &ehdr_dict,
        &endianness) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function get_ehdr_string_table_slice");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data_seq) == 0
            || PyList_Check(elf_section_header_table) == 0
            || PyDict_Check(ehdr_dict) == 0 || PyUnicode_Check(endianness) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function get_ehdr_string_table_slice");

            ret = NULL;
        }
        else
        {

            string_table_record = PySequence_GetItem(
                elf_section_header_table,
                PyLong_AsSsize_t(
                    PyObjectAddToDelQueue(
                        &q,
                        PyLong_FromPyBytes(
                            PyDict_GetItem(
                                ehdr_dict,
                                PyObjectAddToDelQueue(
                                    &q,
                                    PyUnicode_FromString("e_shstrndx"))),
                            endianness,
                            Py_False))));

            PyObjectAddToDelQueue(&q, string_table_record);

            string_table_offset = PyLong_FromPyBytes(
                PyDict_GetItem(
                    string_table_record,
                    PyObjectAddToDelQueue(
                        &q,
                        PyUnicode_FromString("sh_offset"))),
                endianness,
                Py_False);

            PyObjectAddToDelQueue(&q, string_table_offset);

            string_table_size = PyLong_FromPyBytes(
                PyDict_GetItem(
                    string_table_record,
                    PyObjectAddToDelQueue(&q, PyUnicode_FromString("sh_size"))),
                endianness,
                Py_False);

            PyObjectAddToDelQueue(&q, string_table_size);

            header_bytes = PySequence_GetSlice(
                data_seq,
                PyLong_AsSsize_t(string_table_offset),
                PyLong_AsSsize_t(
                    PyNumber_Add(string_table_offset, string_table_size)));

            ret = header_bytes;
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
get_dyn_string_table_slice(PyObject *self, PyObject *args)
{

    PyObject * ret = NULL;
    PyObject * args2 = NULL;
    PyObject * program_table = NULL;

    PyObject * data_seq = NULL;
    PyObject * dinamics_table = NULL;

    PyObject * item = NULL;

    long dinamics_table_size = 0;
    long i = 0;

    PyObject * strtab = NULL;
    PyObject * strsz = NULL;

    PyObject * long_value = NULL;

    PyObject * byteorder = NULL;

    PyObject * q = NULL;

    if (PyArg_ParseTuple(
        args,
        "OOOO",
        &data_seq,
        &program_table,
        &dinamics_table,
        &byteorder) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function get_dyn_string_table_slice");

        ret = NULL;
    }
    else
    {

        if (PySequence_Check(data_seq) == 0 || PyList_Check(program_table) == 0
            || PyList_Check(dinamics_table) == 0
            || PyUnicode_Check(byteorder) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function get_dyn_string_table_slice");

            ret = NULL;
        }
        else
        {
            dinamics_table_size = PySequence_Length(dinamics_table);

            for (i = 0; i != dinamics_table_size; i++)
            {
                item = PyList_GetItem(dinamics_table, i);

                Py_XINCREF(item);

                PyObjectAddToDelQueue(&q, item);

                long_value = PyDict_GetItem(
                    item,
                    PyObjectAddToDelQueue(&q, PyUnicode_FromString("d_tag")));

                if (PyObject_RichCompareBool(
                    long_value,
                    PyObjectAddToDelQueue(&q, PyLong_FromLong(DT_STRTAB)),
                    Py_EQ) == 1)
                {
                    strtab = PyDict_GetItem(
                        item,
                        PyObjectAddToDelQueue(
                            &q,
                            PyUnicode_FromString("d_ptr")));
                }

                if (PyObject_RichCompareBool(
                    long_value,
                    PyObjectAddToDelQueue(&q, PyLong_FromLong(DT_STRSZ)),
                    Py_EQ) == 1)
                {
                    strsz = PyDict_GetItem(
                        item,
                        PyObjectAddToDelQueue(
                            &q,
                            PyUnicode_FromString("d_val")));
                }
            }

            if ((PyObject_RichCompareBool(strtab, 0, Py_EQ) == 1)
                || (PyObject_RichCompareBool(strsz, 0, Py_EQ) == 1))
            {
                ret = PyLong_FromLong(2);
            }
            else
            {

                args2 = Py_BuildValue("OOO", program_table, strtab, byteorder);

                PyObjectAddToDelQueue(&q, args2);

                strtab = convert_virtual_to_file(self, args2);

                PyObjectAddToDelQueue(&q, strtab);

                if (strtab == NULL)
                {
                    ret = NULL;
                }
                else
                {

                    ret = PySequence_GetSlice(
                        data_seq,
                        PyLong_AsUnsignedLongLong(strtab),
                        PyLong_AsUnsignedLongLong(
                            PyObjectAddToDelQueue(
                                &q,
                                PyNumber_Add(strtab, strsz))));
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
read_elf_section_header_table_names(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data_seq = NULL;
    PyObject * elf_section_header_table = NULL;
    PyObject * ehdr_dict = NULL;

    PyObject * section_header = NULL;
    PyObject * header_bytes = NULL;

    PyObject * endianness;

    PyObject * q = NULL;

    char * header_bytes_char = NULL;

    Py_ssize_t table_len = 0;
    unsigned long long name_offset = 0;
    unsigned long long i = 0;

    if (PyArg_ParseTuple(
        args,
        "OOOO",
        &data_seq,
        &elf_section_header_table,
        &ehdr_dict,
        &endianness) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_elf_section_header_table_names");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data_seq) == 0
            || PyList_Check(elf_section_header_table) == 0
            || PyDict_Check(ehdr_dict) == 0 || PyUnicode_Check(endianness) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function read_elf_section_header_table_names");

            ret = NULL;
        }
        else
        {

            header_bytes = get_ehdr_string_table_slice(self, args);

            PyObjectAddToDelQueue(&q, header_bytes);

            if (PyBytes_Check(header_bytes) == 0)
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function read_elf_section_header_table_names");
                ret = NULL;
            }
            else
            {
                table_len = PySequence_Length(elf_section_header_table);

                header_bytes_char = PyBytes_AsString(header_bytes);

                ret = PyList_New(0);

                for (i = 0; i != table_len; i++)
                {
                    section_header = PySequence_GetItem(
                        elf_section_header_table,
                        i);

                    PyObjectAddToDelQueue(&q, section_header);

                    name_offset = PyLong_AsLong(
                        PyObjectAddToDelQueue(
                            &q,
                            PyLong_FromPyBytes(
                                PyDict_GetItem(
                                    section_header,
                                    PyObjectAddToDelQueue(
                                        &q,
                                        PyUnicode_FromString("sh_name"))),
                                endianness,
                                Py_False)));

                    PyList_Append(
                        ret,
                        PyObjectAddToDelQueue(
                            &q,
                            PyUnicode_FromString(
                                header_bytes_char + name_offset)));

                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
read_dynamic_section(PyObject *self, PyObject *args)
{
    PyObject * ret = NULL;

    PyObject * data_seq = NULL;
    PyObject * index = NULL;
    PyObject * bitness = NULL;

    PyObject * new_dyn_dict = NULL;

    PyObject * sub_data = NULL;
    char * sub_data_char = NULL;

    PyObject * current_index = NULL;
    PyObject * v1 = NULL;

    PyObject * endianness = NULL;

    PyObject * q = NULL;

    unsigned long long one_value_size = 0;
    long bitness_l = 0;
    unsigned long long end = 0;

    union
    {
        Elf32_Dyn u32;
        Elf64_Dyn u64;
    } u;

    if (PyArg_ParseTuple(args, "OOOO", &data_seq, &index, &bitness, &endianness)
        == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function read_dynamic_section");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data_seq) == 0 || PyLong_Check(index) == 0
            || PyLong_Check(bitness) == 0 || PyUnicode_Check(endianness) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function read_dynamic_section");

            ret = NULL;
        }
        else
        {

            if (PyLong_AsLong(index) < 0
                || (PyLong_AsLong(bitness) != 32 && PyLong_AsLong(bitness) != 64))
            {
                PyErr_SetString(
                    PyExc_ValueError,
                    "Wrong parameter values to function read_dynamic_section");
                ret = NULL;
            }
            else
            {
                bitness_l = PyLong_AsLong(bitness);

                switch (bitness_l)
                {
                    case 32:
                        one_value_size = sizeof(Elf32_Dyn);
                        break;
                    case 64:
                        one_value_size = sizeof(Elf64_Dyn);
                        break;
                    default:
                        PyErr_SetString(
                            PyExc_TypeError,
                            "Wrong bitness number in read_dynamic_section");

                        ret = NULL;
                        one_value_size = 0;
                        break;
                }

                if (one_value_size == 0)
                {
                    ret = NULL;
                }
                else
                {

                    ret = PyList_New(0);

                    current_index = PyLong_FromLong(0);

                    PyObjectAddToDelQueue(&q, current_index);

                    end = 0;

                    while (1)
                    {

                        memset(&u, 0, sizeof(u));

                        v1 = PyNumber_Add(
                            index,
                            PyObjectAddToDelQueue(
                                &q,
                                PyNumber_Multiply(
                                    current_index,
                                    PyObjectAddToDelQueue(
                                        &q,
                                        PyLong_FromUnsignedLongLong(
                                            one_value_size)))));

                        PyObjectAddToDelQueue(&q, v1);

                        sub_data = PySequence_GetSlice(
                            data_seq,
                            PyLong_AsSsize_t(v1),
                            PyLong_AsSsize_t(
                                PyObjectAddToDelQueue(
                                    &q,
                                    PyNumber_Add(
                                        v1,
                                        PyObjectAddToDelQueue(
                                            &q,
                                            PyLong_FromUnsignedLongLong(
                                                one_value_size))))));

                        PyObjectAddToDelQueue(&q, sub_data);

                        sub_data_char = PyBytes_AsString(sub_data);

                        switch (bitness_l)
                        {
                            case 32:
                                memcpy(
                                    &u.u32,
                                    sub_data_char,
                                    sizeof(Elf32_Dyn));
                                break;
                            case 64:
                                memcpy(
                                    &u.u64,
                                    sub_data_char,
                                    sizeof(Elf64_Dyn));
                                break;
                            default:
                                PyErr_SetString(
                                    PyExc_TypeError,
                                    "Wrong bitness number in read_dynamic_section");

                                ret = NULL;
                                break;
                        }

                        if (PyErr_Occurred() != NULL)
                        {
                            ret = NULL;
                            break;
                        }

                        switch (bitness_l)
                        {
                            case 32:
                                if (u.u32.d_tag == 0)
                                {
                                    end = 1;
                                }
                                break;
                            case 64:
                                if (u.u64.d_tag == 0)
                                {
                                    end = 1;
                                }
                                break;
                            default:
                                PyErr_SetString(
                                    PyExc_TypeError,
                                    "Wrong bitness number in read_dynamic_section");

                                ret = NULL;
                                break;
                        }

                        if (PyErr_Occurred() != NULL)
                        {
                            ret = NULL;
                            break;
                        }

                        if (end == 1)
                        {
                            break;
                        }

                        new_dyn_dict = PyDict_New();

                        PyObjectAddToDelQueue(&q, new_dyn_dict);

                        switch (bitness_l)
                        {
                            case 32:

                                PyDict_SetItem(
                                    new_dyn_dict,
                                    PyObjectAddToDelQueue(
                                        &q,
                                        PyUnicode_FromString("d_tag")),
                                    PyObjectAddToDelQueue(
                                        &q,
                                        ReadLong(
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyBytes_FromStringAndSize(
                                                    (char *) ((char *) &u
                                                        + offsetof(
                                                            Elf32_Dyn,
                                                            d_tag)),
                                                    member_size(Elf32_Dyn, d_tag) )),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(0)),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(
                                                    member_size(Elf32_Dyn, d_tag) )),
                                            endianness,
                                            Py_False)));

                                PyDict_SetItem(
                                    new_dyn_dict,
                                    PyObjectAddToDelQueue(
                                        &q,
                                        PyUnicode_FromString("d_val")),
                                    PyObjectAddToDelQueue(
                                        &q,
                                        ReadLong(
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyBytes_FromStringAndSize(
                                                    (char *) ((char *) &u
                                                        + offsetof(
                                                            Elf32_Dyn,
                                                            d_un)),
                                                    member_size(Elf32_Dyn, d_un) )),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(0)),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(
                                                    member_size(Elf32_Dyn, d_un) )),
                                            endianness,
                                            Py_False)));

                                PyDict_SetItem(
                                    new_dyn_dict,
                                    PyObjectAddToDelQueue(
                                        &q,
                                        PyUnicode_FromString("d_ptr")),
                                    PyObjectAddToDelQueue(
                                        &q,
                                        ReadLong(
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyBytes_FromStringAndSize(
                                                    (char *) ((char *) &u
                                                        + offsetof(
                                                            Elf32_Dyn,
                                                            d_un)),
                                                    member_size(Elf32_Dyn, d_un) )),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(0)),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(
                                                    member_size(Elf32_Dyn, d_un) )),
                                            endianness,
                                            Py_False)));

                                break;
                            case 64:

                                PyDict_SetItem(
                                    new_dyn_dict,
                                    PyObjectAddToDelQueue(
                                        &q,
                                        PyUnicode_FromString("d_tag")),
                                    PyObjectAddToDelQueue(
                                        &q,
                                        ReadLong(
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyBytes_FromStringAndSize(
                                                    (char *) ((char *) &u
                                                        + offsetof(
                                                            Elf64_Dyn,
                                                            d_tag)),
                                                    member_size(Elf64_Dyn, d_tag) )),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(0)),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(
                                                    member_size(Elf64_Dyn, d_tag) )),
                                            endianness,
                                            Py_False)));

                                PyDict_SetItem(
                                    new_dyn_dict,
                                    PyObjectAddToDelQueue(
                                        &q,
                                        PyUnicode_FromString("d_val")),
                                    PyObjectAddToDelQueue(
                                        &q,
                                        ReadLong(
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyBytes_FromStringAndSize(
                                                    (char *) ((char *) &u
                                                        + offsetof(
                                                            Elf64_Dyn,
                                                            d_un)),
                                                    member_size(Elf64_Dyn, d_un) )),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(0)),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(
                                                    member_size(Elf64_Dyn, d_un) )),
                                            endianness,
                                            Py_False)));

                                PyDict_SetItem(
                                    new_dyn_dict,
                                    PyObjectAddToDelQueue(
                                        &q,
                                        PyUnicode_FromString("d_ptr")),
                                    PyObjectAddToDelQueue(
                                        &q,
                                        ReadLong(
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyBytes_FromStringAndSize(
                                                    (char *) ((char *) &u
                                                        + offsetof(
                                                            Elf64_Dyn,
                                                            d_un)),
                                                    member_size(Elf64_Dyn, d_un) )),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(0)),
                                            PyObjectAddToDelQueue(
                                                &q,
                                                PyLong_FromLong(
                                                    member_size(Elf64_Dyn, d_un) )),
                                            endianness,
                                            Py_False)));
                                break;
                        }

                        if (PyErr_Occurred() != NULL)
                        {
                            ret = NULL;
                            break;
                        }

                        PyList_Append(ret, new_dyn_dict);

                        current_index = PyObjectAddToDelQueue(
                            &q,
                            PyNumber_Add(
                                current_index,
                                PyObjectAddToDelQueue(&q, PyLong_FromLong(1))));
                    }
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
get_dynamic_strings(PyObject *self, PyObject *args, int type)
{
    PyObject * ret = NULL;

    PyObject * dinamics_table = NULL;
    PyObject * data_seq = NULL;
    PyObject * elf_section_header_table = NULL;
    PyObject * byteorder = NULL;

    PyObject * program_table = NULL;

    PyObject * args2 = NULL;
    PyObject * header_bytes = NULL;
    char * header_bytes_chars = NULL;

    PyObject * item = NULL;
    PyObject * name = NULL;

    PyObject * q = NULL;

    long i = 0;
    long offset = 0;
    long dinamics_table_size = 0;

    if (PyArg_ParseTuple(
        args,
        "OOOOO",
        &data_seq,
        &program_table,
        &dinamics_table,
        &elf_section_header_table,
        &byteorder) == 0)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Wrong parameters to function get_dynamic_libs_names");

        ret = NULL;
    }
    else
    {
        if (PySequence_Check(data_seq) == 0 || PyList_Check(program_table) == 0
            || PyList_Check(dinamics_table) == 0
            || PyList_Check(elf_section_header_table) == 0
            || PyUnicode_Check(byteorder) == 0)
        {
            PyErr_SetString(
                PyExc_TypeError,
                "Wrong parameter types to function get_dynamic_libs_names");

            ret = NULL;
        }
        else
        {

            args2 = Py_BuildValue(
                "OOOO",
                data_seq,
                program_table,
                dinamics_table,
                byteorder);

            PyObjectAddToDelQueue(&q, args2);

            header_bytes = get_dyn_string_table_slice(self, args2);

            PyObjectAddToDelQueue(&q, header_bytes);

            if (header_bytes == NULL)
            {
                ret = NULL;
            }
            else
            {

                if (PyBytes_Check(header_bytes) == 0)
                {
                    ret = PyLong_FromLong(2);
                }
                else
                {
                    header_bytes_chars = PyBytes_AsString(header_bytes);

                    dinamics_table_size = PySequence_Length(dinamics_table);

                    ret = PyList_New(0);

                    for (i = 0; i != dinamics_table_size; i++)
                    {
                        item = PySequence_GetItem(dinamics_table, i);

                        PyObjectAddToDelQueue(&q, item);

                        if (PyLong_AsLong(
                            PyDict_GetItem(
                                item,
                                PyObjectAddToDelQueue(
                                    &q,
                                    PyUnicode_FromString("d_tag"))))
                            == type)
                        {
                            offset = PyLong_AsLong(
                                PyDict_GetItem(
                                    item,
                                    PyObjectAddToDelQueue(
                                        &q,
                                        PyUnicode_FromString("d_ptr"))));

                            name = PyObjectAddToDelQueue(
                                &q,
                                PyUnicode_FromString(
                                    header_bytes_chars + offset));

                            PyList_Append(ret, name);
                        }
                    }
                }
            }
        }
    }

    PyObjectDelQueue(&q);

    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        Py_XDECREF(ret);
        ret = NULL;
    }

    return ret;
}

PyObject *
get_dynamic_libs_names(PyObject *self, PyObject *args)
{
    return get_dynamic_strings(self, args, DT_NEEDED);
}

PyObject *
get_dynamic_runpath_values(PyObject *self, PyObject *args)
{
    return get_dynamic_strings(self, args, DT_RUNPATH);
}

static PyMethodDef elf_bin_methods[] =
    {
        {
            "read_e_ident",
            read_e_ident,
            METH_VARARGS,
            "read e_ident from bytes object" },

        {
            "is_elf",
            is_elf,
            METH_VARARGS,
            "check is bytes varibale is elf. var length must be == 4 bytes" },

        {
            "e_ident_bitness",
            e_ident_bitness,
            METH_VARARGS,
            "return elf bitness by e_ident" },

        {
            "e_ident_endianness",
            e_ident_endianness,
            METH_VARARGS,
            "return elf endianness by e_ident" },

        {
            "e_ident_to_dict",
            e_ident_to_dict,
            METH_VARARGS,
            "convert e_ident to Python dict" },

        {
            "read_elf_ehdr",
            read_elf_ehdr,
            METH_VARARGS,
            "reads elf header using e_ident to know bitness" },

        {
            "read_elf_ehdr_x",
            read_elf_ehdr_x,
            METH_VARARGS,
            "read elf section header by given bitness" },

        {
            "read_elf_shdr",
            read_elf_shdr,
            METH_VARARGS,
            "reads elf section header using e_ident to know bitness" },

        {
            "read_elf_shdr_x",
            read_elf_shdr_x,
            METH_VARARGS,
            "read elf header by given bitness" },

        {
            "read_elf_phdr",
            read_elf_phdr,
            METH_VARARGS,
            "reads elf section header using e_ident to know bitness" },

        {
            "read_elf_phdr_x",
            read_elf_phdr_x,
            METH_VARARGS,
            "read elf header by given bitness" },

        {
            "elf32_ehdr_to_dict",
            elf32_ehdr_to_dict,
            METH_VARARGS,
            "convert Elf32_Ehdr to dict" },

        {
            "elf64_ehdr_to_dict",
            elf64_ehdr_to_dict,
            METH_VARARGS,
            "convert Elf64_Ehdr to dict" },

        {
            "elf_ehdr_to_dict",
            elf_ehdr_to_dict,
            METH_VARARGS,
            "Split elf ehdr to Python dict by knowing bitness from e_ident" },

        {
            "shdr32_to_dict",
            shdr32_to_dict,
            METH_VARARGS,
            "Reads header item form header table" },

        {
            "shdr64_to_dict",
            shdr64_to_dict,
            METH_VARARGS,
            "Reads header item form header table" },

        {
            "read_elf_section_header_table",
            read_elf_section_header_table,
            METH_VARARGS,
            "reads header table" },

        {
            "phdr32_to_dict",
            phdr32_to_dict,
            METH_VARARGS,
            "Reads header item from header table" },

        {
            "phdr64_to_dict",
            phdr64_to_dict,
            METH_VARARGS,
            "Reads header item from header table" },

        {
            "read_elf_program_header_table",
            read_elf_program_header_table,
            METH_VARARGS,
            "reads header table" },

        {
            "read_elf_section_header_table_names",
            read_elf_section_header_table_names,
            METH_VARARGS,
            "get section headers names" },

        {
            "read_dynamic_section",
            read_dynamic_section,
            METH_VARARGS,
            "read dynamic section" },

        {
            "get_dynamic_libs_names",
            get_dynamic_libs_names,
            METH_VARARGS,
            "Get dianmic libs names required by elf file" },

        {
            "get_dynamic_runpath_values",
            get_dynamic_runpath_values,
            METH_VARARGS,
            "Get runpath values" },

        {
            "convert_virtual_to_file",
            convert_virtual_to_file,
            METH_VARARGS,
            "Converts address from virtual to offset" },

        { NULL, NULL, 0, NULL } };

static struct PyModuleDef elf_bin_module =
    { PyModuleDef_HEAD_INIT, "elf_bin", NULL, -1, elf_bin_methods };

PyMODINIT_FUNC
PyInit_elf_bin(void)
{
    return PyModule_Create(&elf_bin_module);
}

#undef member_size
