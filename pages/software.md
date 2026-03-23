---
layout: page
title: Software
permalink: /software/
---

I've created many open-source projects as well as made significant contributions
to others:

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

I've created many databases myself through curation, automated assembly, and
also by coordinating others.

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
