document.addEventListener('click', function(e){
  const el = e.target.closest('[data-event]');
  if(!el) return;
  const eventName = el.dataset.event;
  const productName = el.dataset.product || '';
  if(window.gtag){
    gtag('event', eventName, {product_name: productName});
  }
  if(window.dataLayer){
    dataLayer.push({event: eventName, product_name: productName});
  }
});
