# Hinglish Notes

While learning Hindi the past few years, it's been interesting to wonder about the differences between `Pure Hindi` ( शुद्ध हिंदी ) and the hindi english hybrid known as `Hinglish`.

In modern day when watching TV or listening to people speak, I almost always hear people use Hinglish.

This document contains some notes and observations on this topic. 


## Hinglish Compound Verbs I've encountered

In English we often turn nouns into verbs in English by adding verb endings to it. E.g. `Googl-ing`, `Uber-ed`, etc. 

The same can be done for Hindi.

Trying to formalize this in a Backus–Naur style inspired formula I get

```
    NEW_VERB :== <NOUN> + <HINDI_VERB>
    
    where NOUN ∈ { nouns in Hindi}
          HINDI_VERB ∈ { subset of verbs used in hindi करना, होना,... }
```

So for example:

काम - (kaam) - is the hindi noun for `work`.

करना - (karna) - the verb `to do`.

so `काम` + `करना`  produces the verb `काम करना` which means `to work`. 

You can then conjugate and use `काम करना` as a verb by simply conjugating the `करना` part as you normally would. 
So if the past participle of `करना` is `किया` like in the sentence

```
मैंने यह कल किया।  - I did it yesterday
```

Then the past participle of `काम करना` is just `काम किया`.

```
मैंने कल काम किया। - did the work yesterday
```

This grammar point in Hindi is often classified as `compound verbs` in Hindi textbooks.

There are certain rules as to which Hindi verbs you can use for `HINDI_VERB` in the formula above. In general the most often used verbs are करना (to do) and होना (to be).

The cool thing about colloquial Hindi is you can extend 

```
NOUN ∈ { nouns in Hindi}
```

to 

```
NOUN ∈ { nouns in Hindi AND some nouns from English, Farsi, Arabic }
```

The words from English, Farsi, etc are called `loanwords`.

Below is a running list of Hinglish Compound verbs where the noun is a loanword from English:

* `use` करना - can be used in place of इस्तेमाल करना. Interestingly इस्तेमाल is also a load word from Arabic. The original Sanskrit derived word `उपयोग` can also be used उपयोग करना ( 9/21/2025 )
