CROSS =
CC = $(CROSS)cc
AR = $(CROSS)ar

# Source of extensions compiled w/ Lua's source.
# Only include .c files that can't be directly included in ext/all.c.
SRC = \
	ext/all.c \
	ext/libinjection/libinjection_html5.c \
	ext/libinjection/libinjection_xss.c \
	ext/libinjection/libinjection_sqli.c \
	ext/lpeg/lpcap.c \
	ext/lpeg/lpcode.c \
	ext/lpeg/lpprint.c \
	ext/lpeg/lpvm.c

LUA_SRC = \
	lib/cookie.lua \
	lib/DataDumper.lua \
	lib/date.lua \
	lib/defence.lua \
	lib/diag.lua \
	lib/extensions.lua \
	lib/hmac.lua \
	lib/hooks.lua \
	lib/idn.lua \
	lib/lexgraph.lua \
	lib/neturl.lua \
	lib/paths.lua \
	lib/perf.lua \
	lib/permit.lua \
	lib/real_ip.lua \
	lib/sanitize_sql.lua \
	lib/sanitize_command.lua \
	lib/semver.lua \
	lib/sha1.lua \
	lib/snap.lua \
	lib/utils.lua \
	lib/lexers/bash_dqstr.lua \
	lib/lexers/bash.lua \
	lib/lexers/css_attr.lua \
	lib/lexers/css.lua \
	lib/lexers/html.lua \
	lib/lexers/javascript.lua \
	lib/lexer.lua \
	lib/hooks/authenticate.lua \
	lib/hooks/bad_cookie.lua \
	lib/hooks/custom_threat.lua \
	lib/hooks/encode.lua \
	lib/hooks/eval.lua \
	lib/hooks/exception.lua \
	lib/hooks/file_io.lua \
	lib/hooks/framework_csrf_check.lua \
	lib/hooks/framework_login.lua \
	lib/hooks/framework_password_reset.lua \
	lib/hooks/framework_redirect.lua \
	lib/hooks/framework_session.lua \
	lib/hooks/framework_user.lua \
	lib/hooks/http_request_finish.lua \
	lib/hooks/http_request_start.lua \
	lib/hooks/http_response_start.lua \
	lib/hooks/should_report.lua \
	lib/hooks/sql_execute.lua \
	lib/hooks/template_render_done.lua \
	lib/hooks/xss/escape.lua \
	lib/hooks/xss/escape_js.lua

OBJ = ${SRC:.c=.o}

SHA1OBJ = ext/sha1/sha1.o
SHA2OBJ = ext/sha2/sha256.o
OBJ = ${SRC:.c=.o} ${SHA1OBJ} ${SHA2OBJ}

# Library archive. Used for compiling along agent bindings.
SO_OUT = libimmunio.so
A_OUT = libimmunio.a

# CLI for running tests
CLI = ./lua
CLI_SRC = ext/luajit/src/luajit.c ${SRC}

XCFLAGS =
CFLAGS = -DLUA_USE_APICHECK -DLUAJIT -Dlua_assert=assert -O3 -fPIC ${XCFLAGS}
INCS = -Iext -Iext/luajit/src
LIBS = -lm -ldl

INIT_HOOK = hooks/__init__.lua
HOOK_SRCS := $(wildcard hooks/*.lua) hooks/__init__.lua
MIN_SRCS = $(HOOK_SRCS:hooks/%.lua=build/%.lua)
HOOKS_TARBALL = hooks.tgz
HOOKS_SRCS_TARBALL = hooks_srcs.tgz

LUAJIT_OBJ = ext/luajit/src/libluajit.a
LUAJIT_OUT = libluajit.a
LUAJIT_XCFLAGS = -fPIC

SYS = $(shell uname -s)

ifeq (${SYS}, Darwin)
	# Disable the JIT on OS X
	LUAJIT_XCFLAGS += -DLUAJIT_ENABLE_GC64
endif

# Build lua, run tests, and create hooks archive
all: ${CLI} ${INIT_HOOK} ${HOOKS_TARBALL} ${HOOKS_SRCS_TARBALL}

%.o: %.c
	MACOSX_DEPLOYMENT_TARGET="10.8" ${CC} ${CFLAGS} -c ${INCS} -o $@ $<

# There is a huge performance advantage compiling sha1.o with just -O
# -O2 or -O3 *reduce* the speed of the algorithm 30%
${SHA1OBJ}:
	${CC} -O -c ${INCS} -o ${SHA1OBJ} ${SHA1OBJ:.o=.c}

${SHA2OBJ}:
	${CC} -O -c ${INCS} -o ${SHA2OBJ} ${SHA2OBJ:.o=.c}

${SO_OUT}: ${OBJ} ${LUAJIT_OBJ}
	${CC} -shared ${CFLAGS} ${LIBS} -o $@ -lc $^

${A_OUT}: ${OBJ}
	${AR} -rcus $@ $^

${LUAJIT_OUT}: ${LUAJIT_OBJ}
	cp $^ $@

${LUAJIT_OBJ}:
	cd ext/luajit && MACOSX_DEPLOYMENT_TARGET="10.8" make CROSS="${CROSS}" CC=cc HOST_CC=cc TARGET_SYS=${SYS} XCFLAGS="${LUAJIT_XCFLAGS}"

# Build lua executable for testing and compilation
# Seperate compilation as we need the LUA_UNSAFE_MODE flag set...
${CLI}: ${CLI_SRC} ${LUAJIT_OBJ} ${SHA1OBJ} ${SHA2OBJ}
	${CC} ${CFLAGS} -DLUA_UNSAFE_MODE ${INCS} -o $@ $^ ${LIBS}

# Concatenate init hooks into one __init__.lua hook with two newlines in between
${INIT_HOOK}: ${LUA_SRC} ${CLI}
	rm -f hooks/__init__.lua
	${CLI} ./luald.lua ${LUA_SRC} > hooks/__init__.lua

build/%.lua: hooks/%.lua ${CLI}
	@mkdir -p build
	@echo Minifying $<
	@cd LuaMinify; ../lua CommandLineMinify.lua ../$< ../$@ >/dev/null

# Create tarball of hooks to publish
${HOOKS_TARBALL}: ${MIN_SRCS}
	tar -czf $@ -C build .

${HOOKS_SRCS_TARBALL}: ${HOOK_SRCS}
	tar -czf $@ -C hooks . --exclude="init"

cleanhooks:
	rm -f ${INIT_HOOK}
	rm -f build/*.lua

clean: cleanhooks
	rm -f ${CLI} ${OBJ} ${SO_OUT} ${A_OUT} ${LUAJIT_OUT} ${SHA1OBJ} ${SHA2OBJ}
	cd ext/luajit && make clean
	rm -f test_failed
	rm -rf build
	find . -name \*.o -delete


test: ${CLI} ${INIT_HOOK} lint ${MIN_SRCS}
	@rm -f test_failed
	@for file in test/*_test.lua; do printf "\nRunning $$file\n"; TEST_BUILT_HOOKS=1 ./${CLI} $$file || touch test_failed; done
	@test ! -f test_failed

lint: ${INIT_HOOK}
	@# Scan all lua files for lines with trailing spaces
	@# The leading `!` negates the logic, so this target fails if trailing
	@# spaces are found in any Lua file.
	@! find . -path ./LuaMinify -prune -o -name "*.lua" -exec grep -E -n "[[:space:]]+$$" {} +

.PHONY: all test clean lint
