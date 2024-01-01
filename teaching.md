---
layout: page
title: Teaching
permalink: /teaching/
---
I've found teaching and tutoring to be a really rewarding experience.
It has been an opportunity to improve my own knowledge and communicate
topics that I know but can't be found on the internet or in a book. 

## Coursework

{% for entry in site.data.courses %}
<b>{{ entry.code }} {{ entry.name }}</b> ({{ entry.period.semester }} {{ entry.period.year }}; {{ entry.role }})<br />
{{ entry.level }} at {{ entry.location.university }} ({{ entry.location.department }}){% if entry.primary %}
primarily taught by <a href="{{ entry.primary.link }}">{{ entry.primary.name }}</a>.
{% endif %}<br />

{% if entry.presentation %}
{% if entry.date %}
Guest lecture on {{ entry.date.month }} {{ entry.date.day }}, {{ entry.date.year }}:
{% elsif entry.start %}
Guest lecture series from {{ entry.start.month }} {{ entry.start.day }} - {{ entry.end.month }} {{ entry.end.day }}, {{ entry.start.year }}:
{% else %}
Guest lecture:
{% endif %} <a href="{{ entry.presentation.url }}">{{ entry.presentation.name }}</a><br />
{% if entry.presentation.description %}
<i>Description</i>: {{ entry.presentation.description }}
{% endif %}
{% endif %}
{% if entry.description %}
<i>Description</i>: {{ entry.description }}
{% endif %}
{% endfor %}

## Scientific Programming Training

I care very deeply about reproducibility, especially in scientific software development. However,
this is not one of the core values taught by most PIs, nor are the core skills part of either
scientific or informatics curricula. I'm generating some resources to help fill that gap:

- [Blog: Dealing with Big Pull Requests]({% post_url 2020-03-20-how-to-fix-your-monolithic-pull-request %})
- [Blog: Flake8]({% post_url 2020-04-25-how-to-code-with-me-flake8 %})
- [Blog: Packaging]({% post_url 2020-06-03-how-to-code-with-me-organization %})
- [Blog: CLIs]({% post_url 2020-06-11-click %})
- [Blog: CLIs and Flask]({% post_url 2021-01-11-click-and-flask %})
- [Video: Writing Reusable, Reproducible Python: Documentation, Packaging, Continuous Integration, and Beyond](https://www.youtube.com/watch?v=lo_g-GbYtaA)
- [Video: Reusable, Reproducible, Useful Computational Science in Python (July 2021)](https://www.youtube.com/watch?v=f6brWkO9OiE)
- [GitHub: Using Flask, Celery, and Docker](https://github.com/cthoyt/flask-celery-docker-demo)
- [GitHub: Examples](https://github.com/cthoyt-teaches-reproducibility/)

Here's my playlist of videos to help people to go from intermediate to
advanced Python programming: <https://youtube.com/playlist?list=PLPFmTfhIBiumfYT3rsa35fHJxabB78er1&si=rLUBLi4UvAmDFn0_>

<iframe width="560" height="315" src="https://www.youtube.com/embed/videoseries?si=0NkCF7VbhxbC_ZDn&amp;list=PLPFmTfhIBiumfYT3rsa35fHJxabB78er1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>