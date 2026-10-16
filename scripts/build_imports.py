"""Render supplied affiliate links as searchable collections; retain existing site chrome."""
from pathlib import Path
from html import escape as E
import json,re

def build_imports(root):
 root=Path(root);items=json.loads((root/'imported-products.json').read_text());template=(root/'index.html').read_text()
 for filename,selected,title,description in [
 ('amazon-new-finds.html',[p for p in items if p['marketplace']!='AE'],'More Amazon Product Finds','Explore newly added Amazon product links across beauty, home, tech, fashion and more. Search the collection and check current details on Amazon.')]:
  body='<main id="main" class="wrap"><section class="section"><p class="breadcrumb"><a href="./">Home</a> / '+E(title)+'</p><p class="eyebrow">Gardezi Finds · Product collection</p><h1>'+E(title)+'</h1><p class="intro">'+E(description)+'</p><p>Product names and affiliate links come from the supplied catalog. Confirm the destination marketplace, exact variant, price, availability, delivery and warranty before ordering. Listed features have not been independently verified.</p><p><a href="amazon-new-finds.html">More Amazon finds</a> · <a href="./#collections">Original collections</a></p><label for="filter">Search these products</label> <input id="filter" type="search" placeholder="Product, brand or category" style="padding:12px;border:1px solid #bbc4d0;border-radius:8px;max-width:100%;width:360px"><p id="result-count" aria-live="polite">'+str(len(selected))+' products in this collection</p><div class="products" data-product-grid>'
  for i,p in enumerate(selected):
   attrs=' href="'+E(p['url'],quote=True)+'" target="_blank" rel="sponsored nofollow noopener" data-affiliate data-asin="'+E(p.get('asin') or '')+'" data-title="'+E(p['title'],quote=True)+'"'
   body+='<article class="product-card" data-title="'+E(p['title'],quote=True)+'" data-search="'+E((p['title']+' '+p['category']).lower(),quote=True)+'" data-photo="'+str(int(bool(p.get('image'))))+'" data-order="'+str(i)+'">'
   if p.get('image'):body+='<div class="product-media"><img src="'+E(p['image'],quote=True)+'" alt="'+E(p['title'],quote=True)+'" loading="lazy" width="240" height="200"><div class="product-placeholder" hidden>View product on Amazon</div></div>'
   body+='<p class="product-tag">'+E(p['category'])+'</p><h3><a'+attrs+'>'+E(p['title'])+'</a></h3><p>'+('Amazon UAE · Check price in AED' if p['marketplace']=='AE' else 'Check marketplace and current price on Amazon')+'</p><a class="buy"'+attrs+'>View on Amazon'+(' UAE' if p['marketplace']=='AE' else '')+' ↗</a></article>'
  body+='</div><p id="empty" hidden>No matching products. Try another search.</p></section></main>'
  page=re.sub(r'<main\b.*?</main>',lambda _:body,template,count=1,flags=re.S)
  page=re.sub(r'<title>.*?</title>','<title>'+E(title)+' | Gardezi Finds</title>',page,count=1,flags=re.S)
  base=re.search(r'<link rel="canonical" href="([^"]+)"',template)[1];base=base.removesuffix('index.html').rstrip('/')+'/'
  page=re.sub(r'(<link rel="canonical" href=")[^"]+',lambda m:m[1]+base+filename,page)
  for attr,key,val in [('name','description',description),('property','og:title',title),('property','og:description',description),('property','og:url',base+filename),('name','twitter:title',title),('name','twitter:description',description)]:
   page=re.sub(r'(<meta '+attr+'="'+re.escape(key)+'" content=")[^"]*',lambda m:m[1]+E(val,quote=True),page)
  page=re.sub(r'<script type="application/ld\+json">.*?</script>','',page,flags=re.S)
  schema={'@context':'https://schema.org','@type':'CollectionPage','name':title,'url':base+filename,'description':description}
  page=page.replace('</head>','<script type="application/ld+json">'+json.dumps(schema).replace('<','\\u003c')+'</script></head>')
  (root/filename).write_text(page)
if __name__=='__main__':
 import sys
 build_imports(sys.argv[1])
