import re


class Scraper(object):
    """ We scrape the website and store the information in the models. We save the urls
    and the previously modified time, so that if anything is updated, we may update our
    resources. We also don't want to peg the site too much, by being good webizens. """
    wet_weight_name_regex = re.compile(r"Wet Weight", re.I)
    dry_weight_name_regex = re.compile(r"(Curb|Dry|Unladen) Weight", re.I)
    # weights saves in either kgs or lbs group
    weight_value_regex = re.compile(r"(?:(?P<kgs>[0-9]+)\s*Kg)|(?:(?P<lbs>[0-9]+)\s*lbs?)", re.I)

    @staticmethod
    def parse_model(soup, make_name='unknown make', model_name='unknown model'):
        """ Parse a model of bike """
        for strip_tag in ['script', 'style']:
            for s in soup(strip_tag):
                s.extract()
        # gather stats
        stats = []
        for i, table_row in enumerate(soup.select('table[cellspacing=1] tr')):
            try:
                tds = table_row.select('td')
                model_name = tds[0].text.strip() # e.g. Dry Weight or Capacity
                value = tds[1].text.strip() # e.g. 400 lbs or 410 lbs, 200 kg
                # scrape and correct for weight. lbs vs kgs, dry vs wet
                md = re.match(Scraper.dry_weight_name_regex, model_name)
                if re.match(Scraper.wet_weight_name_regex, model_name) or md:
                    model_name = 'weight'
                    match_weight_value = re.match(Scraper.weight_value_regex, value)
                    value = match_weight_value.group('lbs') or str(float(match_weight_value.group('kgs')) * 2.2)
                    if md: # add 10% for dry weight. who knows weights so lame.
                        value = str(float(value) * 1.1)
                stats.append([model_name, value])
                table_row.extract()
            except:
                print 'Failed to parse table_row: ' + str(i) + ' for make/model: ' + make_name + '/' + model_name
        if stats and stats[0]:
            model_name = stats[0][1]
        # extract description
        description = ''
        try:
            parent_element = soup.select('table[cellspacing=1]')[0]
            description_element = parent_element.parent.parent.parent.parent.parent
            description = unicode(description_element).strip()
        except:
            print 'Failed to parse description from make/model: ' + make_name + '/' + model_name
        return (model_name, description, stats)

    @staticmethod
    def parse_makes(soup):
        """ Parse all the makes (manufacturers) from the left bar """
        for make_anchor in soup.select('.leftMenu_container > a'):
            make = make_anchor.text.strip()
            href = make_anchor['href']
            yield [make, href]

    @staticmethod
    def parse_make(soup, recursive=False, name='unknown make'):
        """ Parse make (manufacturer) page

        Args:
            recursive: Boolean representing if each child page should also be parsed
        """
        for strip_tag in ['script', 'style']:
            for s in soup(strip_tag):
                s.extract()
        # grab models from each page
        models = list(Scraper.parse_make_models(soup, name))
        pages = Scraper.parse_make_pages(soup)
        # scrape make description
        description = ''
        try:
            soup_element = soup.select('div > table > tr div')
            description = Scraper.prettify(unicode(soup_element[1]), False)
        except:
            print 'Failed to parse description for make: ' + name
        return (models, description, pages)

    @staticmethod
    def parse_make_pages(soup):
        """ Generate list of pages, e.g. 1, 2, 3, 4 """
        pages = []
        for anchor in soup.select('p > font > a'):
            href = anchor['href']
            if 'model' not in href and 'http' not in href:
                pages.append(href)
        return set(pages)

    @staticmethod
    def parse_make_models(soup, make_name='unknown make'):
        """ Parse all the make's models on a given page. """
        for i, model_row in enumerate(soup.select('div > table > tr div > table > tr')):
            try:
                anchor = model_row.select('a')[0]
                name = Scraper.prettify(anchor.text)
                href = anchor['href']
                # check if model has date information in another td
                year_start = year_end = ''
                if len(model_row.select('td')) > 1:
                    years = model_row.select('td')[1].text.strip()
                    if years.endswith('-'):
                        years = years.rstrip('-')
                    if years.isdigit():
                        year_start = year_end = int(years)
                    elif '-' in years:
                        year_start, year_end = years.split('-')
                        if len(year_end) == 2:
                            year_end = ('20' if 1900 + int(year_end) < int(year_start) else '19') + year_end
                if 'http' not in href:
                    yield [name, href, year_start, year_end]
            except:
                print 'Failed to parse model_row: ' + Scraper.prettify(model_row.text) + ' for make: ' + make_name

    @staticmethod
    def prettify(text, removeNewlines=True):
        """ Remove obnoxious newlines tabs and strip """
        text = text.replace("\n", " ") if removeNewlines else text
        return text.replace("\r", " ").replace("\t", " ").strip()
