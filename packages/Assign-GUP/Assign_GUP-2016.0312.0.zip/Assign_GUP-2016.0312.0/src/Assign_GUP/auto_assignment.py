
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
automatic assignment of reviewers to proposals
'''


import history

SCORE_EXCLUDED = -2
SCORE_ALREADY_ASSIGNED = -1


class Auto_Assign(object):
    '''
    automatically assign reviewers to proposals
    
    :meth:`simpleAssignment`: assign the first two reviewers with the highest scores to *unassigned* proposals
    '''
    
    def __init__(self, agup):
        self.agup = agup
    
    def getScores(self, prop):
        '''
        generate scores for this proposal
        '''
        exclusions = prop.getExcludedReviewers(self.agup.reviewers)
        panel_scores = {}
        for rvwr in self.agup.reviewers:
            full_name = rvwr.getFullName()
            if full_name in exclusions:
                score = SCORE_EXCLUDED
            else:
                score = int(100.0*prop.topics.dotProduct(rvwr.topics) + 0.5)
            panel_scores[full_name] = score
        return panel_scores
    
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
            # check for any existing assignments
            assigned = prop.getAssignedReviewers()
            if None not in assigned:
                continue    # all assigned, skip this proposal

            scores = self.getScores(prop)
            
            # mark existing assigned reviewers to exclude further consideration, this round
            for role, full_name in enumerate(assigned):
                if full_name in prop.eligible_reviewers:
                    scores[full_name] = SCORE_ALREADY_ASSIGNED
            
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
                if None not in assigned:
                    break    # all assigned, move to next proposal
            
            for role, full_name in enumerate(assigned):
                prop.eligible_reviewers[full_name] = role + 1

        msg = 'Auto_Assign.simpleAssignment: '
        msg += str(counter)
        msg += ' assignment'
        if counter > 1:
            msg += 's'
        history.addLog(msg)
        return counter
