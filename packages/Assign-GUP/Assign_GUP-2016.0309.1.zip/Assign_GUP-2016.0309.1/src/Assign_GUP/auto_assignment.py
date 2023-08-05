
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
automatic assignment of reviewers to proposals
'''


import history


class Auto_Assign(object):
    '''
    automatically assign reviewers to proposals
    
    :meth:`simpleAssignment`: assign the first two reviewers with the highest scores to *unassigned* proposals
    '''
    
    def __init__(self, agup):
        self.agup = agup
        self.scores = {}
        self.getScores()
    
    def getScores(self):
        '''
        generate the table of scores
        '''
        self.scores = {}
        for prop in self.agup.proposals:
            prop_id = prop.getKey('proposal_id')
            panel = {}
            for rvwr in self.agup.reviewers:
                full_name = rvwr.getFullName()
                score = int(100.0*prop.topics.dotProduct(rvwr.topics) + 0.5)
                panel[full_name] = score
            self.scores[prop_id] = panel
    
    def simpleAssignment(self):
        '''
        assign the first two reviewers with the highest scores to *unassigned* proposals
        
        * no attempt to balance assignment loads in this procedure
        * score must be above zero to qualify
        '''
        def sort_reviewers(scores):
            '''
            order the reviewers by score on this proposal
            '''
            xref = {}
            for who, score in scores.items():
                if score not in xref:
                    xref[score] = []
                xref[score].append(who)
            name_list = []
            for s, names in sorted(xref.items(), reverse=True):
                if s > 0:
                    name_list += names
            return name_list
        
        counter = 0
        for prop in self.agup.proposals:
            assigned = prop.getAssignedReviewers()
            if None not in assigned:
                continue    # all assigned, skip this proposal
            prop_id = prop.getKey('proposal_id')
            scores = self.scores[prop_id]
            
            # mark existing assigned reviewers to exclude further consideration, this round
            for role, full_name in enumerate(assigned):
                if full_name in prop.eligible_reviewers:
                    scores[full_name] = -1
            
            # order the reviewers by score on this proposal
            for full_name in sort_reviewers(scores):
                role = None
                if assigned[0] is None:
                    role = 0
                elif assigned[1] is None:
                    role = 1
                else:
                    break
                if role is not None:
                    assigned[role] = full_name
                    counter += 1
            
            for role, full_name in enumerate(assigned):
                prop.eligible_reviewers[full_name] = role + 1

        msg = 'Auto_Assign.simpleAssignment: '
        msg += str(counter)
        msg += ' assignment'
        if counter > 1:
            msg += 's'
        history.addLog(msg)
        return counter
