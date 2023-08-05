import re


class Scraper(object):
    """ We scrape the website and store the information in the models. We save the urls
    and the previously modified time, so that if anything is updated, we may update our
    resources. We also don't want to peg the site too much, by being good webizens. """

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
                model_name = tds[0].text.strip()
                value = tds[1].text.strip()
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
            description = unicode(soup_element[1]).replace('\r', '').replace('\t', '').strip()
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
                name = anchor.text.replace("\n","").replace("\r","").replace("\t","").strip()
                href = anchor['href']
                # check if model has date information in another td
                years = -1
                if len(model_row.select('td')) > 1:
                    years = model_row.select('td')[1].text.strip().rstrip('-')
                if 'http' not in href:
                    yield [name, href, years]
            except:
                print 'Failed to parse model_row: ' + str(i) + ' for make: ' + make_name
