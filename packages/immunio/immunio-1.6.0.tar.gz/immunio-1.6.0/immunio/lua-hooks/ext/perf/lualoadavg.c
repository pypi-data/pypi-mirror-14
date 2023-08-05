#include <stdio.h>
#include <stdlib.h>

#define LUA_LIB
#include "lua.h"
#include "lauxlib.h"


/*https://www.centos.org/docs/5/html/5.1/Deployment_Guide/s2-proc-loadavg.html
Gives load average in regard to both the CPU and IO over time, as well as additional
data used by uptime and other commands. 
*/

/* Immunio Lua bindings */

static int
lua_loadavg(lua_State *L) {
  char c[100];
  FILE *fp;
  if ((fp=fopen("/proc/loadavg","r"))==NULL) {
    printf("Error! opening file");
  }
  if (fgets(c, 100, fp) != NULL) {
    lua_pushstring(L, c);
  }
  fclose(fp);
  return 1;
}

static const luaL_Reg libloadavg[] = {
  {"loadavg", lua_loadavg},
  {NULL, NULL}
};

int
luaopen_loadavg(lua_State *L) {
  luaL_checkversion(L);
  luaL_register(L, "perf", libloadavg);
  return 1;
}
