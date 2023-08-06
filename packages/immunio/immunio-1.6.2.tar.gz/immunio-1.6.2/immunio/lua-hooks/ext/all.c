/*
* Based on Lua's all.c -- Lua core & libraries in a single file.
*/

#define luaall_c

#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"


// Include our custom modules
#include "libinjection/lualib.c"
#include "luautf8/lutf8lib.c"
#include "lpeg/lptree.c"
#include "lua-cmsgpack/lua_cmsgpack.c"
#include "lua-snapshot/snapshot.c"
#include "sha1/luasha1.c"
#include "sha2/luasha256.c"
#include "perf/luacpu.c"
#include "perf/lualoadavg.c"
#include "perf/luameminfo.c"
#include "perf/luaoslib.c"


static const luaL_Reg lj_lib_load[] = {
  // Default Lua modules
  //
  // SECURITY NOTE:
  // Some of the following modules are unsafe according to http://lua-users.org/wiki/SandBoxes.
  // They are loaded, but never exposed to the sandbox used to run the hook handlers.
  // See lib/boot.lua for more details.
  { "",               luaopen_base },
  { LUA_LOADLIBNAME,  luaopen_package },
  { LUA_TABLIBNAME,   luaopen_table },
  #if defined(LUA_UNSAFE_MODE)
    { LUA_IOLIBNAME,    luaopen_io },
    { LUA_OSLIBNAME,    luaopen_os },
  #endif
  { LUA_STRLIBNAME,   luaopen_string },
  { LUA_MATHLIBNAME,  luaopen_math },
  { LUA_DBLIBNAME,    luaopen_debug },
  { LUA_BITLIBNAME,   luaopen_bit },
  { LUA_JITLIBNAME,   luaopen_jit },

  // Our custom modules
  {"libinjection", luaopen_libinjection},
  {"utf8", luaopen_utf8},
  {"lpeg", luaopen_lpeg},
  {LUACMSGPACK_NAME, luaopen_cmsgpack},
  {"snapshot", luaopen_snapshot},
  {"sha1", luaopen_sha1},
  {"sha2", luaopen_sha256},
  {"perf", luaopen_cpuload},
  {"perf", luaopen_loadavg},
  {"perf", luaopen_meminfo},
  {"perf", luaopen_luaos},

  { NULL,   NULL }
};

// In unsafe mode define these as NOPs when we build a .so
#if !defined(LUA_UNSAFE_MODE)
LUALIB_API int luaopen_io(lua_State *L) {
  return 0;
}
LUALIB_API int luaopen_os(lua_State *L) {
  return 0;
}
#endif

LUALIB_API void luaL_openlibs(lua_State *L) {
  const luaL_Reg *lib;
  for (lib = lj_lib_load; lib->func; lib++) {
    lua_pushcfunction(L, lib->func);
    lua_pushstring(L, lib->name);
    lua_call(L, 1, 0);
  }
}

