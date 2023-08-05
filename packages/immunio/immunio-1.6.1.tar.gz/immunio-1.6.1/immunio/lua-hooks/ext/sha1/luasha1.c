#include <stdio.h>

#define LUA_LIB
#include "lua.h"
#include "lauxlib.h"

// Link this program with an external C or x86 compression function
extern void sha1_compress(uint32_t state[5], const uint8_t block[64]);

/* This function is implements the padding and blocking around the SHA1 compression function
 *
 * Copyright (c) 2014 Project Nayuki
 * http://www.nayuki.io/page/fast-sha1-hash-implementation-in-x86-assembly
 */
static void
sha1_hash(const uint8_t *message, uint32_t len, uint32_t hash[5]) {
	hash[0] = UINT32_C(0x67452301);
	hash[1] = UINT32_C(0xEFCDAB89);
	hash[2] = UINT32_C(0x98BADCFE);
	hash[3] = UINT32_C(0x10325476);
	hash[4] = UINT32_C(0xC3D2E1F0);

	uint32_t i;
	for (i = 0; len - i >= 64; i += 64)
		sha1_compress(hash, message + i);

	uint8_t block[64];
	uint32_t rem = len - i;
	memcpy(block, message + i, rem);

	block[rem] = 0x80;
	rem++;
	if (64 - rem >= 8)
		memset(block + rem, 0, 56 - rem);
	else {
		memset(block + rem, 0, 64 - rem);
		sha1_compress(hash, block);
		memset(block, 0, 56);
	}

	uint64_t longLen = ((uint64_t)len) << 3;
	for (i = 0; i < 8; i++)
		block[64 - 1 - i] = (uint8_t)(longLen >> (i * 8));
	sha1_compress(hash, block);
}

/* Immunio Lua bindings */

static int
lua_sha1(lua_State *L) {
	uint32_t hash[5] = {};
	char buf[41];
	size_t slen = 0;

	const char *input = luaL_checklstring(L, 1, &slen);
	sha1_hash(input, slen, hash);
	sprintf(buf, "%08x%08x%08x%08x%08x", hash[0], hash[1], hash[2], hash[3], hash[4]);
	lua_pushstring(L, buf);
	return 1;
}

static const luaL_Reg libsha1[] = {
  {"sha1", lua_sha1},
  {NULL, NULL}
};

int
luaopen_sha1(lua_State *L) {
  luaL_checkversion(L);
  luaL_register(L, "sha1", libsha1);
  return 1;
}