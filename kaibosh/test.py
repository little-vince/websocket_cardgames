from game import KaiboshGame, OutOfTurn, GameProcedureError
from cardgame.deck import Suits, Values, Card
from player import Player

def test_setup():
    g = KaiboshGame()
    p1 = Player('Alice', g)
    p2 = Player('Bob', g)
    p3 = Player('Chuck', g)
    p4 = Player('Dan', g)
    assert g.state == 'add_player'
    g.add_player(p1, p1)
    g.add_player(p2, p2)
    g.add_player(p3, p3)
    g.add_player(p4, p4)
    assert g.state == 'bid'
    p1_card = Card(Values['A'], Suits['Hearts'])
    p2_card = Card(Values['K'], Suits['Hearts'])
    p3_card = Card(Values['Q'], Suits['Clubs'])
    p4_card = Card(Values['10'], Suits['Spades'])
    p1.hand = []
    p2.hand = []
    p3.hand = []
    p4.hand = []
    for _ in xrange(6):
        p1.hand.append(p1_card)
        p2.hand.append(p2_card)
        p3.hand.append(p3_card)
        p4.hand.append(p4_card)
    p1.bid(0)
    p2.bid(1)
    p3.bid(2)
    p4.bid(3)
    assert g.high_bid == (p4, 3)
    assert g.state == 'name_trump'
    try:
        p4.name_trump('fred')
        assert False, 'Should raise game proc error'
    except GameProcedureError:
        assert True
    p4.name_trump(Suits['Hearts'])
    return
    assert g.state == 'play_card'
    assert g.next_player == p1
    p1.play_card(p1_card)
    try:
        p1.play_card(p1_card)
        assert False, 'Out of turn not raised'
    except OutOfTurn:
        assert True
    p2.play_card(p2_card)
    p3.play_card(p3_card)
    p4.play_card(p4_card)
    assert g.tricks_won[p1] == 1
    assert g.next_player == p1
    for i in xrange(12):
        p1.play_card(p1_card)
        p2.play_card(p2_card)
        p3.play_card(p3_card)
        p4.play_card(p4_card)
    assert g.state == 'bid'
    assert p1.score == 14
    assert p2.score == 14
    assert p3.score == 1
    assert p4.score == 1