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
<strong><a href="https://github.com/{{ entry.github }}">{{ entry.name }}</a></strong> <small style="color: #999">{{ entry.role }}</small><br />
{{ entry.description }}
</div>
{% endfor %}

## Databases

{% for entry in site.data.software %}
<div style="padding-bottom: 10px;">
<strong>
<a href="{% if entry contains "github" %}https://github.com/{{ entry.github }}{% else %}https://zenodo.org/record/{{ entry.zenodo }}{% endif %}">
{{ entry.name }}</a></strong> <small style="color: #999">{{ entry.role }}</small><br />
{% else $}
<strong><a href="https://github.com/{{ entry.github }}">{{ entry.name }}</a></strong> <small style="color: #999">{{ entry.role }}</small><br />

{{ entry.description }}
</div>
{% endfor %}


## Training

I care very deeply about reproducibility, especially in scientific software development. However,
this is not one of the core values taught by most PIs, nor are the core skills part of either scientific
or informatics curricula. I'm generating some resources to help fill that gap:

- [Blog: Dealing with Big Pull Requets]({% post_url 2020-03-20-how-to-fix-your-monolithic-pull-request %})
- [Blog: Flake8]({% post_url 2020-04-25-how-to-code-with-me-flake8 %})
- [Blog: Packaging]({% post_url 2020-06-03-how-to-code-with-me-organization %})
- [Blog: CLIs]({% post_url 2020-06-11-click %})
- [Video: Writing Reusable, Reproducible Python: Documentation, Packaging, Continuous Integration, and Beyond](https://www.youtube.com/watch?v=lo_g-GbYtaA)
- [GitHub: Using Flask, Celery, and Docker](https://github.com/cthoyt/flask-celery-docker-demo)
- [GitHub: Examples](https://github.com/cthoyt-teaches-reproducibility/)
