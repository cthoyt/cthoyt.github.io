---
layout: page
title: Software
permalink: /software/
---
I've created many open-source projects as well as made significant contributions to others:

{% for entry in site.data.software %}
<div style="padding-bottom: 10px;">
{% if entry contains "logo" %}
<img src="{{ entry.logo }}" alt="{{ entry.name }} Logo" style="float: left; max-height: 40px; max-width: 40px; margin-right: 15px" />
{% endif %}
<strong><a href="https://github.com/{{ entry.github }}">{{ entry.name }}</a></strong> <small style="color: #999">{{ entry.role }}</small>
{% if entry contains "github" %}
      <a href="https://github.com/in/{{ entry.github }}">
      <img alt="GitHub logo" src="/img/logos/github-icon.svg" width="16" height="16" />
      </a>
{% endif %}
{% if entry contains "wikidata" %}
    <a href="https://scholia.toolforge.org/topic/{{ entry.wikidata }}">
    <img alt="WikiData logo" src="/img/logos/wikidata_logo.svg" height="16" />
    </a>
{% endif %}
<br />
{{ entry.description }}
</div>
{% endfor %}

## Databases

I've created many databases myself through curation, automated assembly, and also by coordinating
others.

{% for entry in site.data.databases %}
<div style="padding-bottom: 10px;">
{% if entry contains "logo" %}
<img src="{{ entry.logo }}" alt="{{ entry.name }} Logo" style="float: left; max-width: 40px; margin-right: 15px" />
{% endif %}
<strong>
{% if entry contains "github" %}
<a href="https://github.com/{{ entry.github }}">{{ entry.name }}</a>
{% else %}
<a href="https://zenodo.org/record/{{ entry.zenodo }}">{{ entry.name }}</a>
{% endif %}
</strong> <small style="color: #999">{{ entry.role }}</small>
{% if entry contains "github" %}
      <a href="https://github.com/{{ entry.github }}">
      <img alt="GitHub logo" src="/img/logos/github-icon.svg" width="16" height="16" />
      </a>
{% endif %}
{% if entry contains "wikidata" %}
    <a href="https://scholia.toolforge.org/topic/{{ entry.wikidata }}">
    <img alt="WikiData logo" src="/img/logos/wikidata_logo.svg" height="16" />
    </a>
{% endif %}
<br />
{{ entry.description }}
</div>
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
advanced Python programming: https://youtube.com/playlist?list=PLPFmTfhIBiumfYT3rsa35fHJxabB78er1&si=rLUBLi4UvAmDFn0_
