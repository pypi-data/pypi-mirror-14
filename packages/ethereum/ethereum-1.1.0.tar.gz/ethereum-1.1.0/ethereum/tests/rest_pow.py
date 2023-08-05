import time
from ethereum import blocks
from ethereum import utils
from ethereum import ethash_utils
from ethereum.tests.utils import new_db
from ethereum.slogging import get_logger
log = get_logger()

_db = new_db()


def mine(block, steps=1000):
    sz = blocks.get_cache_size(block.number)
    cache = blocks.get_cache_memoized(block.header.seed, sz)
    fsz = blocks.get_full_size(block.number)
    nonce = utils.big_endian_to_int(block.nonce)
    TT64M1 = 2**64 - 1
    target = utils.zpad(utils.int_to_big_endian(2**256 // (block.difficulty or 1)), 32)
    found = False
    for i in range(1, steps + 1):
        block.nonce = utils.zpad(utils.int_to_big_endian((nonce + i) & TT64M1), 8)
        o = blocks.hashimoto_light(fsz, cache, block.mining_hash,
                                   block.nonce)
        if o["result"] <= target:
            block.mixhash = o["mix digest"]
            found = True
            break
    if not found:
        return False


def test_pow():
    blk = blocks.genesis(_db)
    pow_times = []
    for i in range(10):
        blk.finalize()
        blk.commit_state()
        blk = blocks.Block.init_from_parent(blk, blk.coinbase, timestamp=blk.timestamp + 12)
        log.debug('mining', num=blk.number)
        mine(blk, steps=10000000)
        st = time.time()
        blk.header.check_pow()
        pow_times.append(time.time() - st)
    avg = sum(pow_times) / len(pow_times)
    sdev = [abs(t - avg) for t in pow_times] / len(pow_times)
    rdev = sdev / avg
    log.debug('stats', avg=avg, sdev=sdev, rdev=rdev, max=max(pow_times))
