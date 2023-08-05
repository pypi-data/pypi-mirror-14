
SCRYPT_SOURCES = scrypt/lib/crypto/crypto_scrypt.c scrypt/libcperciva/alg/sha256.c scrypt/lib/crypto/crypto_scrypt_smix.c scrypt/libcperciva/util/insecure_memzero.c scrypt/libcperciva/util/warnp.c
SCRYPT_INCLUDES = -Iscrypt -I scrypt/libcperciva/alg -I scrypt/libcperciva/cpusupport -I scrypt/libcperciva/util
SCRYPT_DEFS = -DCONFIG_H_FILE=\"config_freebsd.h\"

BCRYPT_SOURCES = py-bcrypt/bcrypt/bcrypt.c py-bcrypt/bcrypt/blowfish.c py-bcrypt/bcrypt/bcrypt_pbkdf.c py-bcrypt/bcrypt/sha2.c
BCRYPT_INCLUDES = -Ipy-bcrypt/bcrypt 

FASTPBKDF2_SOURCES = fastpbkdf2/fastpbkdf2.c
FASTPBKDF2_INCLUDES = -Ifastpbkdf2
FASTPBKDF2_DEFS = -std=c99
FASTPBKDF2_LIBS = -lcrypto

SOURCES += ${SCRYPT_SOURCES} ${BCRYPT_SOURCES} ${FASTPBKDF2_SOURCES}
INCLUDES += ${SCRYPT_INCLUDES} ${BCRYPT_INCLUDES} ${FASTPBKDF2_INCLUDES}
DEFS += ${SCRYPT_DEFS} ${FASTPBKDF2_DEFS}
LIBS += ${FASTPBKDF2_LIBS}

LIBPATH = ./libmultikdf.so


# Use cffi.FFI.dlopen() to check that all symbols are resolved
LOADLIB_PYSRC = "from cffi import FFI; ffi = FFI(); lib = ffi.dlopen('${LIBPATH}')"


# Default to NOT printing commands - override with
# VERBOSE=1 make
#MAKEFLAGS += --silent

# Don't treat files named clean, prebuild_all etc as targets
.PHONY: clean buildlib test prep help targets

all:	prep

# Make some targets silent (do not print commands)
.SILENT: help gitupdate test scrypt/cpusupport-config.h

help:
	echo "\
help: 		Show this output\n\
targets:	Same as help\n\
prep:		Configure code including CPU-specific optimizations\n\
buildlib:	Build shared library\n\
test:		Test that all shared library symbols can be resolved\n\
clean:		Clean up build outputs\n\
gitupdate:	Update sources from upstream git repos\n\
"

targets: help

clean: 
	rm -rf libmultikdf.so scrypt/cpusupport-config.h

prep: scrypt/cpusupport-config.h

test:	buildlib
	python -c ${LOADLIB_PYSRC}
	echo "Shared library symbols can be resolved"

buildlib: prep ${LIBPATH}

scrypt/cpusupport-config.h:
	srcdir=. make -s -C scrypt -f Makefile.am cpusupport-config.h

${LIBPATH}:
	gcc -o ${LIBPATH} -shared -fPIC ${DEFS} ${INCLUDES} -Wl,--whole-archive ${SOURCES} -Wl,--no-whole-archive ${LIBS}

gitupdate:
	echo "Updating sources from upstream git repos"
	rm -rf fastpbkdf2 py-bcrypt scrypt

	git clone --depth 1 'https://github.com/ctz/fastpbkdf2.git'
	rm -rf fastpbkdf2/.git fastpbkdf2/.gitignore

	git clone --depth 1 'https://github.com/sundarnagarajan/py-bcrypt.git'
	rm -rf py-bcrypt/.git py-bcrypt/.gitignore

	git clone --depth 1 'https://github.com/Tarsnap/scrypt.git'
	rm -rf scrypt/.git scrypt/.gitignore scrypt/test/.gitignore
