The continuous integration service runs tests that provide a technical,
objective implementation of the Bioregistry's code and data quality standards
any time the code or data in the repository are changed or suggestions for
changes are made in a pull request. The tests provide trustworthy, unopinionated
feedback that enables faster iteration and promotes trust in the project. The
continuous integration service also supports other actions, such automatically
generating pull requests for new prefix requests and other change suggestions
sent through the GitHub issue tracking system, which makes updating the
Bioregistry accessible to non-technical contributors. Second, the continuous
delivery service runs the aforementioned alignment workflows, generates all
derived artifacts, pushes changes to GitHub, and assigns a new version number on
a daily basis. Third, the continuous deployment service package deploys the code
and data to the Python Package Index (PyPI), builds a Docker container and
deploys to Docker Hub, and finally triggers a re-deployment of the website on a
daily basis. Combined, the continuous integration, delivery, and deployment
services allow contributors and consumers of the Bioregistry to more easily
propose improvements, review them as a community, and see them reflected in the
data and website without the need for manual intervention by the project team.
Using an entirely free, public, and open public infrastructure to do so promes
longevity and sustainability by mitigating the monetary requirements. Further,
the technical requirements of the deployment of the web service and hosting are
also minimized such that hosting costs around 33$/year and compute costs around
27$/year (details in the supplement).