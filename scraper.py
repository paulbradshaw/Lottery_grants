#import our libraries
import scraperwiki
import mechanize 
import lxml.html

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#now create a function called scrape_table which doesn't run until later... 
#this gets passed an individual page (root) to scrape - look to see where it is created lower down
def scrape_table(root):
    #grab all table rows <tr> in table class="tblSearchResults"
    rows = root.cssselect("table.tblSearchResults tr")
    #create an ID number set at 0 - will add 1 every time we store a record (below)
    idno = 0
    #create a record to hold the data
    record = {}
    #for each row, loop through this
    for row in rows:
        #create a list of all cells <td> in that row
        table_cells = row.cssselect("td")
        if table_cells: 
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'recipient' and so on
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
            # Save the record to the datastore - 'ID' is our unique key - 
            scraperwiki.sqlite.save(["ID"], record)

#create our browser
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#store the results of opening the URL with that browser
response = br.open(lotterygrantsurl)

#loop through all the forms (put in a list) and print them
print "All forms:", [ form.name  for form in br.forms() ]

#select the form with the name "aspnetForm"
br.select_form(name="aspnetForm")
print br.form

#Set 3 of the options in the form, as specified
br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
br["ctl00$phMainContent$txtGrantDateFrom"] = "01/01/2014"
br["ctl00$phMainContent$txtGrantDateTo"]  = "20/01/2017"

#print the values being held by br
print br
#submit the options
response = br.submit()
#read the results into new variable called 'html'
html = response.read()
print html
#convert to lxml object
root = lxml.html.fromstring(html)
# START scraping by running scrape_table function created above
scrape_table(root)
