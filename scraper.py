#import our libraries
import scraperwiki
import mechanize 
import lxml.html

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#now create a function called scrape_table which isn't run until the end... 
#this gets passed an individual page (root) to scrape - look to see where it is created lower down
def scrape_table(root):
    #grab all table rows <tr> in table class="reports"
    rows = root.cssselect("table.tblSearchResults tr")
    #create an ID number set at 0 - will add 1 every time we store a record (below)
    idno = 0
    #for each row, loop through this
    #create a record to hold the data
    record = {}
    for row in rows:
        #create a list of all cells <td> in that row
        table_cells = row.cssselect("td")
        if table_cells: 
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
            record['Recipient'] = table_cells[0].text_content()
            record['Description'] = table_cells[1].text_content()
            #this line adds 1 to the ID no. we set at 0 earlier
            idno=idno+1
            record['ID'] = idno 
            record['Amount'] = table_cells[2].text_content()
            record['Date'] = table_cells[3].text_content()
            record['LA'] = table_cells[4].text_content()
            record['Distributing body'] = table_cells[5].text_content()
            #find any links <a ...
            table_cellsurls = table_cells[0].cssselect("a")
            #grab the href=" attribute of the first <a ... and store
            record['URL'] = table_cellsurls[0].attrib.get('href')
                # Print out the data we've gathered
            print record, '------------'
            # Save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.sqlite.save(["ID"], record)

br = mechanize.Browser()
response = br.open(lotterygrantsurl)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
print br.form

br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
br["ctl00$phMainContent$txtGrantDateFrom"] = "01/01/2014"
br["ctl00$phMainContent$txtGrantDateTo"]  = "20/01/2017"

#print the values being held by br
print br
response = br.submit()
#print response.read()
html = response.read()
print html
#ERROR GENERATED: XMLSyntaxError: None
root = lxml.html.fromstring(html)
# START scraping by running scrape_table function created above
scrape_table(root)
