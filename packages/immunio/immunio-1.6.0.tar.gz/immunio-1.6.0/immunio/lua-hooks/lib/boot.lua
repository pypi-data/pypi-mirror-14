VM_VERSION = 1
-- Global reference to hold the VM itself.
VM = nil

-- Create global agentdata and serverdata
agentdata = agentdata or {}
serverdata = serverdata or {}

-- XXX Java agent has built in assumption that this function exists before VM
-- initialisation.
-- Encode a Lua object to be sent to the server.
-- This can be removed when Java agent has moved to new VM API
function encode(object)
  return cmsgpack.pack(object)
end

-- Function called by the Agent to call and sandbox a function.
function sandboxed_call(method, vars)
  local rval = nil
  -- Merge caller supplied vars
  if vars then
    -- utils.debug_dump("Merge vars from agent: ", vars)
    for k, v in pairs(vars) do
      if k ~= "utils" then -- XXX agent API compatability. Ignore utils.
        _G[k] = v
      end
    end
  end
  if type(method) == "function" then
    -- legacy hooks. Convert to new hook call
    rval = method(vars)
    if rval and type(rval) == 'table' then
      -- Special handling for the __init__ hook
      -- If rval contains a _vm_update key then (re)install the package loader
      -- and (re)load packages and hooks
      if rval._vm_update then
        VM = rval._vm_update(DEV_MODE, VM_VERSION)
        rval = {}
      end
      -- Special handling for the other hooks
      if rval._vm_hook_call then
        -- swap _vm_hook_call string into method which will be passed to hooks.run below
        method = rval._vm_hook_call
      else
        -- Just punt the rval back to the caller.
        return rval
      end
    end
  end
  if type(method) == "string" then
    -- new style hook call
    if VM then
      -- Call it!
      rval = VM.run(method, vars)
    else
      error("Attempt to call hook '" .. method .. "' before VM code has loaded.")
    end
  elseif type(method) ~= 'function' then
    error("sandboxed_call called with a method of type " .. type(method) .. ".")
  end
  return rval
end

