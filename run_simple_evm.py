from eth_utils import decode_hex
from ethereum.tools._solidity import get_contract_data
from ethereum import vm

# 복호화된 바이트코드
evm_hex = "600060005561000f565b60006000fd5b5078d9cd7eebb512f957b17e346c920e29eed9f66a914aed82d5b17e9462920e6878d9f6da934aedc253b1aebf658f39"

# 실행
code = decode_hex(evm_hex)
context = vm.Context(origin=b'\x00'*20, data=b'', to=b'', sender=b'\x00'*20, value=0, code=code)
comp = vm.Computation(context, vm.Memory(), vm.Stack(), {})
vm.run_code(comp)

output = comp.output
print("[+] Return data (hex):", output.hex())
try:
    print("[+] Decoded ASCII:", output.decode('utf-8'))
except:
    print("[-] Could not decode ASCII; output raw.")
