---
layout: page
title: Software
permalink: /software/
---
I've worked on several open source projects, and still do quite a bit of maintenance on them:

{% for entry in site.data.software %}
<div style="padding-bottom: 10px;">
{% if entry contains "logo" %}
<img src="{{ entry.logo }}" alt="{{ entry.name }} Logo" style="float: left; max-height: 40px; max-width: 40px; margin-right: 15px" />
{% endif %}
<strong><a href="https://github.com/{{ entry.github }}">{{ entry.name }}</a></strong><small>{{ entry.role }}</small><br />
{{ entry.description }}
</div>
{% endfor %}

## Training

I care very deeply about reproducibility, especially in scientific software development. I've
created several resources including blog posts, videos, and repositories.

- [Blog: Dealing with Big Pull Requets]({% post_url 2020-03-20-how-to-fix-your-monolithic-pull-request %})
- [Blog: Flake8]({% post_url 2020-04-25-how-to-code-with-me-flake8 %})
- [Blog: Packaging]({% post_url 2020-06-03-how-to-code-with-me-organization %})
- [Blog: CLIs]({% post_url 2020-06-11-click %})
- [Video: Writing Reusable, Reproducible Python: Documentation, Packaging, Continuous Integration, and Beyond](https://www.youtube.com/watch?v=lo_g-GbYtaA)
- [GitHub: Using Flask, Celery, and Docker](https://github.com/cthoyt/flask-celery-docker-demo)
- [GitHub: Examples](https://github.com/cthoyt-teaches-reproducibility/)
