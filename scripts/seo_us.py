"""Apply US-focused metadata and shopping context without altering affiliate links."""
from pathlib import Path
from html import escape,unescape
import re,json,xml.etree.ElementTree as ET
BASE='https://jamalgardezi.github.io/amazon-affiliate-finds/'
TITLES={
'index':'Amazon Finds & Shopping Guides for US Shoppers',
'beauty-care-buying-guide':'Beauty & Skincare Buying Guide for US Shoppers',
'jewelry-buying-guide':'Jewelry Buying Guide for US Shoppers',
'gaming-buying-guide':'Video Games & Gaming Gifts: US Buying Guide',
'pet-accessories-buying-guide':'Dog & Cat Accessories: US Buying Guide',
'kids-toys-buying-guide':'Kids’ Toy Buying Guide for US Families',
 'tech-accessories-buying-guide':'Tech & Charging Accessories: US Buying Guide',
'electronics-tech':'Tech & Electronics: Amazon Finds for US Shoppers',
'home-kitchen':'Home & Kitchen: Amazon Finds for US Homes',
'beauty-care':'Beauty & Personal Care: Amazon US Shopping Finds',
'jewelry':'Jewelry & Gift Ideas for US Shoppers',
'toys-games':'Kids Toys & Games: Amazon US Gift Ideas',
'books-media':'Books & Movies: Amazon US Shopping Finds',
'mens-clothing':"Men’s Clothing & Accessories: Amazon US Finds",
'womens-clothing':"Women’s Clothing, Bags & Shoes: Amazon US Finds",
'kids-clothing':"Kids’ Clothing & Winter Wear: Amazon US Finds",
'grocery':'Grocery & Pantry: Amazon US Shopping Finds',
'sports-outdoors':'Sports & Outdoor Gear: Amazon US Finds',
'automotive-tools':'Car Accessories & Tools for US Shoppers',
'pets':'Pet Supplies & Accessories for US Shoppers',
'office-creative':'Office & Creative Supplies: Amazon US Finds',
'more-finds':'More Amazon Finds & Gift Ideas for US Shoppers',
'video-games':'Nintendo, PS5 & Xbox Games for US Shoppers',
'gaming-accessories':'Gaming Controllers & Accessories for US Shoppers',
'roblox':'Roblox Gifts & Gift Cards for US Shoppers',
'amazon-new-finds':'New Amazon Finds for US Shoppers',
}
DESC={
'index':'Explore Amazon finds for US shoppers across beauty, home, tech, jewelry, toys and gaming. Browse categories and guides; check delivery to your ZIP code.',
'amazon-new-finds':'Browse new Amazon finds for US shoppers in beauty, home, tech, fashion and gifts. Search products and confirm marketplace, price and US delivery on Amazon.',
}
def apply(root):
 root=Path(root)
 for p in root.glob('*.html'):
  s=p.read_text();match=re.search(r'<title>(.*?)</title>',s,re.S)
  if not match:continue
  slug=p.stem;oldtitle=unescape(match[1]);title=TITLES.get(slug)
  if not title and slug.endswith('buying-guide'):
   title=oldtitle.split(' | ')[0]
   if not re.search(r'\bUS\b',title):title+=' for US Shoppers'
  if title:
   title+=' | Gardezi Finds'
   s=re.sub(r'<title>.*?</title>',lambda _: '<title>'+escape(title)+'</title>',s,count=1,flags=re.S)
   olddesc=re.search(r'<meta name="description" content="([^"]*)"',s)
   desc=DESC.get(slug)
   if not desc and olddesc:
    first=unescape(olddesc[1]).split('. ')[0].rstrip('.')
    desc=first+'. For US shoppers: check current prices, product details and delivery to your ZIP code on Amazon.'
   for attr,key,val in [('name','description',desc),('property','og:title',title),('name','twitter:title',title),('property','og:description',desc),('name','twitter:description',desc)]:
    if val:s=re.sub(r'(<meta '+attr+'="'+key+'" content=")[^"]*',lambda m:m[1]+escape(val,quote=True),s)
  s=re.sub(r'(<html[^>]*lang=")[^"]*',r'\1en-US',s)
  s=s.replace('content="en_US"','content="en_US"')
  def schema(m):
   obj=json.loads(m[1])
   def visit(x):
    if isinstance(x,dict):
     if x.get('@type') in ('WebSite','WebPage','CollectionPage','Article'):
      x['inLanguage']='en-US';x['audience']={'@type':'Audience','geographicArea':{'@type':'Country','name':'United States'}}
      if title and x.get('@type') in ('WebSite','WebPage','CollectionPage'):x['description']=desc
     for v in list(x.values()):visit(v)
    elif isinstance(x,list):
     for v in x:visit(v)
   visit(obj)
   return '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False).replace('<','\\u003c')+'</script>'
  s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,s,flags=re.S)
  if slug in TITLES and not slug.endswith('buying-guide') and 'id="us-shopping"' not in s:
   note='<section id="us-shopping" class="section wrap" aria-label="Shopping in the United States"><h2>Shopping from the United States</h2><p>Set your US delivery ZIP code on Amazon to check availability, shipping costs and delivery estimates. Confirm the marketplace, selected size or model, current price in USD and return terms before ordering. Prices and availability can change.</p><p>For electronics, check US voltage and plug compatibility. For games and gift cards, confirm the US account or region requirements. Gardezi Finds shares affiliate links; purchases and customer service are handled by Amazon or the listed seller.</p><p><a href="./#collections">Browse product categories</a> · <a href="./#guides">Read shopping guides</a> · <a href="about.html#disclosure">Affiliate disclosure</a></p></section>'
   s=s.replace('</main>',note+'</main>',1)
  p.write_text(s)
if __name__=='__main__':apply(Path(__file__).resolve().parents[1])
