
#include <Python.h>
#include <stddef.h>

/* this block of #ifs should be kept exactly identical between
   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py */
#if defined(_MSC_VER)
# include <malloc.h>   /* for alloca() */
# if _MSC_VER < 1600   /* MSVC < 2010 */
   typedef __int8 int8_t;
   typedef __int16 int16_t;
   typedef __int32 int32_t;
   typedef __int64 int64_t;
   typedef unsigned __int8 uint8_t;
   typedef unsigned __int16 uint16_t;
   typedef unsigned __int32 uint32_t;
   typedef unsigned __int64 uint64_t;
   typedef __int8 int_least8_t;
   typedef __int16 int_least16_t;
   typedef __int32 int_least32_t;
   typedef __int64 int_least64_t;
   typedef unsigned __int8 uint_least8_t;
   typedef unsigned __int16 uint_least16_t;
   typedef unsigned __int32 uint_least32_t;
   typedef unsigned __int64 uint_least64_t;
   typedef __int8 int_fast8_t;
   typedef __int16 int_fast16_t;
   typedef __int32 int_fast32_t;
   typedef __int64 int_fast64_t;
   typedef unsigned __int8 uint_fast8_t;
   typedef unsigned __int16 uint_fast16_t;
   typedef unsigned __int32 uint_fast32_t;
   typedef unsigned __int64 uint_fast64_t;
   typedef __int64 intmax_t;
   typedef unsigned __int64 uintmax_t;
# else
#  include <stdint.h>
# endif
# if _MSC_VER < 1800   /* MSVC < 2013 */
   typedef unsigned char _Bool;
# endif
#else
# include <stdint.h>
# if (defined (__SVR4) && defined (__sun)) || defined(_AIX)
#  include <alloca.h>
# endif
#endif

#if PY_MAJOR_VERSION < 3
# undef PyCapsule_CheckExact
# undef PyCapsule_GetPointer
# define PyCapsule_CheckExact(capsule) (PyCObject_Check(capsule))
# define PyCapsule_GetPointer(capsule, name) \
    (PyCObject_AsVoidPtr(capsule))
#endif

#if PY_MAJOR_VERSION >= 3
# define PyInt_FromLong PyLong_FromLong
#endif

#define _cffi_from_c_double PyFloat_FromDouble
#define _cffi_from_c_float PyFloat_FromDouble
#define _cffi_from_c_long PyInt_FromLong
#define _cffi_from_c_ulong PyLong_FromUnsignedLong
#define _cffi_from_c_longlong PyLong_FromLongLong
#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong

#define _cffi_to_c_double PyFloat_AsDouble
#define _cffi_to_c_float PyFloat_AsDouble

#define _cffi_from_c_int_const(x)                                        \
    (((x) > 0) ?                                                         \
        ((unsigned long long)(x) <= (unsigned long long)LONG_MAX) ?      \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromUnsignedLongLong((unsigned long long)(x)) :       \
        ((long long)(x) >= (long long)LONG_MIN) ?                        \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromLongLong((long long)(x)))

#define _cffi_from_c_int(x, type)                                        \
    (((type)-1) > 0 ? /* unsigned */                                     \
        (sizeof(type) < sizeof(long) ?                                   \
            PyInt_FromLong((long)x) :                                    \
         sizeof(type) == sizeof(long) ?                                  \
            PyLong_FromUnsignedLong((unsigned long)x) :                  \
            PyLong_FromUnsignedLongLong((unsigned long long)x)) :        \
        (sizeof(type) <= sizeof(long) ?                                  \
            PyInt_FromLong((long)x) :                                    \
            PyLong_FromLongLong((long long)x)))

#define _cffi_to_c_int(o, type)                                          \
    (sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \
                                         : (type)_cffi_to_c_i8(o)) :     \
     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \
                                         : (type)_cffi_to_c_i16(o)) :    \
     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \
                                         : (type)_cffi_to_c_i32(o)) :    \
     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \
                                         : (type)_cffi_to_c_i64(o)) :    \
     (Py_FatalError("unsupported size for type " #type), (type)0))

#define _cffi_to_c_i8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[1])
#define _cffi_to_c_u8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[2])
#define _cffi_to_c_i16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[3])
#define _cffi_to_c_u16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[4])
#define _cffi_to_c_i32                                                   \
                 ((int(*)(PyObject *))_cffi_exports[5])
#define _cffi_to_c_u32                                                   \
                 ((unsigned int(*)(PyObject *))_cffi_exports[6])
#define _cffi_to_c_i64                                                   \
                 ((long long(*)(PyObject *))_cffi_exports[7])
#define _cffi_to_c_u64                                                   \
                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])
#define _cffi_to_c_char                                                  \
                 ((int(*)(PyObject *))_cffi_exports[9])
#define _cffi_from_c_pointer                                             \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[10])
#define _cffi_to_c_pointer                                               \
    ((char *(*)(PyObject *, CTypeDescrObject *))_cffi_exports[11])
#define _cffi_get_struct_layout                                          \
    ((PyObject *(*)(Py_ssize_t[]))_cffi_exports[12])
#define _cffi_restore_errno                                              \
    ((void(*)(void))_cffi_exports[13])
#define _cffi_save_errno                                                 \
    ((void(*)(void))_cffi_exports[14])
#define _cffi_from_c_char                                                \
    ((PyObject *(*)(char))_cffi_exports[15])
#define _cffi_from_c_deref                                               \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[16])
#define _cffi_to_c                                                       \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[17])
#define _cffi_from_c_struct                                              \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[18])
#define _cffi_to_c_wchar_t                                               \
    ((wchar_t(*)(PyObject *))_cffi_exports[19])
#define _cffi_from_c_wchar_t                                             \
    ((PyObject *(*)(wchar_t))_cffi_exports[20])
#define _cffi_to_c_long_double                                           \
    ((long double(*)(PyObject *))_cffi_exports[21])
#define _cffi_to_c__Bool                                                 \
    ((_Bool(*)(PyObject *))_cffi_exports[22])
#define _cffi_prepare_pointer_call_argument                              \
    ((Py_ssize_t(*)(CTypeDescrObject *, PyObject *, char **))_cffi_exports[23])
#define _cffi_convert_array_from_object                                  \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[24])
#define _CFFI_NUM_EXPORTS 25

typedef struct _ctypedescr CTypeDescrObject;

static void *_cffi_exports[_CFFI_NUM_EXPORTS];
static PyObject *_cffi_types, *_cffi_VerificationError;

static int _cffi_setup_custom(PyObject *lib);   /* forward */

static PyObject *_cffi_setup(PyObject *self, PyObject *args)
{
    PyObject *library;
    int was_alive = (_cffi_types != NULL);
    (void)self; /* unused */
    if (!PyArg_ParseTuple(args, "OOO", &_cffi_types, &_cffi_VerificationError,
                                       &library))
        return NULL;
    Py_INCREF(_cffi_types);
    Py_INCREF(_cffi_VerificationError);
    if (_cffi_setup_custom(library) < 0)
        return NULL;
    return PyBool_FromLong(was_alive);
}

static int _cffi_init(void)
{
    PyObject *module, *c_api_object = NULL;

    module = PyImport_ImportModule("_cffi_backend");
    if (module == NULL)
        goto failure;

    c_api_object = PyObject_GetAttrString(module, "_C_API");
    if (c_api_object == NULL)
        goto failure;
    if (!PyCapsule_CheckExact(c_api_object)) {
        PyErr_SetNone(PyExc_ImportError);
        goto failure;
    }
    memcpy(_cffi_exports, PyCapsule_GetPointer(c_api_object, "cffi"),
           _CFFI_NUM_EXPORTS * sizeof(void *));

    Py_DECREF(module);
    Py_DECREF(c_api_object);
    return 0;

  failure:
    Py_XDECREF(module);
    Py_XDECREF(c_api_object);
    return -1;
}

#define _cffi_type(num) ((CTypeDescrObject *)PyList_GET_ITEM(_cffi_types, num))

/**********/



#include "Python.h"
#ifdef __FreeBSD__
#include <sys/extattr.h>
#elif defined(__SUN__) || defined(__sun__) || defined(__sun)
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#include <alloca.h>
#else
#include <sys/xattr.h>
#endif

#ifdef __FreeBSD__

/* FreeBSD compatibility API */
#define XATTR_XATTR_NOFOLLOW 0x0001
#define XATTR_XATTR_CREATE 0x0002
#define XATTR_XATTR_REPLACE 0x0004
#define XATTR_XATTR_NOSECURITY 0x0008

#define XATTR_CREATE 0x1
#define XATTR_REPLACE 0x2

/* Converts a freebsd format attribute list into a NULL terminated list.
 * While the man page on extattr_list_file says it is NULL terminated,
 * it is actually the first byte that is the length of the
 * following attribute.
 */
static void convert_bsd_list(char *namebuf, size_t size)
{
    size_t offset = 0;
    while(offset < size) {
        int length = (int) namebuf[offset];
        memmove(namebuf+offset, namebuf+offset+1, length);
        namebuf[offset+length] = '\0';
        offset += length+1;
    }
}

static ssize_t xattr_getxattr(const char *path, const char *name,
                              void *value, ssize_t size, u_int32_t position,
                              int options)
{
    if (position != 0 ||
        !(options == 0 || options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }

    if (options & XATTR_XATTR_NOFOLLOW) {
        return extattr_get_link(path, EXTATTR_NAMESPACE_USER,
                                name, value, size);
    }
    else {
        return extattr_get_file(path, EXTATTR_NAMESPACE_USER,
                                name, value, size);
    }
}

static ssize_t xattr_setxattr(const char *path, const char *name,
                              void *value, ssize_t size, u_int32_t position,
                              int options)
{
    int rv = 0;
    int nofollow;

    if (position != 0) {
        return -1;
    }

    nofollow = options & XATTR_XATTR_NOFOLLOW;
    options &= ~XATTR_XATTR_NOFOLLOW;

    if (options == XATTR_XATTR_CREATE ||
        options == XATTR_XATTR_REPLACE) {

        /* meh. FreeBSD doesn't really have this in its
         * API... Oh well.
         */
    }
    else if (options != 0) {
        return -1;
    }

    if (nofollow) {
        rv = extattr_set_link(path, EXTATTR_NAMESPACE_USER,
                                name, value, size);
    }
    else {
        rv = extattr_set_file(path, EXTATTR_NAMESPACE_USER,
                                name, value, size);
    }

    /* freebsd returns the written length on success, not zero. */
    if (rv >= 0) {
        return 0;
    }
    else {
        return rv;
    }
}

static ssize_t xattr_removexattr(const char *path, const char *name,
                                 int options)
{
    if (!(options == 0 ||
          options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }

    if (options & XATTR_XATTR_NOFOLLOW) {
        return extattr_delete_link(path, EXTATTR_NAMESPACE_USER, name);
    }
    else {
        return extattr_delete_file(path, EXTATTR_NAMESPACE_USER, name);
    }
}


static ssize_t xattr_listxattr(const char *path, char *namebuf,
                               size_t size, int options)
{
    ssize_t rv = 0;
    if (!(options == 0 ||
          options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }

    if (options & XATTR_XATTR_NOFOLLOW) {
        rv = extattr_list_link(path, EXTATTR_NAMESPACE_USER, namebuf, size);
    }
    else {
        rv = extattr_list_file(path, EXTATTR_NAMESPACE_USER, namebuf, size);
    }

    if (rv > 0 && namebuf) {
        convert_bsd_list(namebuf, rv);
    }

    return rv;
}

static ssize_t xattr_fgetxattr(int fd, const char *name, void *value,
                               ssize_t size, u_int32_t position, int options)
{
    if (position != 0 ||
        !(options == 0 || options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }

    if (options & XATTR_XATTR_NOFOLLOW) {
        return -1;
    }
    else {
        return extattr_get_fd(fd, EXTATTR_NAMESPACE_USER, name, value, size);
    }
}

static ssize_t xattr_fsetxattr(int fd, const char *name, void *value,
                               ssize_t size, u_int32_t position, int options)
{
    int rv = 0;
    int nofollow;

    if (position != 0) {
        return -1;
    }

    nofollow = options & XATTR_XATTR_NOFOLLOW;
    options &= ~XATTR_XATTR_NOFOLLOW;

    if (options == XATTR_XATTR_CREATE ||
        options == XATTR_XATTR_REPLACE) {
        /* freebsd noop */
    }
    else if (options != 0) {
        return -1;
    }

    if (nofollow) {
        return -1;
    }
    else {
        rv = extattr_set_fd(fd, EXTATTR_NAMESPACE_USER,
                            name, value, size);
    }

    /* freebsd returns the written length on success, not zero. */
    if (rv >= 0) {
        return 0;
    }
    else {
        return rv;
    }
}

static ssize_t xattr_fremovexattr(int fd, const char *name, int options)
{

    if (!(options == 0 ||
          options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }

    if (options & XATTR_XATTR_NOFOLLOW) {
        return -1;
    }
    else {
        return extattr_delete_fd(fd, EXTATTR_NAMESPACE_USER, name);
    }
}


static ssize_t xattr_flistxattr(int fd, char *namebuf, size_t size, int options)
{
    ssize_t rv = 0;

    if (!(options == 0 ||
          options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }

    if (options & XATTR_XATTR_NOFOLLOW) {
        return -1;
    }
    else {
        rv = extattr_list_fd(fd, EXTATTR_NAMESPACE_USER, namebuf, size);
    }

    if (rv > 0 && namebuf) {
        convert_bsd_list(namebuf, rv);
    }

    return rv;
}

#elif defined(__SUN__) || defined(__sun__) || defined(__sun)

/* Solaris 9 and later compatibility API */
#define XATTR_XATTR_NOFOLLOW 0x0001
#define XATTR_XATTR_CREATE 0x0002
#define XATTR_XATTR_REPLACE 0x0004
#define XATTR_XATTR_NOSECURITY 0x0008

#define XATTR_CREATE 0x1
#define XATTR_REPLACE 0x2

#ifndef u_int32_t
#define u_int32_t uint32_t
#endif

static ssize_t xattr_fgetxattr(int fd, const char *name, void *value,
                               ssize_t size, u_int32_t position, int options)
{
    int xfd;
    ssize_t bytes;
    struct stat statbuf;

    /* XXX should check that name does not have / characters in it */
    xfd = openat(fd, name, O_RDONLY | O_XATTR);
    if (xfd == -1) {
    return -1;
    }
    if (lseek(xfd, position, SEEK_SET) == -1) {
    close(xfd);
    return -1;
    }
    if (value == NULL) {
        if (fstat(xfd, &statbuf) == -1) {
        close(xfd);
        return -1;
        }
    close(xfd);
    return statbuf.st_size;
    }
    /* XXX should keep reading until the buffer is exhausted or EOF */
    bytes = read(xfd, value, size);
    close(xfd);
    return bytes;
}

static ssize_t xattr_getxattr(const char *path, const char *name,
                              void *value, ssize_t size, u_int32_t position,
                              int options)
{
    int fd;
    ssize_t bytes;

    if (position != 0 ||
        !(options == 0 || options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }

    fd = open(path,
          O_RDONLY |
          ((options & XATTR_XATTR_NOFOLLOW) ? O_NOFOLLOW : 0));
    if (fd == -1) {
    return -1;
    }
    bytes = xattr_fgetxattr(fd, name, value, size, position, options);
    close(fd);
    return bytes;
}

static ssize_t xattr_fsetxattr(int fd, const char *name, void *value,
                               ssize_t size, u_int32_t position, int options)
{
    int xfd;
    ssize_t bytes = 0;

    /* XXX should check that name does not have / characters in it */
    xfd = openat(fd, name, O_XATTR | O_TRUNC |
         ((options & XATTR_XATTR_CREATE) ? O_EXCL : 0) |
         ((options & XATTR_XATTR_NOFOLLOW) ? O_NOFOLLOW : 0) |
         ((options & XATTR_XATTR_REPLACE) ? O_RDWR : O_WRONLY|O_CREAT),
         0644);
    if (xfd == -1) {
    return -1;
    }
    while (size > 0) {
    bytes = write(xfd, value, size);
    if (bytes == -1) {
        close(xfd);
        return -1;
    }
    size -= bytes;
    value += bytes;
    }
    close(xfd);
    return 0;
}

static ssize_t xattr_setxattr(const char *path, const char *name,
                              void *value, ssize_t size, u_int32_t position,
                              int options)
{
    int fd;
    ssize_t bytes;

    if (position != 0) {
        return -1;
    }

    fd = open(path,
          O_RDONLY | (options & XATTR_XATTR_NOFOLLOW) ? O_NOFOLLOW : 0);
    if (fd == -1) {
    return -1;
    }
    bytes = xattr_fsetxattr(fd, name, value, size, position, options);
    close(fd);
    return bytes;
}

static ssize_t xattr_fremovexattr(int fd, const char *name, int options)
{
  int xfd, status;
    /* XXX should check that name does not have / characters in it */
    if (!(options == 0 || options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }
    if (options & XATTR_XATTR_NOFOLLOW) {
        return -1;
    }
    xfd = openat(fd, ".", O_XATTR, 0644);
    if (xfd == -1) {
    return -1;
    }
    status = unlinkat(xfd, name, 0);
    close(xfd);
    return status;
}

static ssize_t xattr_removexattr(const char *path, const char *name,
                                 int options)
{
    int fd;
    ssize_t status;

    fd = open(path,
          O_RDONLY | ((options & XATTR_XATTR_NOFOLLOW) ? O_NOFOLLOW : 0));
    if (fd == -1) {
    return -1;
    }
    status =  xattr_fremovexattr(fd, name, options);
    close(fd);
    return status;
}

static ssize_t xattr_xflistxattr(int xfd, char *namebuf, size_t size, int options)
{
    int esize;
    DIR *dirp;
    struct dirent *entry;
    ssize_t nsize = 0;

    dirp = fdopendir(xfd);
    if (dirp == NULL) {
        return (-1);
    }
    while (entry = readdir(dirp)) {
        if (strcmp(entry->d_name, ".") == 0 ||
                strcmp(entry->d_name, "..") == 0)
            continue;
        esize = strlen(entry->d_name);
        if (nsize + esize + 1 <= size) {
            snprintf((char *)(namebuf + nsize), esize + 1,
                    entry->d_name);
        }
        nsize += esize + 1; /* +1 for \0 */
    }
    closedir(dirp);
    return nsize;
}
static ssize_t xattr_flistxattr(int fd, char *namebuf, size_t size, int options)
{
    int xfd;

    xfd = openat(fd, ".", O_RDONLY | O_XATTR);
    return xattr_xflistxattr(xfd, namebuf, size, options);
}

static ssize_t xattr_listxattr(const char *path, char *namebuf,
                               size_t size, int options)
{
    int xfd;

    xfd = attropen(path, ".", O_RDONLY);
    return xattr_xflistxattr(xfd, namebuf, size, options);
}

#elif !defined(XATTR_NOFOLLOW)
/* Linux compatibility API */
#define XATTR_XATTR_NOFOLLOW 0x0001
#define XATTR_XATTR_CREATE 0x0002
#define XATTR_XATTR_REPLACE 0x0004
#define XATTR_XATTR_NOSECURITY 0x0008
static ssize_t xattr_getxattr(const char *path, const char *name, void *value, ssize_t size, u_int32_t position, int options) {
    if (position != 0 || !(options == 0 || options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }
    if (options & XATTR_XATTR_NOFOLLOW) {
        return lgetxattr(path, name, value, size);
    } else {
        return getxattr(path, name, value, size);
    }
}

static ssize_t xattr_setxattr(const char *path, const char *name, void *value, ssize_t size, u_int32_t position, int options) {
    int nofollow;
    if (position != 0) {
        return -1;
    }
    nofollow = options & XATTR_XATTR_NOFOLLOW;
    options &= ~XATTR_XATTR_NOFOLLOW;
    if (options == XATTR_XATTR_CREATE) {
        options = XATTR_CREATE;
    } else if (options == XATTR_XATTR_REPLACE) {
        options = XATTR_REPLACE;
    } else if (options != 0) {
        return -1;
    }
    if (nofollow) {
        return lsetxattr(path, name, value, size, options);
    } else {
        return setxattr(path, name, value, size, options);
    }
}

static ssize_t xattr_removexattr(const char *path, const char *name, int options) {
    if (!(options == 0 || options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }
    if (options & XATTR_XATTR_NOFOLLOW) {
        return lremovexattr(path, name);
    } else {
        return removexattr(path, name);
    }
}


static ssize_t xattr_listxattr(const char *path, char *namebuf, size_t size, int options) {
    if (!(options == 0 || options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }
    if (options & XATTR_XATTR_NOFOLLOW) {
        return llistxattr(path, namebuf, size);
    } else {
        return listxattr(path, namebuf, size);
    }
}

static ssize_t xattr_fgetxattr(int fd, const char *name, void *value, ssize_t size, u_int32_t position, int options) {
    if (position != 0 || !(options == 0 || options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }
    if (options & XATTR_XATTR_NOFOLLOW) {
        return -1;
    } else {
        return fgetxattr(fd, name, value, size);
    }
}

static ssize_t xattr_fsetxattr(int fd, const char *name, void *value, ssize_t size, u_int32_t position, int options) {
    int nofollow;
    if (position != 0) {
        return -1;
    }
    nofollow = options & XATTR_XATTR_NOFOLLOW;
    options &= ~XATTR_XATTR_NOFOLLOW;
    if (options == XATTR_XATTR_CREATE) {
        options = XATTR_CREATE;
    } else if (options == XATTR_XATTR_REPLACE) {
        options = XATTR_REPLACE;
    } else if (options != 0) {
        return -1;
    }
    if (options & XATTR_XATTR_NOFOLLOW) {
        return -1;
    } else {
        return fsetxattr(fd, name, value, size, options);
    }
}

static ssize_t xattr_fremovexattr(int fd, const char *name, int options) {
    if (!(options == 0 || options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }
    if (options & XATTR_XATTR_NOFOLLOW) {
        return -1;
    } else {
        return fremovexattr(fd, name);
    }
}


static ssize_t xattr_flistxattr(int fd, char *namebuf, size_t size, int options) {
    if (!(options == 0 || options == XATTR_XATTR_NOFOLLOW)) {
        return -1;
    }
    if (options & XATTR_XATTR_NOFOLLOW) {
        return -1;
    } else {
        return flistxattr(fd, namebuf, size);
    }
}

#else /* Mac OS X assumed */
#define xattr_getxattr getxattr
#define xattr_fgetxattr fgetxattr
#define xattr_removexattr removexattr
#define xattr_fremovexattr fremovexattr
#define xattr_setxattr setxattr
#define xattr_fsetxattr fsetxattr
#define xattr_listxattr listxattr
#define xattr_flistxattr flistxattr
#endif

#ifndef XATTR_MAXNAMELEN
#define XATTR_MAXNAMELEN 127
#endif

#ifndef XATTR_NOFOLLOW
#define XATTR_NOFOLLOW 0x0001
#endif

#ifndef XATTR_NOSECURITY
#define XATTR_NOSECURITY 0x0008
#endif


static PyObject *
_cffi_f_xattr_fgetxattr(PyObject *self, PyObject *args)
{
  int x0;
  char const * x1;
  void * x2;
  ssize_t x3;
  uint32_t x4;
  int x5;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:xattr_fgetxattr", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(0), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca((size_t)datasize);
    memset((void *)x2, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(1), arg2) < 0)
      return NULL;
  }

  x3 = _cffi_to_c_int(arg3, ssize_t);
  if (x3 == (ssize_t)-1 && PyErr_Occurred())
    return NULL;

  x4 = _cffi_to_c_int(arg4, uint32_t);
  if (x4 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  x5 = _cffi_to_c_int(arg5, int);
  if (x5 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = xattr_fgetxattr(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static PyObject *
_cffi_f_xattr_flistxattr(PyObject *self, PyObject *args)
{
  int x0;
  char * x1;
  size_t x2;
  int x3;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:xattr_flistxattr", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, size_t);
  if (x2 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, int);
  if (x3 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = xattr_flistxattr(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static PyObject *
_cffi_f_xattr_fremovexattr(PyObject *self, PyObject *args)
{
  int x0;
  char const * x1;
  int x2;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:xattr_fremovexattr", &arg0, &arg1, &arg2))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(0), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = xattr_fremovexattr(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static PyObject *
_cffi_f_xattr_fsetxattr(PyObject *self, PyObject *args)
{
  int x0;
  char const * x1;
  void * x2;
  ssize_t x3;
  uint32_t x4;
  int x5;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:xattr_fsetxattr", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(0), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca((size_t)datasize);
    memset((void *)x2, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(1), arg2) < 0)
      return NULL;
  }

  x3 = _cffi_to_c_int(arg3, ssize_t);
  if (x3 == (ssize_t)-1 && PyErr_Occurred())
    return NULL;

  x4 = _cffi_to_c_int(arg4, uint32_t);
  if (x4 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  x5 = _cffi_to_c_int(arg5, int);
  if (x5 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = xattr_fsetxattr(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static PyObject *
_cffi_f_xattr_getxattr(PyObject *self, PyObject *args)
{
  char const * x0;
  char const * x1;
  void * x2;
  ssize_t x3;
  uint32_t x4;
  int x5;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:xattr_getxattr", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(0), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca((size_t)datasize);
    memset((void *)x2, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(1), arg2) < 0)
      return NULL;
  }

  x3 = _cffi_to_c_int(arg3, ssize_t);
  if (x3 == (ssize_t)-1 && PyErr_Occurred())
    return NULL;

  x4 = _cffi_to_c_int(arg4, uint32_t);
  if (x4 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  x5 = _cffi_to_c_int(arg5, int);
  if (x5 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = xattr_getxattr(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static PyObject *
_cffi_f_xattr_listxattr(PyObject *self, PyObject *args)
{
  char const * x0;
  char * x1;
  size_t x2;
  int x3;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:xattr_listxattr", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, size_t);
  if (x2 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, int);
  if (x3 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = xattr_listxattr(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static PyObject *
_cffi_f_xattr_removexattr(PyObject *self, PyObject *args)
{
  char const * x0;
  char const * x1;
  int x2;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:xattr_removexattr", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(0), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = xattr_removexattr(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static PyObject *
_cffi_f_xattr_setxattr(PyObject *self, PyObject *args)
{
  char const * x0;
  char const * x1;
  void * x2;
  ssize_t x3;
  uint32_t x4;
  int x5;
  Py_ssize_t datasize;
  ssize_t result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:xattr_setxattr", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(0), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca((size_t)datasize);
    memset((void *)x2, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(1), arg2) < 0)
      return NULL;
  }

  x3 = _cffi_to_c_int(arg3, ssize_t);
  if (x3 == (ssize_t)-1 && PyErr_Occurred())
    return NULL;

  x4 = _cffi_to_c_int(arg4, uint32_t);
  if (x4 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  x5 = _cffi_to_c_int(arg5, int);
  if (x5 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = xattr_setxattr(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, ssize_t);
}

static int _cffi_const_XATTR_CREATE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(XATTR_CREATE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "XATTR_CREATE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return ((void)lib,0);
}

static int _cffi_const_XATTR_MAXNAMELEN(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(XATTR_MAXNAMELEN);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "XATTR_MAXNAMELEN", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_XATTR_CREATE(lib);
}

static int _cffi_const_XATTR_NOFOLLOW(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(XATTR_NOFOLLOW);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "XATTR_NOFOLLOW", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_XATTR_MAXNAMELEN(lib);
}

static int _cffi_const_XATTR_NOSECURITY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(XATTR_NOSECURITY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "XATTR_NOSECURITY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_XATTR_NOFOLLOW(lib);
}

static int _cffi_const_XATTR_REPLACE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(XATTR_REPLACE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "XATTR_REPLACE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_XATTR_NOSECURITY(lib);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return _cffi_const_XATTR_REPLACE(lib);
}

static PyMethodDef _cffi_methods[] = {
  {"xattr_fgetxattr", _cffi_f_xattr_fgetxattr, METH_VARARGS, NULL},
  {"xattr_flistxattr", _cffi_f_xattr_flistxattr, METH_VARARGS, NULL},
  {"xattr_fremovexattr", _cffi_f_xattr_fremovexattr, METH_VARARGS, NULL},
  {"xattr_fsetxattr", _cffi_f_xattr_fsetxattr, METH_VARARGS, NULL},
  {"xattr_getxattr", _cffi_f_xattr_getxattr, METH_VARARGS, NULL},
  {"xattr_listxattr", _cffi_f_xattr_listxattr, METH_VARARGS, NULL},
  {"xattr_removexattr", _cffi_f_xattr_removexattr, METH_VARARGS, NULL},
  {"xattr_setxattr", _cffi_f_xattr_setxattr, METH_VARARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__x7c9e2f59xb862c7dd",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__x7c9e2f59xb862c7dd(void)
{
  PyObject *lib;
  lib = PyModule_Create(&_cffi_module_def);
  if (lib == NULL)
    return NULL;
  if (((void)lib,0) < 0 || _cffi_init() < 0) {
    Py_DECREF(lib);
    return NULL;
  }
  return lib;
}

#else

PyMODINIT_FUNC
init_cffi__x7c9e2f59xb862c7dd(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__x7c9e2f59xb862c7dd", _cffi_methods);
  if (lib == NULL)
    return;
  if (((void)lib,0) < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
