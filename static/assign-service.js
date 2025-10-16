function openAssignServiceWindow(companyId, productId, productTitle, productPrice) {
    var assignWindow = window.open('about:blank', '_blank', 'width=700,height=800,scrollbars=yes,resizable=yes');
    
    assignWindow.document.write(`
        <html>
        <head>
            <title>Assign Service - Mizzanine</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .assign-container { background: white; border-radius: 15px; max-width: 600px; margin: 0 auto; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
                .assign-header { background: linear-gradient(135deg, #17a2b8 0%, #138496 100%); color: white; padding: 2rem; text-align: center; }
                .assign-header h2 { margin: 0 0 0.5rem 0; font-size: 1.5rem; }
                .assign-body { padding: 2rem; }
                .section-title { font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 1rem; }
                .product-summary { background: #f8f9ff; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; border-left: 4px solid #17a2b8; }
                .product-name { font-weight: 600; color: #333; font-size: 1.1rem; margin-bottom: 0.5rem; }
                .service-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem; }
                .service-card { background: white; border: 2px solid #e9ecef; border-radius: 12px; padding: 1.5rem; text-align: center; cursor: pointer; transition: all 0.3s ease; }
                .service-card:hover { border-color: #17a2b8; }
                .service-card.selected { border-color: #17a2b8; background: #f0f8ff; }
                .service-icon { font-size: 2rem; margin-bottom: 0.5rem; }
                .service-name { font-weight: 600; color: #333; margin-bottom: 0.25rem; }
                .pricing-grid { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 2rem; }
                .price-range { display: flex; align-items: center; gap: 1rem; padding: 0.75rem; background: #f8f9fa; border-radius: 8px; }
                .range-label { min-width: 80px; font-weight: 500; color: #333; }
                .price-input { flex: 1; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; }
                .assign-footer { padding: 1.5rem 2rem; background: #f8f9fa; border-top: 1px solid #e9ecef; }
                .assign-btn { width: 100%; background: linear-gradient(135deg, #17a2b8 0%, #138496 100%); color: white; border: none; border-radius: 12px; padding: 1rem 2rem; font-size: 1.1rem; font-weight: 600; cursor: pointer; }
                .close-btn { background: #dc3545; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer; margin-left: 1rem; }
            </style>
        </head>
        <body>
            <div class="assign-container">
                <div class="assign-header">
                    <h2>🚚 Assign Delivery Service</h2>
                    <p>Set delivery options for this product</p>
                </div>
                <div class="assign-body">
                    <div class="section-title">📦 Product Information</div>
                    <div class="product-summary">
                        <div class="product-name">${productTitle}</div>
                        <div>Company: ${companyId}</div>
                        <div>Price: $${productPrice}</div>
                    </div>
                    <div class="section-title">🚛 Select Service Type</div>
                    <div class="service-grid">
                        <div class="service-card selected" onclick="selectService(this, 'fast')">
                            <div class="service-icon">⚡</div>
                            <div class="service-name">Fast Delivery</div>
                            <div>Same day delivery</div>
                        </div>
                        <div class="service-card" onclick="selectService(this, 'standard')">
                            <div class="service-icon">📦</div>
                            <div class="service-name">Standard Delivery</div>
                            <div>2-3 days</div>
                        </div>
                    </div>
                    <div class="section-title">💰 Set Pricing (SAR)</div>
                    <div class="pricing-grid">
                        <div class="price-range">
                            <span class="range-label">1-10 units:</span>
                            <input type="number" class="price-input" id="price1" placeholder="25" min="0" step="0.01">
                            <span>SAR</span>
                        </div>
                        <div class="price-range">
                            <span class="range-label">11-50 units:</span>
                            <input type="number" class="price-input" id="price2" placeholder="20" min="0" step="0.01">
                            <span>SAR</span>
                        </div>
                        <div class="price-range">
                            <span class="range-label">51+ units:</span>
                            <input type="number" class="price-input" id="price3" placeholder="15" min="0" step="0.01">
                            <span>SAR</span>
                        </div>
                    </div>
                </div>
                <div class="assign-footer">
                    <button class="assign-btn" onclick="assignService('${companyId}', '${productId}', '${productTitle}')">
                        🔧 Assign Service
                    </button>
                    <button class="close-btn" onclick="window.close()">Close</button>
                </div>
            </div>
            <script>
                var selectedService = 'fast';
                function selectService(card, service) {
                    document.querySelectorAll('.service-card').forEach(c => c.classList.remove('selected'));
                    card.classList.add('selected');
                    selectedService = service;
                }
                function assignService(companyId, productId, productTitle) {
                    var price1 = document.getElementById('price1').value || '25';
                    var price2 = document.getElementById('price2').value || '20';
                    var price3 = document.getElementById('price3').value || '15';
                    alert('Service assigned successfully!\\n\\nProduct: ' + productTitle + '\\nService: ' + (selectedService === 'fast' ? 'Fast Delivery' : 'Standard Delivery') + '\\nPricing:\\n1-10 units: ' + price1 + ' SAR\\n11-50 units: ' + price2 + ' SAR\\n51+ units: ' + price3 + ' SAR');
                    window.close();
                }
            </script>
        </body>
        </html>
    `);
}