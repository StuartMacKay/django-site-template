--------
  ToDo
--------

This file contains a bunch of ideas, etc. that eventually get refactored
into things to implement.

Everything right now is feature-complete or idea-complete. The voices site
is working exactly the way we want it.

If anything needs added next, it's an on-this-day feature and better ux/design.

At some point the feed stuff should be factored out but ONLY if it's needed
in another project. DO NOT do this just to get another project up on github.
It's a lot of work to make a project reusabled by others - Powers of 3 rule.
It's a much better use of time doing something new or learning something new.

Migrate the RSS models into a new app, in preparation for factoring it out.
https://realpython.com/move-django-model/#copy-the-data-to-the-new-model

Add Home, Contact to the site header?

Look at existing tags

Add a switch to Feed to selectively set tags from the tags for an Entry.
Would work for Peter Bell.

Add an Alias table for tags? Allow the alias to be None so it can filter
out tags like "Uncategorized" Just an idea, probably not useful/practical,

Add a custom page to browse Chris Cairns cartoons?

---------
  Later
---------

If ever,

- Add sorl-thumbnail to show icons for Sources and Articles.

  Cache the images using Redis or memcached.

  thumbnail images - would need to be scraped from the site if the feed
  is from wordpress <generator> tag.

  Some useful info,
  https://www.umaryland.edu/cpa/toolbox/web-image-specifications-cheat-sheet/
  https://www.techsmith.com/blog/youtube-thumbnail-sizes/
  http://tim-stanley.com/post/standard-web-digital-image-sizes/
  https://medium.com/hceverything/applying-srcset-choosing-the-right-sizes-for-responsive-images-at-different-breakpoints-a0433450a4a3
  https://github.com/jazzband/sorl-thumbnail
  https://ogp.me/
  https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary-card-with-large-image

  Add an icon for an Article
  Add an icon for a Source
  Display the Source icon when the Article does not have one
  Display a default icon when the Source does not have one

- Add more blocks to templates

- Enable the check-untyped-defs flag
  https://mypy.readthedocs.io/en/stable/command_line.html#untyped-definitions-and-calls
  reorg the code for confirming and cancelling subscriptions to deal with mypy issues

- Add different views and template for different layouts.

  Calendar list - the version we have now.
  Magazine - like Holyrood Magazine or Zero Hedge with thumbnails
