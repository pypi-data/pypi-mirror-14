require "snapshot"

snapshot.tron()
local S1 = snapshot.snapshot()

local tmp_local = {}
tmp_global = {}
local S2 = snapshot.snapshot()
print('RESULT:')
for k,v in pairs(S2) do
	if S1[k] == nil then
		print(k,v)
	end
end

