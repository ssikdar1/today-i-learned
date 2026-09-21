# Hinglish Notes

While learning Hindi the past few years, it's been interesting to wonder about the differences between `Pure Hindi` ( शुद्ध हिंदी ) and the hindi english hybrid known as `Hinglish`.

In modern day when watching TV or listening to people speak, I almost always hear people use Hinglish.

This document contains some notes and observations on this topic. 


## Hinglish Compound Verbs I've encountered

In English we often turn nouns into verbs in English by adding verb endings to it. E.g. `Googl-ing`, `Uber-ed`, etc. 

Bengali and Hindi also create new verbs with nouns.

Trying to write this in a Backus–Naur style formula I get

```
    NEW_VERB :== <NOUN> + <HINDI_VERB>
    
    where NOUN ∈ {All nouns in Hindi}
          HINDI_VERB ∈ { subset of verbs user in hindi करना, होना,... }
```

So for example:

काम - (kaam) - is the hindi noun for `work`
करना - (karna) - the verb `to do`

so काम + करना  produces काम करना the verb `to work`.

There are certain rules as to which Hindi verbs you can use for `HINDI_VERB` in the formula above. In general the most often used verbs are करना (to do) and होना (to be).

The cool thing in colloquial Hindi is you will see many English, Farsi, Arabic nouns being used for the `NOUN` part in the formula.

For Example:

* `use` करना - can be used in place of इस्तेमाल करना. Interestingly इस्तेमाल is also a load word from Arabic. The original Sanskrit derived word `उपयोग` can also be used उपयोग करना ( 9/21/2025 )
