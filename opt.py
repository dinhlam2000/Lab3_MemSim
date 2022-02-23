from virtualMem import BaseVirtualMem
class OPTMem(BaseVirtualMem):
    def __init__(self,frame_number, addresses, binaryFileContent):
        super().__init__(frame_number)
        self.addresses = addresses
        self.tlb_fault = 0
        self.page_fault = 0
        self.fileContent = binaryFileContent
        self.fn = 0

    def map_virtual_memory(self):
        output = []
        for index, address in enumerate(self.addresses):
            soft_miss, hard_miss, found_frame = self.__mapHelper(int(address), index)
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
    def __mapHelper(self,value, index):

        foundInLookUp = False
        foundFrame = -1
        pn = value // 256

        foundInLookUp, foundFrame = super().seekTlb(pn, self.fn)

        if foundInLookUp == True: #found in TLB
            #modify the lru queue
            return False, False, foundFrame

        #misses in tlb, now look up in pt
        foundInLookUp, foundFrame = super().seekPt(pn)
        if foundInLookUp == True: #found in PT
            return True, False, foundFrame

        # if value == 1050:
        #     import pdb; pdb.set_trace()

        #hard misses
        foundFrame = self.fn % self.frame_number
        if len(self.physical_memory) < self.frame_number:
            self.physical_memory.append(pn)
        else:
            #pick a victim based on the future
            foundFrame = self.__futureLookUp(self.addresses[index + 1:])
            pn_evicted = self.physical_memory[foundFrame]
            self.pt[pn_evicted] = [self.pt[pn_evicted][0] , 0] #change old pn to invalid bit
            self.updateTlb(pn_evicted, pn, foundFrame) #modify tlb table
            self.physical_memory[foundFrame] = pn


        self.fn = foundFrame + 1
        self.pt[pn] = [foundFrame, 1]
        return True, True, foundFrame

    def __futureLookUp(self, futureAddresses):
        foundFrame = -1
        futurePages = list(map(lambda x: int(x) // 256, futureAddresses))

        pn_referenced = {}
        #initialized everything to be -1 first
        for pn in self.physical_memory:
            pn_referenced[pn] = float('inf')


        counter = 0
        for index, page in enumerate(futurePages):
            if page in pn_referenced and pn_referenced[page] == float('inf'):
                pn_referenced[page] = index
                counter += 1

            if counter == len(pn_referenced): #don't need to keep searching since we found the first appearance of all pn in the future
                break

        # maxValue = max(pn_referenced.values())
        # latestOccurence = list(filter(lambda x: pn_referenced[x] == maxValue, pn_referenced))

        latestOccurence = max(pn_referenced, key=pn_referenced.get)

        return self.physical_memory.index(latestOccurence)





