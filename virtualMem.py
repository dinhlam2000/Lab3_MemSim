class BaseVirtualMem:
    def __init__(self, frame_number):
        self.tlb = []
        self.pt = [[None, None]] * 256
        self.frame_number = frame_number
        self.physical_memory = []

    def seekTlb(self, pn, fn):
        for index, tlb_val in enumerate(self.tlb):
            # hit in TLB
            if tlb_val[0] == pn:
                evicted_value = self.tlb.pop(index)
                self.tlb.append(evicted_value)
                return True, tlb_val[1]

        if len(self.tlb) < self.frame_number and len(self.tlb) < 16:
            self.tlb.append([pn,fn])
        else:
            self.tlb.pop(0)
            self.tlb.append([pn, fn])

        return False, -1

    def seekPt(self, pn):
        if self.pt[pn][1] == 1:  # soft_miss only but found in PT
            return True, self.pt[pn][0]


        return False, -1

    def updateTlb(self, oldPn, newPn, foundFrame):
        for index, tlb_val in enumerate(self.tlb):
            if tlb_val[0] == oldPn:
                self.tlb.pop(index)
                self.tlb.append([newPn, foundFrame])
                return
