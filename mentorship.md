---
layout: page
title: Mentorship
permalink: /mentorship/
---

## My Mentors

<ul>
    <li>
    {% if mentor contains "orcid" %}
    <img src="https://orcid.org/sites/default/files/images/orcid_16x16(1).gif" alt="ORCID"/>
    <a href="https://orcid.org/{{ mentor.orcid }}">{{ mentor.name }}</a>
    {% else %}
    {% endif %}
    <ul>
        {% for role in roles %}
        <li>
        {{ role.name }} at {{ role.location }} from {{ role.start }} to {{ role.end}}
        </li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
</ul>

## Fraunhofer SCAI

During my master's and doctoral work at the Fraunhofer SCAI Department of
Bioinformatics from 2016-2019, I had the opportunity to recruit, mentor, and
work with many wonderful students:

- [Yojana Gadiya](https://orcid.org/0000-0002-7683-0452). Student Research
  Assistant. April 2019 - May 2019.
- [Trusha Adeshara](https://orcid.org/0000-0002-8929-4724). Student Research
  Assistant. April 2019 - May 2019.
- [Rana Aldisi](https://orcid.org/0000-0002-3034-9970). Student Research
  Assistant. July 2018 - March 2019. Master's Student. March 2019 -
  December 2019.
- [Lingling Xu](https://orcid.org/0000-0002-0303-8616).  Student Research
  Assistant. July 2018 - March 2019. Master's Student. March 2019 -
  December 2019.
- [Özlem Muslu](https://orcid.org/0000-0003-0408-6190). Master's Student.
  May 2018 - December 2018.
- [Kristian Kolpeja](https://orcid.org/0000-0001-9661-5277). Student Research
  Assistant. July 2018 - November 2018.
- [Esther Wollert](https://orcid.org/0000-0002-7128-929X).  Student Research
  Assistant. July 2018 - August 2019.
- [Sandra Spalek](https://orcid.org/0000-0002-6117-4413).  Student Research
  Assistant. July 2018 - August 2019.
- Keerthika Lohanadan. Student Research Assistant. July 2018 - September 2018.
- [Colin Birkenbihl](https://orcid.org/0000-0002-7212-7700). Student Research
  Assistant. July 2017 - October 2017.
- Aram Grigoryan. Student Research Assistant. July 2017 - December 2017.
