from virtualMem import BaseVirtualMem
class OPTMem(BaseVirtualMem):
    def __init__(self,frame_number, addresses, binaryFileContent):
        super().__init__(frame_number)
        self.addresses = addresses
        self.tlb_fault = 0
        self.page_fault = 0
        self.fileContent = binaryFileContent

    def map_virtual_memory(self):
        output = []
        for address in self.addresses:
            soft_miss, hard_miss, found_frame = self.__mapHelper(address)
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
        pass
