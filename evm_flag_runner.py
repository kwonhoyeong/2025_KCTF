from eth.vm.forks.frontier import FrontierVM
from eth.chains.base import MiningChain
from eth.db.atomic import AtomicDB
from eth_utils import decode_hex
from eth.vm.transaction_context import BaseTransactionContext
from eth.rlp.headers import BlockHeader

# 복호화된 바이트코드
evm_code = "600060005561000f565b60006000fd5b5078d9cd7eebb512f957b17e346c920e29eed9f66a914aed82d5b17e9462920e6878d9f6da934aedc253b1aebf658f39"

# Chain 정의
class CustomChain(MiningChain):
    vm_configuration = ((0, FrontierVM),)
    chain_id = 1337

# Genesis 블록 수동 설정
db = AtomicDB()
genesis_header = BlockHeader(
    difficulty=1,
    block_number=0,
    gas_limit=10000000,
    timestamp=0
)

# 체인 생성
chain = CustomChain.from_genesis_header(db, genesis_header)
vm = chain.get_vm()

# 바이트코드 실행
computation = vm.execute_bytecode(
    origin=b'\x00' * 20,
    gas=1000000,
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

try:
    print("[+] Flag (ascii):", computation.output.decode())
except:
    print("[-] Could not decode flag as ASCII.")
