def card_Names():
    suits = ['d', 'h', 'c', 's']
    cards = []

    for card_num in range(1, 14):
        for card_suit in suits:
            str_card = str(card_num) if card_num > 9 else '0' + str(card_num)
            cards.append(str_card + card_suit)

    return cards


class Settings:
    imageNames = card_Names()
    imagePath = 'cards'
    imageBack = 'back01'
    imageType = '.gif'
    imageBottom = 'bottom02-n'
    imageResolution = (80, 122)
    doubleSpeed = 500
    startSpace = 10
    rowSpace = 30
    marginSpace = 20
    tileSmallSpace = 5
    tileLargeSpace = 15
