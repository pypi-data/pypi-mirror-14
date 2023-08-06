#include <stdio.h>

#define LUA_LIB
#include "lua.h"
#include "lauxlib.h"

/*https://www.centos.org/docs/5/html/5.1/Deployment_Guide/s2-proc-meminfo.html
Gives information about RAM*/
/* Immunio Lua bindings */

static int
lua_meminfo(lua_State *L) {
  FILE *fp;
  char buf[2000];
  if ((fp=fopen("/proc/meminfo","r"))==NULL) {
    printf("Error! opening file");
  }
  else {
    fread(buf, 1, 2000, fp);
    size_t fsize = ftell(fp);
    buf[fsize] = '\0';
    lua_pushstring(L,buf);
  }
  fclose(fp);
  return 1;
}

static const luaL_Reg libmeminfo[] = {
  {"meminfo", lua_meminfo},
  {NULL, NULL}
};

int
luaopen_meminfo(lua_State *L) {
  luaL_checkversion(L);
  luaL_register(L, "perf", libmeminfo);
  return 1;
}
