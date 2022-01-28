from datetime import datetime
import hashlib
import time
import traceback

class Block:
    __hash = ''
    __data = ''
    __time_stamp = None
    __prev_hash = ''
    __block_id = 0
    __static_block_id = -1
    __nonce = 0
    def __init__(self, prevHash: str, data) -> None:
        self.__prev_hash = prevHash
        self.__data = data
        self.__time_stamp = datetime.now().strftime('%H:%M:%S:%f')
        Block.__static_block_id+=1
        self.__block_id = Block.__static_block_id
        self.__hash = self.__calculate_hash_key()

    def __calculate_hash_key(self):
        self.__hash =  hashlib.sha256(str(self.__prev_hash + "".join(value for value in self.__data) + str(self.__block_id) + str(self.__nonce)).encode()).hexdigest()
        return self.__hash

    def _mining(self, difficult=1):
        hash = ""
        while(not(self.__valid_hash(hash, difficult))):
            self.__nonce+=1
            hash = self.__calculate_hash_key()

    def __valid_hash(self, hash, difficult):
        return hash[0:difficult] == '0'*difficult
        
    def _get_hash(self):
        return self.__hash

    def _get_block_id(self):
        return self.__block_id

    def _get_previous_hash(self):
        return self.__prev_hash

    def __str__(self) -> str:
        return f'Block: {self.__block_id} [\n\tPrev hash: {self.__prev_hash},\n\tData: {self.__data},\n\tTime Stamp: {self.__time_stamp},\n\tHash: {self.__hash},\n\tNonce: {self.__nonce}\n]\n'

class BlockChain:
    __chain = []
    __genesis_block = Block('00000000000', 'Genesis Block')
    def __init__(self, path_name='BlockChainDatabase_Example.txt') -> None:
        if not(self.__chain):
            self.__chain.append(self.__genesis_block)
            self.__load_database_create_block_chain(path_name)

    def __load_database_create_block_chain(self, path_name):
        block_chain = BlockChain()
        with open(path_name) as f:
            data = f.read()
            data = data.split('\n')
        block_data = []
        for cell in data:
            block_data = [value for value in cell.split()]
            block_chain.add_new_block(block_data)
        return True

    def get_last_block(self):
        return self.__chain[-1]

    def add_new_block(self, data: str):
        try:
            start_time = time.time()*1000
            block = Block(self.get_last_block()._get_hash(), data)
            block._mining()
            self.__chain.append(block)
            self.__write_log([str(len(self.__chain)-2), str(int(time.time()*1000 - start_time)), self.__chain[-1]._get_hash()])

            return True
        except: 
            traceback.print_exc()
            return False

    def export_chain(self):
        with open('./BlockChain.txt', 'w') as f:
            for block in list(self.__chain):
                f.writelines(block.__str__())

    def __write_log(self, log):
        with open('./log.txt', 'a+') as f:
            for data in log:
                f.write(data+', ')
            f.write("\n")
            f.close()

    def is_valid(self):
        previous_hash_block = self.__chain[0]._get_hash()
        for i in range(1, len(self.__chain)):
            block = self.__chain[i]
            prev_hash_current_block = block._get_previous_hash()

            if (block._get_hash() != block.__calculate_hash_key()) or (prev_hash_current_block != previous_hash_block):
                return (block._get_block_id, False)

            previous_hash_block = self.__chain[i]._get_hash()
        
        return True

block_chain = BlockChain()
block_chain.export_chain()