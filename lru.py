from virtualMem import BaseVirtualMem
class LRUMem(BaseVirtualMem):
    def __init__(self,frame_number, addresses, binaryFileContent):
        super().__init__(frame_number)
        self.addresses = addresses
        self.tlb_fault = 0
        self.page_fault = 0
        self.fileContent = binaryFileContent
        self.lru_queue = []
        self.fn = 0

    def map_virtual_memory(self):
        output = []
        for address in self.addresses:
            soft_miss, hard_miss, found_frame = self.__mapHelper(int(address))
            if soft_miss:
                self.tlb_fault += 1
            if hard_miss:
                self.page_fault += 1

            byteAtAddress = self.fileContent[int(address)]
            if byteAtAddress > 127:
                byteAtAddress = byteAtAddress - 256
            page_number = int(address) // 256

            content = self.fileContent[page_number * 256: (page_number + 1) * 256]
            content = content.hex()

            output.append([address, byteAtAddress, str(found_frame), content])

        return output
    def __mapHelper(self,value):

        foundInLookUp = False
        foundFrame = -1
        pn = value // 256

        # if value == 45631:
        #     import pdb; pdb.set_trace()
        foundInLookUp, foundFrame = super().seekTlb(pn)

        if foundInLookUp == True: #found in TLB
            #modify the lru queue
            index_foundFrame = self.lru_queue.index(foundFrame)
            self.lru_queue.pop(index_foundFrame)
            self.lru_queue.append(foundFrame)
            return False, False, foundFrame

        #misses in tlb, now look up in pt
        foundInLookUp, foundFrame = super().seekPt(pn)
        if foundInLookUp == True: #found in PT
            index_foundFrame = self.lru_queue.index(foundFrame)
            self.lru_queue.pop(index_foundFrame)
            self.lru_queue.append(foundFrame)
            self.updateTlb(pn,foundFrame)
            return True, False, foundFrame


        #hard misses
        foundFrame = self.fn % self.frame_number

        if len(self.physical_memory) < self.frame_number:
            self.physical_memory.append(pn)
            self.updateTlb(pn,foundFrame)
            self.lru_queue.append(foundFrame)
        else:
            #pick a victim based on least recently used
            foundFrame = self.lru_queue.pop(0)
            self.lru_queue.append(foundFrame)
            pn_evicted = self.physical_memory[foundFrame]
            self.pt[pn_evicted] = [self.pt[pn_evicted][0] , 0] #change old pn to invalid bit
            # self.updateTlb(pn,foundFrame)
            self.updateEvictedTlb(pn_evicted, pn, foundFrame) #modify tlb table
            self.physical_memory[foundFrame] = pn


        self.fn = foundFrame + 1
        self.pt[pn] = [foundFrame, 1]

        return True, True, foundFrame
