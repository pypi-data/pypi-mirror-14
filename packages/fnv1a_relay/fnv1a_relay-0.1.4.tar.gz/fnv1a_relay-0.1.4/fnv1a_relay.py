#coding=utf8

from cffi import FFI

ffi = FFI()

header = '''
static unsigned short
fnv1a_hashpos(const char *key, int len);
'''

src = '''
#include <stdlib.h>
#define FNV1A_32_OFFSET   2166136261UL
#define FNV1A_32_PRIME    16777619
/**
 * 32-bits unsigned FNV1a returning into hash, using p to as variable to
 * walk over metric up to firstspace
 */
#define fnv1a_32(hash, p, metric, firstspace) \
	hash = FNV1A_32_OFFSET; \
	for (p = metric; p < firstspace; p++) \
		hash = (hash ^ (unsigned int)*p) * FNV1A_32_PRIME;

static unsigned short
fnv1a_hashpos(const char *key, int len)
{
	unsigned int hash;
    const char *end = key + len;
	fnv1a_32(hash, key, key, end);
	return (unsigned short)((hash >> 16) ^ (hash & (unsigned int)0xFFFF));
}
'''
ffi.set_source("_fnv1a", header+src)
ffi.cdef(header)
ffi.compile()

from _fnv1a import ffi
lib = ffi.dlopen(None)
fnv1a_hashpos = lib.fnv1a_hashpos

if __name__ == "__main__":
    print fnv1a_hashpos('test', 4)