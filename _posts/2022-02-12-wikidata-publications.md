## 1. Get content in EndNote XML

### Mendeley

[Mendeley](https://www.mendeley.com) is a less open citation manager owned by
Elsevier.

![](/img/wikidata-publications/mendley.png)

1. Select your publications
2. Right click on one of them
3. Select "export"
4. Choose "EndNote XML" as the filetype

## 2. Wikidata Integration

1. Create an account on [Wikidata](https://www.wikidata.org)
2. Store your account information in a configuration file
   at `~/.config/wikidata.ini` (where `~` means your home directory) that looks
   like:

   ```ini
   [wikidata]
   username = <your username here>
   password = <your password here>
   ```
3. Install [Python](https://www.python.org)
4. Run the following in your terminal:

   ```shell
   $ pip install citation-url[endnote]
   $ python -m citation_url.endnote <PATH TO YOUR ENDNOTE FILE>
   ```

