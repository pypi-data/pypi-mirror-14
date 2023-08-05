#!python
#cython: boundscheck=False
#cython: wraparound=False
#cython: initializedcheck=False
#cython: profile=True

cimport cython
import numpy as np
cimport numpy as np
import os
import string

from BasicBWT cimport BasicBWT

cdef enum:
    letterBits = 3 #defined
    numberBits = 5 #8-letterBits
    numPower = 32  #2**numberBits
    mask = 7       #255 >> numberBits 
    
    bitPower = 11  #defined
    binSize = 2048 #2**self.bitPower
    
    vcLen = 6      #defined
    
    connectBuffer = 30 #defined

cdef struct bwtRange:
    unsigned long l
    unsigned long h
    
cdef class tdbg(object):
    '''
    The intent of this class to store a transcript de bruijn graph, we will have other functions separate for 
    the logic of what we want to store in this graph
    '''
    #we store a dictionary of k-mers where every k-mer has at least "threshold" counts
    cdef dict kmers
    cdef dict addedKmers
    cdef unsigned long k
    cdef unsigned long threshold
    
    #we also store a dictionary of the transcripts
    cdef dict transDict
    cdef dict correctedDict
    
    #this is the BWT things we need
    cdef char * dirName
    cdef bint useMemmapRLE
    cdef np.ndarray bwt
    cdef np.uint8_t [:] bwt_view
    
    cdef np.ndarray startIndex
    cdef np.uint64_t [:] startIndex_view
    cdef np.ndarray endIndex
    cdef np.uint64_t [:] endIndex_view
    
    cdef np.ndarray partialFM
    cdef np.uint64_t[:, :] partialFM_view
    
    cdef unsigned long totalSize
    cdef np.ndarray totalCounts
    cdef np.uint64_t [:] totalCounts_view
    
    cdef np.ndarray refFM
    cdef np.uint64_t [:] refFM_view
    cdef unsigned long offsetSum
    
    cdef dict pathStats
    
    def __init__(tdbg self, char * dirName, unsigned long k=49, unsigned long threshold=3):
        '''
        init
        @param bwt - the bwt we will gather all our counts from
        @param k - the k-mer size to count
        @param threshold - the number of counts we need to store a k-mer long term
        '''
        self.kmers = {}
        self.k = k
        self.threshold = threshold
        
        self.transDict = {}
        self.correctedDict = {}
        
        self.pathStats = {}
        
        self.loadMsbwt(dirName, False, None)
        
        print 'initialized'
    
    def loadMsbwt(tdbg self, char * dirName, bint useMemmap=True, logger=None):
        '''
        This functions loads a BWT file and constructs total counts, indexes start positions, and constructs an FM index in memory
        @param dirName - the directory to load, inside should be '<DIR>/comp_msbwt.npy' or it will fail
        '''
        #open the file with our BWT in it
        self.dirName = dirName
        self.useMemmapRLE = useMemmap
        if useMemmap:
            self.bwt = np.load(self.dirName+'/comp_msbwt.npy', 'r+')
        else:
            self.bwt = np.load(self.dirName+'/comp_msbwt.npy')
        self.bwt_view = self.bwt
        
        #build auxiliary structures
        self.constructTotalCounts(logger)
        self.constructIndexing()
        self.constructFMIndex(logger)
        
    def constructTotalCounts(tdbg self, logger):
        '''
        This function constructs the total count for each valid character in the array and stores it under '<DIR>/totalCounts.p'
        since these values are independent of compression
        '''
        cdef str abtFN = self.dirName+'/totalCounts.npy'
        if os.path.exists(abtFN):
            if self.useMemmapRLE:
                self.totalCounts = np.load(abtFN, 'r+')
            else:
                self.totalCounts = np.load(abtFN)
            self.totalCounts_view = self.totalCounts
        else:
            raise Exception('Need to load MSBWT first!')
        
        self.totalSize = int(np.sum(self.totalCounts))
    
    cdef void constructIndexing(tdbg self):
        '''
        This helper function calculates the start and end index for each character in the BWT.  Basically, the information
        generated here is for quickly finding offsets.  This is run AFTER self.constructTotalCounts(...)
        '''
        #mark starts and ends of key elements
        self.startIndex = np.zeros(dtype='<u8', shape=(vcLen, ))
        self.startIndex_view = self.startIndex
        self.endIndex = np.zeros(dtype='<u8', shape=(vcLen, ))
        self.endIndex_view = self.endIndex
        
        cdef unsigned long pos = 0
        cdef unsigned long i
        with nogil:
            for i in range(0, vcLen):
                self.startIndex_view[i] = pos
                pos += self.totalCounts_view[i]
                self.endIndex_view[i] = pos
    
    def constructFMIndex(tdbg self, logger):
        '''
        This function iterates through the BWT and counts the letters as it goes to create the FM index.  For example, the string 'ACC$' would have BWT
        'C$CA'.  The FM index would iterate over this and count the occurence of the letter it found so you'd end up with this:
        BWT    FM-index
        C    0    0    0
        $    0    0    1
        C    1    0    1
        A    1    0    2
             1    1    2
        This is necessary for finding the occurrence of a letter using the getOccurrenceOfCharAtIndex(...) function.
        In reality, this function creates a sampled FM-index more complicated than the uncompressed counter-part.  This is 
        because the 2048 size bins don't fall evenly all the time.  A second data structure is used to tell you where to start
        a particular FM-index count.  The two files necessary are '<DIR>/comp_fmIndex.npy' and '<DIR>/comp_refIndex.npy'
        '''
        #sampling method
        cdef str fmIndexFN = self.dirName+'/comp_fmIndex.npy'
        cdef str fmRefFN = self.dirName+'/comp_refIndex.npy'
        
        if os.path.exists(fmIndexFN) and os.path.exists(fmRefFN):
            #both exist, just memmap them
            if self.useMemmapRLE:
                self.partialFM = np.load(fmIndexFN, 'r+')
            else:
                self.partialFM = np.load(fmIndexFN)
            self.partialFM_view = self.partialFM
            
            if self.useMemmapRLE:
                self.refFM = np.load(fmRefFN, 'r+')
            else:
                self.refFM = np.load(fmRefFN)
            self.refFM_view = self.refFM
        else:
            raise Exception('Need to load MSBWT first!')
            
        #we'll use this later when we do lookups
        self.offsetSum = np.sum(self.partialFM[0])
    
    
    #cpdef inline unsigned long countOccurrencesOfSeq(tdbg self, unsigned char[:] seq_view) nogil:
    cpdef unsigned long countOccurrencesOfSeq(tdbg self, unsigned char[:] seq_view):
        '''
        This function counts the number of occurrences of the given sequence
        @param seq - the sequence to search for
        @param givenRange - the range to start from (if a partial search has already been run), default=whole range
        @return - an integer count of the number of times seq occurred in this BWT
        '''
        cdef long x
        cdef unsigned long c
        cdef unsigned long seqLen = seq_view.shape[0]
        
        cdef bwtRange krange
        krange.l = 0
        krange.h = self.totalSize
        
        #create a view of the sequence that can be used in a nogil region
        for x in range(seqLen-1, -1, -1):
            #get the character from the sequence, then search at both high and low
            c = charToNum_view[seq_view[x]]
            krange = self.getOccurrenceOfCharAtRange(c, krange)
            
            #early exit for counts
            if krange.l == krange.h:
                return 0
        
        #return the difference
        return krange.h - krange.l
    
    cdef inline unsigned long countOccurrencesOfStr(tdbg self, bytes seq):
        '''
        This function counts the number of occurrences of the given sequence
        @param seq - the sequence to search for
        @param givenRange - the range to start from (if a partial search has already been run), default=whole range
        @return - an integer count of the number of times seq occurred in this BWT
        '''
        cdef long x
        cdef unsigned long c
        cdef unsigned long seqLen = len(seq)
        
        cdef unsigned char * seq_view = seq
        
        cdef bwtRange krange
        krange.l = 0
        krange.h = self.totalSize
        
        #create a view of the sequence that can be used in a nogil region
        for x in range(seqLen-1, -1, -1):
            #get the character from the sequence, then search at both high and low
            c = charToNum_view[seq_view[x]]
            krange = self.getOccurrenceOfCharAtRange(c, krange)
            
            #early exit for counts
            if krange.l == krange.h:
                return 0
        
        #return the difference
        return krange.h - krange.l
    
    cdef inline unsigned long getOccurrenceOfCharAtIndex(tdbg self, unsigned long sym, unsigned long index) :#nogil:
        '''
        This functions gets the FM-index value of a character at the specified position
        @param sym - the character to find the occurrence level
        @param index - the index we want to find the occurrence level at
        @return - the number of occurrences of char before the specified index
        '''
        cdef unsigned long binID = index >> bitPower
        cdef unsigned long compressedIndex = self.refFM_view[binID]
        cdef unsigned long bwtIndex = 0
        cdef unsigned long j
        for j in range(0, vcLen):
            bwtIndex += self.partialFM_view[binID,j]
        bwtIndex -= self.offsetSum
        
        cdef unsigned long ret = self.partialFM_view[binID,sym]
        
        cdef np.uint8_t prevChar = 255
        cdef np.uint8_t currentChar
        cdef unsigned long prevCount = 0
        cdef unsigned long powerMultiple = 1
        #cdef unsigned long powerMultiple = 0
        
        while bwtIndex + prevCount < index:
            currentChar = self.bwt_view[compressedIndex] & mask
            if currentChar == prevChar:
                prevCount += (self.bwt_view[compressedIndex] >> letterBits) * powerMultiple
                powerMultiple *= numPower
                #prevCount += <unsigned long>(self.bwt_view[compressedIndex] >> letterBits) << powerMultiple
                #powerMultiple += numberBits
            else:
                if prevChar == sym:
                    ret += prevCount
                
                bwtIndex += prevCount
                prevCount = (self.bwt_view[compressedIndex] >> letterBits)
                prevChar = currentChar
                powerMultiple = numPower
                #powerMultiple = numberBits
                
            compressedIndex += 1
        
        if prevChar == sym:
            ret += index-bwtIndex
        
        return ret
    
    cdef inline bwtRange getOccurrenceOfCharAtRange(tdbg self, unsigned long sym, bwtRange inRange) nogil:
        '''
        This functions gets the FM-index value of a character at the specified position
        @param sym - the character to find the occurrence level
        @param index - the index we want to find the occurrence level at
        @return - the number of occurrences of char before the specified index
        '''
        cdef unsigned long binID = inRange.l >> bitPower
        cdef unsigned long compressedIndex = self.refFM_view[binID]
        cdef unsigned long bwtIndex = 0
        cdef unsigned long j
        for j in range(0, vcLen):
            bwtIndex += self.partialFM_view[binID,j]
        bwtIndex -= self.offsetSum
        
        cdef bwtRange ret
        ret.l = self.partialFM_view[binID,sym]
        
        cdef np.uint8_t prevChar = 255
        cdef np.uint8_t currentChar
        cdef unsigned long prevCount = 0
        cdef unsigned long powerMultiple = 1
        
        while bwtIndex + prevCount < inRange.l:
            currentChar = self.bwt_view[compressedIndex] & mask
            if currentChar == prevChar:
                prevCount += (self.bwt_view[compressedIndex] >> letterBits) * powerMultiple
                powerMultiple *= numPower
            else:
                if prevChar == sym:
                    ret.l += prevCount
                
                bwtIndex += prevCount
                prevCount = (self.bwt_view[compressedIndex] >> letterBits)
                prevChar = currentChar
                powerMultiple = numPower
                
            compressedIndex += 1
        
        cdef unsigned long tempC = ret.l
        if prevChar == sym:
            ret.l += inRange.l-bwtIndex
        
        cdef unsigned long binID_h = inRange.h >> bitPower
        if binID == binID_h:
            #we can continue, just set this value
            ret.h = tempC
        else:
            #we need to load everything
            compressedIndex = self.refFM_view[binID_h]
            bwtIndex = 0
            for j in range(0, vcLen):
                bwtIndex += self.partialFM_view[binID_h,j]
            bwtIndex -= self.offsetSum
            
            ret.h = self.partialFM_view[binID_h,sym]
            
            prevChar = 255
            prevCount = 0
            powerMultiple = 1
        
        while bwtIndex + prevCount < inRange.h:
            currentChar = self.bwt_view[compressedIndex] & mask
            if currentChar == prevChar:
                prevCount += (self.bwt_view[compressedIndex] >> letterBits) * powerMultiple
                powerMultiple *= numPower
            else:
                if prevChar == sym:
                    ret.h += prevCount
                
                bwtIndex += prevCount
                prevCount = (self.bwt_view[compressedIndex] >> letterBits)
                prevChar = currentChar
                powerMultiple = numPower
                
            compressedIndex += 1
        
        if prevChar == sym:
            ret.h += inRange.h-bwtIndex
        
        return ret
    
    cpdef bint addTranscript(tdbg self, str s, str sID):
        '''
        This adds a transcript to our list
        @param s - the sequence to add
        @param sID - an identifier for the sequence we will use later
        @return - returns "True" if the sequence has been saved; if "False", either len(s) < k OR all counts were
            less than the threshold from before
        '''
        cdef bint stored = False
        cdef unsigned long sLen = len(s)
        
        cdef str rs = revComp(s)
        
        #make it mutable
        cdef bytearray bs = bytearray(s)
        cdef bytearray brs = bytearray(rs)
        
        cdef unsigned char [:] s_view = bs
        cdef unsigned char [:] rs_view = brs
        
        #we won't store anything that's obviously too small
        if sLen < self.k:
            return False
        
        cdef unsigned char [:] forwardKmer
        cdef unsigned char [:] revCompKmer
        
        cdef long prevNonZero = -1
        cdef long prevZero = -1
        cdef unsigned long fc, rc
        
        cdef unsigned long x, y
        
        cdef list connections
        cdef unsigned long pathCount
        
        cdef list changes = []
        cdef str correctedSeq
        
        for x in range(0, sLen-self.k+1):
            #do the forward
            #with nogil:
            forwardKmer = s_view[x:x+self.k]
            revCompKmer = rs_view[sLen-self.k-x:sLen-x]
            fc = self.countOccurrencesOfSeq(forwardKmer)
            rc = self.countOccurrencesOfSeq(revCompKmer)
        
            if fc > 0:
                stored = True
                #self.kmers[forwardKmer] = fc
                #self.kmers[s[x:x+self.k]] = fc
                
            if rc > 0:
                stored = True
                #self.kmers[revCompKmer] = rc
                #self.kmers[rs[sLen-self.k-x:sLen-x]] = rc
            
            if fc+rc < self.threshold:
                if prevZero != x-1:
                    #print 'Non-zero: '+str([prevZero+1, x])+','+bs[prevZero+1:x+self.k-1]
                    pass
                prevZero = x
            else:
                if prevZero == x-1:
                    if prevNonZero == -1:
                        #do something special we aren't ready for
                        pass
                    else:
                        #print 'end of prev', (bs[prevNonZero:prevNonZero+self.k] if prevNonZero != -1 else -1)
                        #print 'start of curr', (bs[x:x+self.k])
                        #allowedGap = (x-prevNonZero-1)+20; 20 is just a value I arbitrarily chose 
                        connections = self.connectKmers(bs[prevNonZero:prevNonZero+self.k], bs[x:x+self.k], (x-prevNonZero)+self.k)
                        pathCount = len(connections)
                        self.pathStats[pathCount] = self.pathStats.get(pathCount, 0)+1
                        
                        if pathCount > 0:
                            #while our path is too short, we go to the next one
                            #y = 0
                            #while y < pathCount and (len(connections[y]) < (x-prevNonZero)+self.k-20):
                            #    y += 1
                            
                            #if y < pathCount:
                            changes.append((prevNonZero, x+self.k, str(connections[0])))
                        
                prevNonZero = x
        #print
        
        cdef unsigned long start, end
        cdef str correction
        if stored:
            self.transDict[sID] = s
            
            correctedSeq = s
            for (start, end, correction) in reversed(changes):
                correctedSeq = correctedSeq[0:start]+correction+correctedSeq[end:]
            self.correctedDict[sID] = correctedSeq
        return stored
    
    cpdef dumpStats(tdbg self, logger):
        logger.info('Number of transcripts saved: '+str(len(self.transDict)))
        logger.info('Number of '+str(self.k)+'-mers saved: '+str(len(self.kmers)))
        logger.info('Path statistics: ')
        cdef unsigned long tot = 0
        for k in sorted(self.pathStats.keys()):
            logger.info(str(k)+'\t'+str(self.pathStats[k]))
            tot += self.pathStats[k]
        logger.info('Total\t'+str(tot))
    
    cpdef writeSeqs(tdbg self, fn):
        cdef unsigned long OFFSET = 50
        cdef str sID
        cdef str seq
        
        fp = open(fn, 'w+')
        for sID in sorted(self.correctedDict.keys()):
            fp.write('>'+sID+'\n')
            seq = self.correctedDict[sID]
            for x in range(0, len(seq), OFFSET):
                fp.write(seq[x:x+OFFSET]+'\n')
            
        fp.close()
    
    cdef list connectKmers(tdbg self, bytearray start, bytearray end, unsigned long expectedGap):
        #print 'connecting', start, end, allowedGap
        
        #initialize to our input kmer
        cdef list ret = []
        cdef list possBridges = [start]
        cdef unsigned long kmerLen = len(start)
        
        #set up some easy values
        cdef list validChars = ['A', 'C', 'G', 'T']
        cdef dict revCompDict = {'A':'T', 'C':'G', 'G':'C', 'T':'A'}
        cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] counts = np.zeros(dtype='<u8', shape=(len(validChars), ))
        cdef np.uint64_t [:] counts_view = counts
        
        #the minimum threshold needed for a path to be considered, 2 is really the lowest you'd ever want to set this
        cdef unsigned long BRIDGE_THRESHOLD = 2
        
        #maximum number of paths we will try to follow, increasing will theoretically find more at the cost of more work
        cdef unsigned long MAX_EXPLORED = 200
        
        #maximum number of paths we can have queued up, if we go over, this is like a highly over-represented k-mer region
        cdef unsigned long allowedGap = expectedGap+connectBuffer
        cdef unsigned long MAX_BRANCHED = 4*allowedGap
        
        #TODO: this should prob be dynamic or even a different static value
        cdef unsigned long overloadThreshold = 1000000
        
        #time to start exploring possible bridges
        cdef unsigned long explored = 0
        
        cdef bytearray currBridge
        cdef bytearray currKmer
        cdef bytearray revKmer
        
        cdef unsigned long i
        cdef str c
        
        cdef unsigned long maxPos
        cdef str maxSym
        
        cdef unsigned long currBridgeLen
        
        #while we have things to explore, and we haven't explored too many, and we don't have a ridiculous number of possibilities
        while len(possBridges) > 0 and explored < MAX_EXPLORED and len(possBridges) < MAX_BRANCHED:
            #get the bridge, the kmer, and the reverse kmer
            currBridge = possBridges.pop()
            currBridgeLen = len(currBridge)
            currKmer = currBridge[currBridgeLen-kmerLen:]
            revKmer = revComp_ba(currKmer)#MultiStringBWT.reverseComplement(currKmer)
            explored += 1
            
            
            #try to extend it on out
            #while len(currBridge) <= allowedGap and currKmer != end:
            while currBridgeLen <= allowedGap and currKmer != end:
                #get the counts for each possible extension
                maxPos = 0
                for i, c in enumerate(validChars):
                    #counts[i] = msbwt.countOccurrencesOfSeq(currKmer+c)+msbwt.countOccurrencesOfSeq(revCompDict[c]+revKmer)
                    counts_view[i] = (self.countOccurrencesOfSeq(currKmer+c)+
                                 self.countOccurrencesOfSeq(revCompDict[c]+revKmer))
                    if counts_view[i] > counts_view[maxPos]:
                        maxPos = i
                    
                #get the highest one
                #maxPos = np.argmax(counts)
                maxSym = validChars[maxPos]
                
                #make sure the highest is high enough for us to consider it 
                if counts_view[maxPos] >= BRIDGE_THRESHOLD:
                    #go through all the other possible extensions
                    for i, c in enumerate(validChars):
                        if i != maxPos and counts_view[i] >= BRIDGE_THRESHOLD and counts_view[i] < overloadThreshold:
                            #add the ones we aren't exploring right now if they're high enough
                            possBridges.append(currBridge+c)
                    
                    #make sure the highest isn't too high
                    if counts_view[maxPos] < overloadThreshold:
                        #this extension meets our requirement so shift over to loop back around
                        currBridge += maxSym
                        currBridgeLen += 1
                        currKmer = currKmer[1:]+maxSym
                        revKmer = revCompDict[maxSym]+revKmer[0:len(revKmer)-1]
                    else:
                        #we are toooo big, break out of this path
                        break
                else:
                    #our BEST doesn't pass the threshold on this path, stop following
                    break
            
            #our kmer is what we're searching for, store the bridge and look some more
            #if currKmer == end and len(currBridge) <= allowedGap and len(currBridge) >= expectedGap-connectBuffer:
            if currKmer == end and currBridgeLen <= allowedGap and currBridgeLen >= expectedGap-connectBuffer:
                ret.append(currBridge)
        
        #return all our possibilities
        #return ret
        #print 'found '+str(len(ret))+' possible connections'
        return ret
    
    cpdef np.ndarray countPileup(tdbg self, bytearray seq, long kmerSize):
        '''
        This function takes an input sequence "seq" and counts the number of occurrences of all k-mers of size
        "kmerSize" in that sequence and return it in an array. Automatically includes reverse complement.
        @param seq - the seq to scan
        @param kmerSize - the size of the k-mer to count
        @return - a numpy array of size (len(seq)-kmerSize+1) containing the counts
        '''
        cdef long seqLen = len(seq)
        cdef long numCounts = max(0, seqLen-kmerSize+1)
        cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] ret = np.zeros(dtype='<u8', shape=(numCounts, ))
        cdef np.uint64_t [:] ret_view = ret
        
        cdef bytearray subseq, subseqRevComp
        cdef bytearray revCompSeq = revComp_ba(seq)#MultiStringBWT.reverseComplement(seq)
        
        cdef unsigned long x
        for x in range(0, numCounts):
            subseq = seq[x:x+kmerSize]
            subseqRevComp = revCompSeq[seqLen-kmerSize-x:seqLen-x]
            ret_view[x] = self.countOccurrencesOfSeq(subseq)+self.countOccurrencesOfSeq(subseqRevComp)
        
        return ret
    
    
    '''
    Let's brainstorm what exactly we need stored in order to accomplish this task
    1) we want an overview of the TDBG; this is primarily so we can see other transcripts we are already aware of
    2) at some point we will need to know counts for each k-mer so we can figure out which to check for alternate paths
    3) once we have alternate paths, we have to somehow decide how to modify the transcripts
    '''
    
    cpdef addConnectedKmers(tdbg self, logger):
        logger.info('Finding connected k-mers...')
        self.addedKmers = {}
        
        '''
        cdef bwtRange kRange
        
        #TODO: make these parameters OR constants (in an enum)
        cdef unsigned long maximumPathExtension = 1000
        cdef unsigned long minThreshold = 5
        cdef float fracThreshold = .1
        
        cdef float currentThreshold
        cdef str c
        
        cdef str tID
        cdef str s, rs
        cdef unsigned long seqLen
        
        cdef unsigned long x
        cdef unsigned long totalCount
        
        for tID in sorted(self.transDict.keys()):
            #get the sequence in question
            s = self.transDict[tID]
            rs = revComp(s)
            seqLen = len(s)
            
            for x in range(0, sLen-self.k+1):
                forwardKmer = s[x:x+self.k]
                revCompKmer = rs[sLen-self.k-x:sLen-x]
                
                totalCount = self.kmers.get(forwardKmer, 0)+self.kmers.get(revCompKmer, 0)
                if totalCount > 0:
                    currentThreshold = max(fracThreshold*totalCount, minThreshold)
                    for c in validBases:
                        modKmer = 
                        revModKmer = 
        ''' 
        '''
        for kmer in self.kmers:
            #the current threshold is either a fraction of the counts OR at least 5
            currentThreshold = max(fracThreshold*self.kmers[kmer], minThreshold)
            
            for c in validBases:
                currKmer = kmer[1:]+c
                revCurrKmer = revComp(currKmer)
                
                if ((currKmer in self.kmers) or
                    (revCurrKmer in self.kmers)):
        '''         

cdef str complement = string.maketrans('ACGNT', 'TGCNA')
cdef inline str revComp(str seq):
    return seq[::-1].translate(complement)
cdef inline bytearray revComp_ba(bytearray seq):
    return seq[::-1].translate(complement)

#################################
#Parameters for a custom counting
#################################
cdef list validBases = ['A', 'C', 'G', 'T']
cdef np.ndarray numToChar = np.array([ord(c) for c in sorted(['$', 'A', 'C', 'G', 'N', 'T'])], dtype='<u1')
cdef np.uint8_t [:] numToChar_view = numToChar

cdef np.ndarray charToNum = np.zeros(dtype='<u1', shape=(256,))
cdef np.uint8_t [:] charToNum_view = charToNum
cdef unsigned long i
for i in range(0, vcLen):
    charToNum_view[numToChar_view[i]] = i

