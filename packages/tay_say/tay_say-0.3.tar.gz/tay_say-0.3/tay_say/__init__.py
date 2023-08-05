__author__ = 'dev3l'

import random


def print_lyric():
    album_taylor_swift = set()
    add_tim_mcgraw(album_taylor_swift)
    print(random.choice(tuple(album_taylor_swift)))


def add_tim_mcgraw(album_taylor_swift):
    # "Tim McGraw"
    album_taylor_swift.add('He said the way my blue eyes shined, put those Georgia stars to shame that night')
    album_taylor_swift.add('I said, "That''s a lie."')
    album_taylor_swift.add('Just a boy in a Chevy truck, That had a tendency of gettin'' stuck, On back roads at night')
    album_taylor_swift.add('And I was right there beside him all summer long, And then the time we woke up to find '
                           'that summer gone')
    album_taylor_swift.add('But when you think Tim McGraw, I hope you think my favorite song, The one we danced to '
                           'all night long,The moon like a spotlight on the lake')
    album_taylor_swift.add('When you think happiness, I hope you think that little black dress')
    album_taylor_swift.add('Think of my head on your chest, And my old faded blue jeans')
    album_taylor_swift.add('When you think Tim McGraw, I hope you think of me')
    album_taylor_swift.add('September saw a month of tears, And thankin'' God that you weren''t here, To see me '
                           'like that')
    album_taylor_swift.add('But in a box beneath my bed, Is a letter that you never read, From three summers back')
    album_taylor_swift.add('It''s hard not to find it all a little bitter sweet, And lookin'' back on all of that, '
                           'it''s nice to believe')
    album_taylor_swift.add('And I''m back for the first time since then')
    album_taylor_swift.add('I''m standin'' on your street, And there''s a letter left on your doorstep')
    album_taylor_swift.add('And the first thing that you''ll read is:, When you think Tim McGraw, I hope you think my '
                           'favorite song')
    album_taylor_swift.add('Someday you''ll turn your radio on, I hope it takes you back to that place')
    album_taylor_swift.add('I hope you think of me, Oh, think of me, Mmmm')


if __name__ == "__main__":
    print_lyric()
