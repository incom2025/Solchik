function sendEvent(name, params){
  if(window.gtag){ gtag('event', name, params || {}); }
  if(window.dataLayer){ dataLayer.push(Object.assign({event:name}, params || {})); }
}

document.querySelectorAll('.order-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const product = btn.dataset.product || 'unknown';
    sendEvent('order_click', {
      product_name: product,
      event_category: 'lead',
      event_label: product
    });
  });
});

document.querySelectorAll('.social').forEach(link => {
  link.addEventListener('click', () => {
    sendEvent(link.dataset.social + '_click', {
      event_category: 'social',
      event_label: link.href
    });
  });
});
