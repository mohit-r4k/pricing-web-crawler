from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options
from simple_salesforce import Salesforce
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
#driver = webdriver.Chrome(options=options)

sf = Salesforce(password='@Ninja2024', username='shrijiit@rent4keeps.com.au', organizationId='00D90000000hZ5L',security_token='vyHCYiqIToLbMeP0C1TGclW0J') 
query_result = sf.query("SELECT Id, Name, Category__c, Email__c, Name__c, Price__c, Supplier__c, URL__c, Scan_Type__c FROM RetailProduct__c WHERE Id in ('a28Ie000000CbdT', 'a28Ie000000CbdO') ")

for i in query_result["records"]:
    url = i["URL__c"]

    if url.find('thegoodguys.com.au') > -1 or url.find('jbhifi.com.au') > -1 :
        old_price = i["Price__c"]
        price = 'None'
        alert = False

        price_val = 0
        old_price_val = 0
        if old_price.rfind('$') > -1:
            old_price_val = old_price[old_price.rfind('$')+1:]

        if (old_price is None) or (old_price == 'None'):
            old_price = 'None'

        driver.get(url)
        driver.implicitly_wait(5)
        
        try:
            if url.find('thegoodguys.com.au') > -1:
                PRODUCT_SELECTOR = 'html.ggds.dj_gecko.dj_ff126.dj_contentbox.mac-magic.svg-magic body div#contentWrapper div#content div#container_4099276460824440307.pdp-container.pdp-container--desk-tab div.bg-graylighter div.container.padd-sm-0.padd-md-0.padd-lg-0 div.col-md-4.col-lg-3.clearfix.padd-xs-0.padd-sm-0.padd-md-0.padd-lg-left-0 div#wrapperDiv.panel-pricing.col-sm-6.col-md-12.padd-xs-left-0.padd-xs-right-0.padd-xs-top-15.padd-md-0.padd-lg-0 div.marg-bottom-25 div#PriceDisplayWidget.panel-pricing__price-display.bg-white.line-height-sml.padd-md-0.padd-lg-0 div#contentRecommendationWidget.contentRecommendationWidget div.left_espot.price_section.padd-15 div.pricepoint-promolabel-wrap span.panel-pricing__price.pricepoint.clearfix div.purchase_section.clearfix'
            elif url.find('jbhifi.com.au') > -1:
                PRODUCT_SELECTOR = 'html.js.svg.flexbox.csstransforms.sass-opt-out-forms body.template-product.pdp-page.has-announcement div.outer-wrapper div#page-body-container.body-container div#PageContainer.page-container main#MainContent.main-content.product-page div#pdp div div#pdp-layout-wrapper.pdp-jss-layoutWrapper-23 div#pdp-layout-inner.pdp-jss-layout-24 div#pdp-right-panel.pdp-jss-layoutRight-27 div.pdp-jss-root-31 div#pdp-price-tag-wrapper._1vzft5e0._1vzft5e1._1vzft5e3 div#pdp-price-cta div.PriceTag_styles_cardContent__1eb7mu91r.Card_mapStyles__14jfglg2 div.PriceTag_priceTag__1eb7mu91q'
            else:
               PRODUCT_SELECTOR = ''

            if PRODUCT_SELECTOR != '': 
                price_element = driver.find_element(By.CSS_SELECTOR, PRODUCT_SELECTOR)

                if price_element is not None:
                    price = price_element.text

                    if price is None or price == '':
                        price = 'None'

                    if price is not None and price != 'None':
                        if price.find('$') <= -1:
                            price = '$' + price

                    """
                    price = price.replace('\n', '')
                    price = price.replace(',', '')
                    price = price.replace(' ', '')
                    price = price.replace('AUD', '')
                    price = price.replace('EA', '')
                    price = price.replace('RRP', '')
                    price = price.replace('of', '')
                    price = price.replace(':', '')
                    price = price.replace('A', '')
                    price = price.replace('Pricereducedfrom', '')
                    price = price.replace('to', '')
                    price = price.replace('Shopwithconfidence.SeeDysonBestPricePolicy', '')
                    price = price.replace('SAVE', ' ')
                    price = price.strip()
                    price = price.split(' ')[0]
                    """

                    if price.rfind('$') > -1:
                        price_val = price[price.rfind('$')+1:] 

                    if old_price == price or int(float(old_price_val)) == int(float(price_val)):
                        alert = False
                    else:
                        alert = True

                    print('price: ' + price + ' url: ' + url) 
                    print('alert: ' + alert)                      
                    
                    """
                    if (alert == True and price != 'None'):
                        sf.RetailProduct__c.update(i["Id"], {'Price__c': price, 'Old_Price__c': old_price, 'Alert__c': alert})
                    elif price == 'None':
                        sf.RetailProduct__c.update(i["Id"], {'Alert__c': True})   
                    """
                else:
                    print('Error')
                    #sf.RetailProduct__c.update(i["Id"], {'Alert__c': True})
                        
        except Exception as ex:
            print('****' + price + ' **** ' + url)
            print(ex)
            #sf.RetailProduct__c.update(i["Id"], {'Alert__c': True})
            pass

driver.quit()
