---
layout: post
title: Some Haskell I Tried to Write
date: 2024-09-27 12:49:00 +0200
author: Charles Tapley Hoyt
tags:
  - Haskell
  - JATS
  - Publishing
  - Pandoc
---

I'm working through making a contribution to [pandoc](https://github.com/jgm/pandoc)
that adds first-class support for author role annotations using the
[Contribution Role Taxonomy (CRediT)](https://credit.niso.org/contributor-roles)
and also outputs compliant [Journal Publishing Tag Set (JATS)](https://jats.nlm.nih.gov/publishing/)
XML. This has lead me down a (losing) journey with learning the Haskell programming language,
so I thought I would post a short note on a function I tried to understand.

For some context, the first stream of changes I sent were in
[jgm/pandoc #10153](https://github.com/jgm/pandoc/pull/10153). I have done some in-place squashes
on the git history, so apologies to future readers if this isn't a helpful thread.
I appreciated the help from Pandoc's maintainer John MacFarlane, but he suggested I add
the following code and I just don't know enough Haskell to make sense of it:

```haskell
addCreditName :: M.Map Text Text -> M.Map Text Text
addCreditName rolemap =
  case M.lookup "credit-name" rolemap of
    Just _ -> rolemap
    Nothing -> maybe id (M.insert "credit-name")
      (M.lookup "credit-id" rolemap >>= flip M.lookup creditNames)
```

The goal was actually pretty simple. I have a dictionary that maybe has a `credit-name`
key. If it does, then we're done. If not, and it has a `credit-id` key, get the value
out of that and look up the `credit-name` using an external `creditNames` dictionary.
The problem is, I can't understand this without going on a massive deep-dive on Haskell
to actually understand the way Haskell programs treat function calls,
monads (which is a yo-dawg in the category of jokes), and function polymorphisms.

One thing to keep in mind is that Haskell is a functional programming language
and everything is supposed to be immutable. This means that mapping insertion operations
(`M.insert`) are returning a new dictionary. That made it possible to at least try
a more verbose way of doing what I needed to.

I like Haskell's `case` statement and first-class notion of optionals, so I thought
I'd try re-writing this code from above in a bit more straight-forward way:

```haskell
addCreditName :: M.Map Text Text -> M.Map Text Text
addCreditName role =
  -- Try looking if there's a "credit-name" key in the role dictionary
  case M.lookup "credit-name" role of
    -- If there's already an explicitly specified "credit-name"
    -- key in the role dictionary, then we don't have to do anything
    Just _ -> role
    Nothing ->
      case M.lookup "credit-id" role of
        -- If there isn't already a "credit-id" key in the role
        -- dictionary, then we aren't able to do anything
        Nothing -> role
        Just creditIdentifier ->
          -- Try looking up the value from the "credit-id" key, which
          -- we stored in the `creditIdentifier` variable, is in the
          -- creditNames dictionary, which is defined as a constant above
          case M.lookup creditIdentifier creditNames of
            -- If the credit-id value from the role dictionary is not
            -- in the creditNames lookup dictionary, then we can't do anything
            Nothing -> role
            -- If the credit-id value from the role dictionary is in
            -- the creditNames lookup dictionary, insert it back into the
            -- role dictionary under the "credit-name" key and return
            Just creditName -> M.insert "credit-name" creditName role
```

The funny thing is, I have been called out before on increasing confusion
by getting tricky when writing Python code. I guess I had it coming!
 