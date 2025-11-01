from eth.vm.forks.frontier import FrontierVM
from eth.chains.base import MiningChain
from eth.db.atomic import AtomicDB
from eth_utils import decode_hex
from eth.rlp.headers import BlockHeader

# 복호화된 바이트코드
evm_code = "600060005561000f565b60006000fd5b5078d9cd7eebb512f957b17e346c920e29eed9f66a914aed82d5b17e9462920e6878d9f6da934aedc253b1aebf658f39"

# 사용자 정의 체인
class CustomChain(MiningChain):
    vm_configuration = ((0, FrontierVM),)
    chain_id = 1337

# 제네시스 헤더 세팅
db = AtomicDB()
genesis_header = BlockHeader(difficulty=1, block_number=0, gas_limit=10000000, timestamp=0)
chain = CustomChain.from_genesis_header(db, genesis_header)

# VM 인스턴스 생성
vm = chain.get_vm()

# 코드 실행
state = vm.state
message = state.get_message(
    gas=1000000,
    to=b'',
    sender=b'\x00' * 20,
    value=0,
    data=b'',
    code=decode_hex(evm_code)
)

computation = state.computation_class.apply_computation(state, message, transaction_context=None)

# 출력
print("[+] Execution Success:", not computation.is_error)
print("[+] Return data (hex):", computation.output.hex())

try:
    print("[+] Flag (ascii):", computation.output.decode())
except:
    print("[-] Could not decode flag as ASCII.")
