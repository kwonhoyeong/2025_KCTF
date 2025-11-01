from eth.vm.forks.frontier import FrontierVM
from eth.chains.base import MiningChain
from eth.db.atomic import AtomicDB
from eth_utils import decode_hex
from eth.vm.transaction_context import BaseTransactionContext

# 복호화된 바이트코드 (hex 그대로 붙여넣기)
evm_code = "600060005561000f565b60006000fd5b5078d9cd7eebb512f957b17e346c920e29eed9f66a914aed82d5b17e9462920e6878d9f6da934aedc253b1aebf658f39"

# EVM 환경 구성
class CustomChain(MiningChain):
    vm_configuration = ((0, FrontierVM),)

chain = CustomChain(AtomicDB())

state = chain.get_vm().state
computation = chain.get_vm().execute_bytecode(
    origin=b'\x00' * 20,
    gas=10**6,
    to=b'',
    sender=b'\x00' * 20,
    value=0,
    data=b'',
    code=decode_hex(evm_code),
    transaction_context=BaseTransactionContext(
        gas_price=1,
        origin=b'\x00' * 20
    )
)

# 결과 출력
print("[+] Execution Success:", not computation.is_error)
print("[+] Return data (hex):", computation.output.hex())

# 플래그 추출 시도
try:
    print("[+] Flag (ascii):", computation.output.decode())
except:
    print("[-] Couldn't decode output directly — try hex-to-ascii manually.")
