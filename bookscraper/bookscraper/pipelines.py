# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        
        adapter=ItemAdapter(item)
        # Strip whitespace from all fields except 'description'
        field_names = adapter.field_names()
        for fieldname in field_names:
            if fieldname !='description':
                value=adapter.get(fieldname)
                adapter[fieldname]=value[0].strip()
        # switch to lowercase category and product_type
        lowercase_keys=['category','product_type']
        for lowercase_key in lowercase_keys:
            value=adapter.get(lowercase_key)
            adapter[lowercase_key]=value.lower()  
                  
        # convert price to lowercase
        price_keys=['price_excl_tax','price_incl_tax','tax','price']
        for price_key in price_keys:
            value=adapter.get(price_key)
            value=value.replace('£','').replace('$','').replace('€','').strip()
            adapter[price_key]=float(value)
        
        # Availability-->extract number of books in stack
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])
        
        # Reviews -->string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews']=int(num_reviews_string)
        
        # Stars-->convert to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value=='zero':
            adapter['stars'] = 0
        elif stars_text_value=='one':
            adapter['stars'] = 1
        elif stars_text_value=='two':
            adapter['stars'] = 2
        elif stars_text_value=='three':
            adapter['stars'] = 3
        elif stars_text_value=='four':
            adapter['stars'] = 4
        elif stars_text_value=='five':
            adapter['stars'] = 5
            
        return item
