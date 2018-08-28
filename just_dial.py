import requests
from bs4 import BeautifulSoup
import csv

fields = ['Name','Land_number','Mobile_number','Address','Email']
out_file = open('dental_services_in_bangalore.csv','wb')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)



def all_links_page(page_id):
        page_text= requests.get("https://www.justdial.com/Bangalore/Dentists/nct-10156331/page-{}".format(page_id), headers={"User-Agent":'Mozilla/5.0 '})
        soup = BeautifulSoup(page_text.text, 'lxml')
        container_elems = soup.find_all('li', {'class': 'cntanr'})
	urls = []
        
	for elem in container_elems:
        	url_s  = elem.select('.store-name > .jcn > a')[0].attrs['href']
        	urls.append(url_s)
       
        
        return urls
       
def get_details(urls):      
        no_of_urls=len(urls)
        result=[]
       
        
	for i in range(0,no_of_urls):
                temp={} 
                
                      
                url__s=urls[i]
                
                
                agent={"User-Agent":'Mozilla/5.0'}
                page_texts=requests.get(url__s,headers=agent)
                soup = BeautifulSoup(page_texts.text, 'lxml')
                
                temp['Name']=soup.select('.fn')[0].text
                try:
			temp['Land_number']=soup.find('div',{'class':'telCntct cmawht'}).text.strip()
                except:
                        temp['Land_number']=None
                try:
                	temp['Mobile_number']=soup.find('span',{'class':'telnowpr'}).text.strip()
                except:
                        temp['Mobile_number']=None
                try:
                	temp['Address']=soup.find('span',{'id':'fulladdress'}).text.strip()
                except:
                        temp['Address']=None
                try:
	                temp['email']=soup.select("span.mreinfp.comp-text > a")[0].attrs['title']
                except:
			temp['email']=None
                
	        
		result.append(temp)
                temp={}
        
	return result	
                
	
def main():

	# No. of pages. Change this accordingly

	n = 20
	for i in range(1,n):
                dentists_data=[]
                dentist_details={}
		page_text = all_links_page(i)
        	dentists_data += get_details(page_text)
                print "$$"*20
                print dentists_data   
                print "$$"*20
                
        	for dentist in dentists_data:
                        dentist_details['Name']=dentist['Name']
                	dentist_details['Land_number']=dentist['Land_number']
                	dentist_details['Mobile_number']=dentist['Mobile_number']
                	dentist_details['Address']=dentist['Address']
                	dentist_details['Email']=dentist['email']
                        
                	csvwriter.writerow(dentist_details)
                
if __name__ == '__main__':
	main()
