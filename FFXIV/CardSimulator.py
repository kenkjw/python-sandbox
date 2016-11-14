import random
simCount = 1000000
singleDPSFactor = 1./5
balanceFactor = 0.2
arrowFactor = 0.07
expandFactor = 0.5
extendFactor = 2.
enhanceFactor = 1.5


totalDPS = 0.



def use(card):
    global totalDPS
    global RR
    dpsInc = 0.
    if card == 1:
        dpsInc = balanceFactor
    elif card == 3:
        dpsInc = arrowFactor

    if RR == 1:
        dpsInc *= expandFactor
    elif RR == 2:
        dpsInc *= singleDPSFactor * extendFactor
    elif RR == 3:
        dpsInc *= singleDPSFactor * enhanceFactor
    elif RR == 0:
        dpsInc *= singleDPSFactor
    totalDPS += dpsInc
    RR = 0


def royalRoad(card):
    global RR
    if card <= 2:
        RR = 3
    elif card <= 4:
        RR = 2
    else:
        RR = 1

def spread(card):
    global spreadCard
    spreadCard = card


def performAction(card):
    global spreadCard
    action = actionDecisionTable[spreadCard][RR][card]
    if action == 1:
        use(card)
    elif action == 2:
        royalRoad(card)
    elif action == 3:
        spread(card)
    elif action == 4:
        royalRoad(card)
        use(spreadCard)
        spreadCard = 0

def drawCard():
    card = random.randint(1,6)
    redraw = redrawDecisionTable[spreadCard][RR][card]
    if redraw == 0:
        oldcard = card
        card = random.randint(1,5)
        if card >= oldcard:
            card += 1
    return card

"""
0 - Discard                 
1 - Use                 
2 - RR                  
3 - Spread              
4 - RR then Spread      
                        
Cards   
1 - Balance
2 - Bole
3 - Arrow
4 - Spear
5 - Ewer
6 - Spire

RR
0 - None
1 - Expand
2 - Extend
3 - Enhance
"""

actionDecisionTable = [[
## No card spread table
[0,3,2,1,2,2,2],    # No RR
[0,1,0,1,0,0,0],    # Expand
[0,3,0,1,0,2,2],    # Extend
[0,3,0,1,0,2,2]     # Enhance
],
[
## Balance spread table
[0,1,0,1,0,4,4],    # No RR
[0,1,0,0,0,0,0],    # Expand
[0,1,0,1,0,4,4],    # Extend
[0,1,0,1,0,4,4]     # Enhance
]
]

"""
0 = redraw
1 = hold
"""

redrawDecisionTable = [[
## No card spread table
[0,1,0,0,0,0,0],    # No RR
[0,1,0,1,0,0,0],    # Expand
[0,1,0,0,0,0,0],    # Extend
[0,1,0,0,0,0,0]     # Enhance
],
[
## Balance spread table
[0,1,0,0,0,1,1],    # No RR
[0,1,0,0,0,0,0],    # Expand
[0,1,0,0,0,1,1],    # Extend
[0,1,0,0,0,1,1]     # Enhance
]
]

### Testing card draw percentages
"""
spreadCard = 0
RR = 0
count = [0,0,0,0,0,0,0]
for draw in range(0,simCount):
    count[drawCard()] += 1.
print count
print [x / simCount for x in count]
"""

spreadCard = 0
RR = 0
for draw in  range(0,simCount):
    card = drawCard()
    performAction(card)

print totalDPS / simCount



