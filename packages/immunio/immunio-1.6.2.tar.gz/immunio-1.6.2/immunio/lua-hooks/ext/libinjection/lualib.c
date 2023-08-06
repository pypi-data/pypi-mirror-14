#include <stdlib.h>

#define LUA_LIB
#include "lua.h"
#include "lauxlib.h"

#include "libinjection.h"
#include "libinjection_sqli.h"

#define MAX_FINGERPRINT_STACK_SIZE 4096

int sqli(lua_State *L) {
  sfilter state;

  size_t slen = 0;
  const char *input = luaL_checklstring(L, 1, &slen);

  libinjection_sqli_init(&state, input, slen, FLAG_NONE);
  int issqli = libinjection_is_sqli(&state);

  lua_pushboolean(L, issqli);

  return 1;
}

int fingerprint(lua_State *L) {
  char stack_result[MAX_FINGERPRINT_STACK_SIZE];
  char *result = stack_result;
  struct libinjection_sqli_state state;
  size_t slen = 0;
  const char *input = luaL_checklstring(L, 1, &slen);

  libinjection_sqli_init(&state, input, slen, 0);

  // libinjection tokenizes in a streaming fashion, meaning we won't know until
  // the end of the process how long the resulting string of tokens will be. But
  // we do know that it will be less than or equal to the length of the SQL
  // string.
  //
  // For speed, use stack-allocated fingerprint result strings unless we need
  // more than 4KB.
  if (slen > sizeof(stack_result)) {
    result = malloc(slen + 1);
    if (!result) {
      lua_pushstring(L, ""); // Push something at least...
      return 1;
    }
  }

  int fp_idx = 0;
  while (state.pos < state.slen) {
    libinjection_sqli_tokenize(&state);
    result[fp_idx++] = state.tokenvec[0].type;
  }
  result[fp_idx] = '\0';

  lua_pushstring(L, result);

  // If we dynamically allocated the result above, free it
  if (result != stack_result) free(result);

  return 1;
}

int xss(lua_State *L) {
  size_t slen = 0;
  const char *input = luaL_checklstring(L, 1, &slen);

  int is_xss = libinjection_xss(input, slen);

  lua_pushboolean(L, is_xss);
  return 1;
}

/*
 * Tokenize the SQL into an array where each element
 * is a table with a type and value. For example:
 * {type: "E", value: "SELECT"}
 */
int sqli_tokenize(lua_State *L) {
  int token_cnt = 1;
  size_t slen = 0;
  const char *input = luaL_checklstring(L, 1, &slen);
  struct libinjection_sqli_state state;
  int var_symbol_count;

  libinjection_sqli_init(&state, input, slen, 0);

  lua_newtable(L);    /* Tokens array */
  while (state.pos < state.slen) {
    libinjection_sqli_tokenize(&state);

    lua_newtable(L); /* Inner token table */

    /* Token.type = type */
    lua_pushlstring(L, &state.tokenvec[0].type, 1);
    lua_setfield(L, -2, "type");

    /* Token.var_symbol_count = count for variable tokens */
    if (state.tokenvec[0].type == 'v') {
      lua_pushinteger(L, state.tokenvec[0].count);
      lua_setfield(L, -2, "var_symbol_count");
    }

    /* Token.value = value */
    lua_pushlstring(L, &input[state.tokenvec[0].pos],
        state.tokenvec[0].len);
    lua_setfield(L, -2, "value");

    /* Tokens.append(Token) */
    lua_pushinteger(L, token_cnt++);
    lua_insert(L, -2); /* [..., token, index] --> [..., index, token] */
    lua_settable(L, -3);
  }
  return 1;
}

static const luaL_Reg libinjection[] = {
  {"sqli", sqli},
  {"fingerprint", fingerprint},
  {"xss", xss},
  {"sqli_tokenize", sqli_tokenize},
  {NULL, NULL}
};

int luaopen_libinjection(lua_State *L) {
  luaL_register(L, "libinjection", libinjection);
  return 1;
}
