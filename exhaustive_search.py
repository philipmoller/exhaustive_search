import numpy
import math

"""
self.pos = [[[40, -12.5],[50,0]],       #PCB
            [[50,-12.5],[47.5,-1.75]],  #SW1
            [[55,-12.5],[50.25,-1.75]], #SW2
            [[60.5,-12.5],[49,1]],      #CLK
            [[64.5,-5],[52.75,0]],      #TRN
            [[64.5,0],[52.75,0]],       #BRC
            [45.5,12.5],              #Gripper
            [54.5,12.5],              #Screwgun
            [52.75,2.25],             #F1
            [52.75,-2.25]]            #F2
"""

class Searcher():
    def __init__(self):
        self.seq0 = [0]
        self.seq1 = []
        self.seq2 = []
        self.seq3 = []
        self.seq4 = []
        self.seq5 = []
        self.seq6 = []
        self.seq7 = []
        self.seq8 = []
        self.current_seq = []

        self.p_chart = [[],[0],[0],[0],[0],[4],[5],[5]]
        self.component_list = [0,1,2,3,4,5,6,7]
        self.seqs = []

        self.pos = [[[40, -12.5],[50,0]],       #PCB
                    [[50,-12.5],[47.5,-1.75]],  #SW1
                    [[55,-12.5],[50.25,-1.75]], #SW2
                    [[60.5,-12.5],[49,1]],      #CLK
                    [[64.5,-5],[52.75,0]],      #TRN
                    [[64.5,0],[52.75,0]],       #BRC
                    [52.75,2.25],             #F1
                    [52.75,-2.25],            #F2
                    [54.5,10]]              #Screwgun

        self.home_pos = [50,0]


    def possible(self, component, current_seq, p_chart):
        parent = p_chart[component]
        if parent[0] in current_seq and component not in current_seq:
            return True
        else:
            return False

    def euc(self, a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def search(self):
        for x in range(1,len(self.component_list)):
            self.current_seq = self.seq0.copy()
            if self.possible(x,self.current_seq,self.p_chart):
                self.current_seq.append(x) # [0,1]
                self.seq1 = self.current_seq.copy() # [0,1]

                for y in range(1,len(self.component_list)):
                    self.current_seq = self.seq1.copy() # [0,1]
                    if self.possible(y,self.current_seq,self.p_chart):
                        self.current_seq.append(y) # [0,1,2]
                        self.seq2 = self.current_seq.copy() # [0,1,2]

                        for z in range(1,len(self.component_list)):
                            self.current_seq = self.seq2.copy()
                            if self.possible(z,self.current_seq,self.p_chart):
                                self.current_seq.append(z)
                                self.seq3 = self.current_seq.copy()

                                for v in range(1,len(self.component_list)):
                                    self.current_seq = self.seq3.copy()
                                    if self.possible(v,self.current_seq,self.p_chart):
                                        self.current_seq.append(v)
                                        self.seq4 = self.current_seq.copy()

                                        for r in range(1,len(self.component_list)):
                                            self.current_seq = self.seq4.copy()
                                            if self.possible(r,self.current_seq,self.p_chart):
                                                self.current_seq.append(r)
                                                self.seq5 = self.current_seq.copy()

                                                for s in range(1,len(self.component_list)):
                                                    self.current_seq = self.seq5.copy()
                                                    if self.possible(s,self.current_seq,self.p_chart):
                                                        self.current_seq.append(s)
                                                        self.seq6 = self.current_seq.copy()

                                                        for t in range(1,len(self.component_list)):
                                                            self.current_seq = self.seq6.copy()
                                                            if self.possible(t,self.current_seq,self.p_chart):
                                                                self.current_seq.append(t)
                                                                self.seq7 = self.current_seq.copy()

                                                                if self.current_seq not in self.seqs:
                                                                    self.seqs.append(self.current_seq)

    def add_tool_change(self, seqs):
        with_toolchange = []
        for i in seqs:
            i.insert(6,8)
            with_toolchange.append(i)
        return with_toolchange

    def find_good_ones(self, seqs): # the good ones are the ones ending in either either [6,7] or [7,6]
        good_seqs = []
        for i in seqs:
            if i[6:] == [6,7] or i[6:] == [7,6]:
                good_seqs.append(i)
        return good_seqs

    def distances(self, seqs):
        min_dist = 1000
        best_seq = []
        dists = []
        for i in seqs:
            dist = self.seq_dist(i)
            if dist < min_dist:
                min_dist = dist
                best_seq = i

        print("Best sequence: {}\nWith total distance: {}".format(best_seq,min_dist))

    def seq_dist(self,seq):
        accum = 0
        prev_pos = self.home_pos
        for i in range(len(seq)):
            action = int(seq[i])
            if action < 6: # If pick and place
                d1 = self.euc(prev_pos, self.pos[action][0])
                d2 = self.euc(self.pos[action][0], self.pos[action][1])
                accum += (d1+d2)
                prev_pos = self.pos[action][1]
            elif action == 8:
                dist = self.euc(prev_pos, self.pos[8])
                accum += dist
                prev_pos = self.pos[8]
            else: # If fasten
                dist = self.euc(prev_pos, self.pos[action])
                accum += dist
                prev_pos = self.pos[action]
        return accum

s = Searcher()
s.search()
good_ones = s.find_good_ones(s.seqs)
with_toolchange = s.add_tool_change(good_ones)
s.distances(with_toolchange)









#
