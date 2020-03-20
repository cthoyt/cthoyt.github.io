---
layout: post
title: How to Fix Your Monolithic Pull Request
date: 2020-03-20 00:00:00 -0800
---
We've all been there. You started a new branch from master. You had a very
specific goal in mind, **The Original Goal**. You made a pull request (PR) to
go with it, too, **The Original Pull Request**. But then, you had an idea! And
also, someone on your team asked you to solve another problem! Now the original
code you wrote to address **The Original Goal**  relies on that code ... 
and now you've got dozens of files changed, hundreds of lines of diff, and
nobody (including you) can understand what you've done. Like I said, we've all
been there. Here's what you can do to fix it:

## 1. Stop and Relax

Don't do anything rash. Git is a pain to use, and you're going to have to
rely on it to keep a history for you of what you've done.

## 2. Summarize

First, you're going to have to take a big step back. Write a summary of all
the things you've done in **The Original Pull Request**. This should be about
*what* the PR does and *why* it does it. Of course it could vary depending on
the situation, but this summary shouldn't be about exactly how the PR does it,
because the implementation details are likely what lead to this situation in
the first place.

Keep in mind that every PR has a box at the top that's used to describe what's
in it. This is where you will put your summary.

## 3. Assessing Dependencies

Of all the things that **The Original Pull Request**, some of them are
self-contained, and some of them rely on each other. It was probably the
case that to accomplish **The Original Goal**, you had to address lots of
smaller goals. You probably also had to change lots of code and write new
code too.

Wouldn't it have been nice if all of these implementations were already done,
because then you could have just solved **The Original Goal** directly by
using/applying previous code. That's what we're going to aim for.

But first, you need to figure out which things you did relied on which other
ones, because you're going to break **The Original Pull Request** up until
it exactly matches up to addressing **The Original Goal**.
don't have any 

## 4. The Break Up

After you understand which parts of **The Original Pull Request** depend on
each other, pick one independent part of the code that accomplishes one
sub-goal. Since you're not doing this to be a martyr, and we all know git is
too complicated to *Do It Right*, you're going to copy/paste the files that
are related to this change to your desktop*.

## 5. Escape the Madness

Before continuing, you're going to make sure all of the code in your big messy
branch for **The Original Pull Request** is committed and pushed. Even though
we want to supersede what's there, it never hurts to keep track of your descent
into madness.

After there's nothing lying around, switch back to master. If your team has
taken good care of your repository, the master branch should be undisturbed
by the chaos you've created in **The Original Pull Request**. Make a new branch
from master, and name it appropriately for fixing the one sub-goal, from here
out known as **The Sub-Goal** that you identified in Step 4. Now you
can start updating the relevant files in your repository based on the files
you copied to your desktop. I suggest you don't copy/paste the contents of the
whole files, because you might have forgotten about something else you changed
in them. After all, you're reading my guide because this was a mess.

## 6. The New Pull Request

Once you've finished making the new branch for your independent part of
code that solves **The Sub-Goal**, you can make **The New Pull Request**.

You will now go through the entire process of writing a good summary of
this branch for your co-developers, you will get their feedback, you
will make updates, pass flake8, and so on. They will thank you for having
code that accomplishes one thing, and can be described simply. They will
thank you for not having too big of a diff, and for the things in the diff
all being relevant and important. Then you can merge this branch into master.

## 7. Newfound Wisdom

Throughout transferring the code for **The New Pull Request** you have probably
realized there are some things you did back in **The Original Pull Request**
that you could do better, and made some updates in the code in **The New
Pull Request** to reflect the wisdom you've gained along the way. That's great!
Congratulations!

After your team has approved **The New Pull Request**, you can merge it into
master and both delete the branch locally and on the remote. Then you should
switch back to the master branch. You can pull from master, and see your code
that solved **The Sub-Goal** reflected here.

## 8. The Hard Part

This is the hard part. Now you have to switch back to the branch for **The
Original Pull Request**. Now you have to update this branch from master. It's
going to be hard because now you've probably made different changes in **The
New Pull Request** than in **The Original Pull Request** so there will likely
be conflicts.

This is not a tutorial on how to solve merge conflicts. Use google to figure
that out

I can't understate: **do this part really well**. If you don't, then the
history in the original branch will be even more incomprehensible, and you
won't be able to tell if you lost any of your original work. Please, please,
please do this well.
 
P.S. Like I said before, don't be a martyr. Use tools like GitHub Desktop
and PyCharm to help you merge. I heard that the git CLI was *allegedly* created
by Linus Torvalds to slow other developers down.

Why are we going through all of this pain, rather than just pushing your team
to let you merge **The Original Pull Request**? The reason you have to do this
is because now all of the changes that addressed **The Sub-Goal** are part of
master, and are no longer part of the diff of **The Original Pull Request**.

Now you're one step closer to your team being able to understand, review, and
eventually merge **The Original Pull Request**.

## 9. The Frustrating Part

This is the frustrating part. After you've gone through all of that work to
split a tiny part of **The Original Pull Request** into a smaller, independent
pull request, you're not done. You will probably have to repeat steps 4-8 a
few times. You'll be tempted to throw away the branch for **The Original Pull
Request** and maybe start over.

Don't do that.

If you do, the same disorganization that lead to the mess of **The Original
Pull Request** might just slip back into whatever you do next. Even worse,
nobody else will be able to follow what you've done until now. 

So relax. This is going to take a few days. You're going to have to wait in
between several iterations for feedback. That's good. You need feedback. I
need feedback. We all need to practice getting it and giving it. Embrace the
opportunity to have your team help you improve your code, gain wisdom, and
make your contributions sustainable.

## Finishing Up

Eventually after several iterations of 4-9, you will have excised all of the
code that was important for **The Original Pull Request**, but not directly
accomplishing **The Original Goal**. As you removed independent parts, new
parts became independent themselves. Eventually, **The Original Pull Request**
will indeed match up exactly to **The Original Goal**, then you will be able
to come back to it for review and merging.

I understand this is a frustrating process. The purpose of these steps were
to help you think through a large piece of work you've done. You should be
proud that you've solved a complex problem with many intricate parts. It was
a lot of extra work to break it into many pull requests, and it might have
taken more of your time the first time working through this process, but in
the future, this might help you to start with small tasks rather than
addressing **The Original Goal** all at once. GitHub, for example, has an
issue tracker that is very helpful for this. I imagine that each issue should
correspond to a **Sub-Goal**, and that each should have exactly one PR that
addresses it. **The Original Goal** also deserves its own issue that points to
all of the issues for its sub-goals. Eventually you will address this with a
beautiful PR as well. Happy coding!

*If you're thinking, why don't I use cherry picking? If you know what cherry
picking is in the context of git (and also how to use it) then you probably
won't have the issue that prompted this blog post. But also, you should go
outside and pick some apples instead. Thanksgiving is never more than a few
hundred days away. It pays to be ready.
