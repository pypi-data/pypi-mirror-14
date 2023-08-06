#include <stdio.h>

#define LUA_LIB
#include "lua.h"
#include "lauxlib.h"

// Link this program with an external C or x86 compression function
extern void sha256_compress(uint32_t state[8], const uint8_t block[64]);

/* This function is implements the padding and blocking around the SHA2 compression function
 *
 * Copyright (c) 2014 Project Nayuki
 * http://www.nayuki.io/page/fast-sha2-hashes-in-x86-assembly
 */
static void
sha256_hash(const uint8_t *message, uint32_t len, uint32_t hash[8]) {
	hash[0] = UINT32_C(0x6A09E667);
	hash[1] = UINT32_C(0xBB67AE85);
	hash[2] = UINT32_C(0x3C6EF372);
	hash[3] = UINT32_C(0xA54FF53A);
	hash[4] = UINT32_C(0x510E527F);
	hash[5] = UINT32_C(0x9B05688C);
	hash[6] = UINT32_C(0x1F83D9AB);
	hash[7] = UINT32_C(0x5BE0CD19);
	
	uint32_t i;
	for (i = 0; len - i >= 64; i += 64)
		sha256_compress(hash, message + i);
	
	uint8_t block[64];
	uint32_t rem = len - i;
	memcpy(block, message + i, rem);
	
	block[rem] = 0x80;
	rem++;
	if (64 - rem >= 8)
		memset(block + rem, 0, 56 - rem);
	else {
		memset(block + rem, 0, 64 - rem);
		sha256_compress(hash, block);
		memset(block, 0, 56);
	}
	
	uint64_t longLen = ((uint64_t)len) << 3;
	for (i = 0; i < 8; i++)
		block[64 - 1 - i] = (uint8_t)(longLen >> (i * 8));
	sha256_compress(hash, block);
}

/* Immunio Lua bindings */

static int
lua_sha256(lua_State *L) {
	uint32_t hash[8] = {};
	char buf[65];
	size_t slen = 0;

	const char *input = luaL_checklstring(L, 1, &slen);
	sha256_hash(input, slen, hash);
	sprintf(buf, "%08x%08x%08x%08x%08x%08x%08x%08x", hash[0], hash[1], hash[2], hash[3], hash[4], hash[5], hash[6], hash[7]);
	lua_pushlstring(L, buf, 64);
	return 1;
}

static const luaL_Reg libsha256[] = {
  {"sha256", lua_sha256},
  {NULL, NULL}
};

int
luaopen_sha256(lua_State *L) {
  luaL_checkversion(L);
  luaL_register(L, "sha2", libsha256);
  return 1;
}