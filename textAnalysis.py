from textblob import TextBlob

text = '''
The Wee One, sat in her thinking place, puzzling. The purple hyacinths grew behind the moss covered rock she sat upon.   She was wondering if what she wanted to do was the right thing.  The longer she sat  in her thinking spot, the more she believed her idea was a good one. With her mind made up to do something she had never done before, the tiny fae  took flight on golden wings.

The fae flitted high into the air over the giant oaks and beyond the meadow.  She   fluttered down on the shore of the Sparkling Lake.  The Wee One walked from one stone to another, towards a very large rock.  It stood above the others, like a beacon.   She hesitated for a moment before whispering to the stone.    Suddenly it appeared to rise a little into the air.  

The Wee One walked under the stone.  A  golden box sat beneath it.  Quickly she lifted the lid of the box.   A Spirit filled the tiny crystal box the fae now held in her hand.  As the fae walked out from under the great stone, it settled down once again.  Without a moment’s hesitation she took to the air.  The fae flitted to her home in the ancient oak,  the crystal box now safely in her pocket.

Once home, the Wee One set the box on her  mushroom  table.   The fireflies gathered overhead.  The crystal box glittered like diamonds.    With trembling hands the Wee One opened the box.  Suddenly, before her stood a beautiful Spirit. “Will you help me?” The Wee One pleaded.  The Spirit did not  so  much speak, as it thought.  The Wee One knew, the Spirit would help her.  

 “We shall begin our journey now,” the spirit thought.  *poof*   In a twinkling, both the Spirit and the Wee One were transported to a city, in the Land of Real.

The Wee  One was not prepared for what she saw when they materialized.  It was a place   that had things called buildings.  Some of the buildings were as tall as the  Magic Mountain.  The air smelled odd and tasted funny.  There was not a tree or flower to be seen.  “I am frightened,” the fae whispered to the Spirit. “Is this where the children come from?” 

“Yes,”  the Spirit replied.  The Wee One shivered a bit, but the Spirit thought, “It will be okay, I’m with you.”  “Now quickly before it gets light open your pouch and do what you have come to do.”  

The Wee One reached deep into her pouch and gathered a handful of faerie dust.  With the Spirit by her side, she sprinkled the magic dust everywhere.  When they had finished the Spirit thought again.  “You have done well wee fae, for a first effort; now watch!”  Quietly,  a gentle rain began to fall.  The Spirit smiled, for the sprinkles began to grow flowers and trees everywhere they settled.

As the sun began to rise the city was ablaze with the color of beautiful flowers, twining green vines and stately trees.  From far beyond the  city  a rainbow appeared and held the city  in its arc.  The Spirit thought.  “It will make them happy wee fae, it truly  will.”   In a twinkle the Wee One and the Spirit sat together on a spire overlooking the city.   They   watched, as the children, the young and the old came out of their houses.  All looked about them with smiles and wonder.  The city was now bursting with  the beauty of flowers and the songs of birds in the young trees.

“It is time to go now,” the Spirit thought.  The Wee One nodded her head. *poof*  In a twinkle the two friends were back on the shore of the Sparkling Lake.   The Spirit returned to the golden box beneath the magic rock.  The Wee One sighed to see the Spirit go, but she knew the Spirit would always be present  for those in need of her.   

In a whisper the Wee One said, “thank you  for helping me... Hope.”'''

blob = TextBlob(text)

for sentence in blob.sentences:
    print(sentence.sentiment.polarity)