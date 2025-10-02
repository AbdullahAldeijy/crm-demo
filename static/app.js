// CRM Dashboard JavaScript

// Global variables
let currentSection = 'dashboard';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadInitialData();
});

// Initialize event listeners
function initializeEventListeners() {
    // Add Product Form
    const addProductForm = document.getElementById('addProductForm');
    if (addProductForm) {
        addProductForm.addEventListener('submit', handleAddProduct);
    }

    // Add Employee Form
    const addEmployeeForm = document.getElementById('addEmployeeForm');
    if (addEmployeeForm) {
        addEmployeeForm.addEventListener('submit', handleAddEmployee);
    }

    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
}

// Load initial data
function loadInitialData() {
    // Load products if we're on the CRM page
    if (document.getElementById('products-grid')) {
        loadProducts();
    }
}

// Navigation functions
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active class from all menu buttons
    document.querySelectorAll('.menu-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected section
    const targetSection = document.getElementById(sectionName);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // Activate corresponding menu button
    const menuButtons = document.querySelectorAll('.menu-btn');
    menuButtons.forEach(btn => {
        if (btn.textContent.toLowerCase().includes(sectionName) || 
            (sectionName === 'dashboard' && btn.textContent.includes('Dashboard')) ||
            (sectionName === 'products' && btn.textContent.includes('Products')) ||
            (sectionName === 'marketplace' && btn.textContent.includes('Marketplace')) ||
            (sectionName === 'employees' && btn.textContent.includes('Employees'))) {
            btn.classList.add('active');
        }
    });

    currentSection = sectionName;
}

// Modal functions
function showAddProductModal() {
    document.getElementById('addProductModal').style.display = 'block';
}

function showAddEmployeeModal() {
    document.getElementById('addEmployeeModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Product management
function handleAddProduct(event) {
    event.preventDefault();
    
    const formData = {
        title: document.getElementById('productTitle').value,
        description: document.getElementById('productDescription').value,
        image: document.getElementById('productImage').value || 'https://via.placeholder.com/300?text=No+Image',
        quantity: document.getElementById('productQuantity').value,
        min_quantity: document.getElementById('productMinQuantity').value,
        price: document.getElementById('productPrice').value,
        category: document.getElementById('productCategory').value
    };

    fetch('/api/products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            alert('Product added successfully!');
            closeModal('addProductModal');
            document.getElementById('addProductForm').reset();
            loadProducts();
            location.reload(); // Refresh to show new product
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding the product.');
    });
}

function loadProducts() {
    fetch('/api/products')
    .then(response => response.json())
    .then(products => {
        const productsGrid = document.getElementById('products-grid');
        if (productsGrid && products.length > 0) {
            updateProductsDisplay(products);
        }
    })
    .catch(error => {
        console.error('Error loading products:', error);
    });
}

function updateProductsDisplay(products) {
    const productsGrid = document.getElementById('products-grid');
    if (!productsGrid) return;

    productsGrid.innerHTML = '';
    
    products.forEach(product => {
        const productCard = createProductCard(product);
        productsGrid.appendChild(productCard);
    });
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    const stockClass = product.quantity <= product.min_quantity ? 'low-stock' : '';
    
    card.innerHTML = `
        <img src="${product.image}" alt="${product.title}" class="product-image">
        <div class="product-info">
            <h3>${product.title}</h3>
            <p>${product.description}</p>
            <div class="product-details">
                <span class="product-price">$${parseFloat(product.price).toFixed(2)}</span>
                <span class="product-stock ${stockClass}">${product.quantity} in stock</span>
            </div>
            <span class="product-category">${product.category}</span>
        </div>
    `;
    
    return card;
}

// Employee management
function handleAddEmployee(event) {
    event.preventDefault();
    
    const formData = {
        name: document.getElementById('employeeName').value,
        employee_id: document.getElementById('employeeId').value,
        role: document.getElementById('employeeRole').value,
        password: document.getElementById('employeePassword').value
    };

    fetch('/api/employees', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            alert('Employee added successfully!');
            closeModal('addEmployeeModal');
            document.getElementById('addEmployeeForm').reset();
            location.reload(); // Refresh to show new employee
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding the employee.');
    });
}

// Marketplace functions
function contactSeller(companyId, productTitle) {
    const message = prompt(`Send a message to the company about "${productTitle}":`);
    if (message) {
        fetch('/api/contact_company', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                company: companyId,
                product: productTitle,
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while sending the message.');
        });
    }
}

function buyProductCRM(companyId, productId, productTitle, price) {
    const quantityInput = document.getElementById(`crm-qty-${productId}`);
    const quantity = parseInt(quantityInput.value);
    
    if (quantity && quantity > 0) {
        const totalPrice = (parseFloat(price) * quantity).toFixed(2);
        
        // Show Torbiona payment modal (reuse the same function from index.html)
        showTorbionePaymentCRM({
            companyId: companyId,
            productId: productId,
            productTitle: productTitle,
            quantity: quantity,
            unitPrice: price,
            totalPrice: totalPrice
        });
    } else {
        alert('Please select a valid quantity.');
    }
}

function showTorbionePaymentCRM(orderData) {
    const modal = document.createElement('div');
    modal.className = 'torbiona-modal';
    modal.innerHTML = `
        <div class="torbiona-modal-content">
            <span class="close" onclick="closeTorbioneModal()">&times;</span>
            <div class="torbiona-header">
                <h2>🔒 Secure B2B Payment with Torbiona</h2>
                <p>Professional procurement made easy</p>
            </div>
            
            <div class="order-summary">
                <h3>Purchase Order Summary</h3>
                <div class="order-item">
                    <span class="item-name">${orderData.productTitle}</span>
                    <span class="item-details">Qty: ${orderData.quantity} × $${orderData.unitPrice}</span>
                    <span class="item-total">$${orderData.totalPrice}</span>
                </div>
                <div class="order-total">
                    <strong>Total: $${orderData.totalPrice}</strong>
                </div>
            </div>
            
            <div class="torbiona-payment">
                <h3>B2B Payment Method</h3>
                <div class="payment-options">
                    <label class="payment-option">
                        <input type="radio" name="payment" value="torbiona-corporate" checked>
                        <span class="payment-icon">🏢</span>
                        <span>Corporate Account</span>
                    </label>
                    <label class="payment-option">
                        <input type="radio" name="payment" value="torbiona-credit">
                        <span class="payment-icon">💳</span>
                        <span>Business Credit Line</span>
                    </label>
                    <label class="payment-option">
                        <input type="radio" name="payment" value="torbiona-invoice">
                        <span class="payment-icon">📄</span>
                        <span>Net 30 Invoice</span>
                    </label>
                </div>
                
                <div class="torbiona-security">
                    <p>🛡️ Enterprise-grade security by Torbiona</p>
                    <p>✅ PCI DSS Level 1 compliant</p>
                    <p>🔐 Multi-signature authorization</p>
                    <p>📊 Real-time transaction tracking</p>
                </div>
                
                <button class="btn btn-primary btn-full" onclick="processTorbionePaymentCRM(${JSON.stringify(orderData).replace(/"/g, '&quot;')})">
                    Process B2B Payment with Torbiona
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

function processTorbionePaymentCRM(orderData) {
    const paymentMethod = document.querySelector('input[name="payment"]:checked').value;
    
    // Show processing animation
    const button = event.target;
    button.innerHTML = '🔄 Processing B2B Payment...';
    button.disabled = true;
    
    // Simulate Torbiona B2B payment processing
    setTimeout(() => {
        fetch('/api/purchase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                company_id: orderData.companyId,
                product_id: orderData.productId,
                quantity: orderData.quantity,
                payment_method: paymentMethod,
                total_amount: orderData.totalPrice,
                b2b_purchase: true
            })
        })
        .then(response => response.json())
        .then(data => {
            closeTorbioneModal();
            if (data.success) {
                showB2BSuccessModal(orderData, paymentMethod);
                // Refresh the marketplace section
                location.reload();
            } else {
                alert('Payment failed: ' + data.message);
            }
        })
        .catch(error => {
            closeTorbioneModal();
            alert('Payment processing error. Please try again.');
        });
    }, 2500);
}

function showB2BSuccessModal(orderData, paymentMethod) {
    const modal = document.createElement('div');
    modal.className = 'success-modal';
    modal.innerHTML = `
        <div class="success-modal-content">
            <div class="success-header">
                <div class="success-icon">✅</div>
                <h2>Purchase Order Confirmed!</h2>
                <p>B2B transaction completed successfully</p>
            </div>
            
            <div class="success-details">
                <h3>Purchase Order Details</h3>
                <p><strong>Product:</strong> ${orderData.productTitle}</p>
                <p><strong>Quantity:</strong> ${orderData.quantity}</p>
                <p><strong>Total Amount:</strong> $${orderData.totalPrice}</p>
                <p><strong>Payment Method:</strong> ${paymentMethod.replace('-', ' ').toUpperCase()}</p>
                <p><strong>PO Number:</strong> PO-${Date.now()}</p>
                <p><strong>Delivery:</strong> 5-7 business days</p>
            </div>
            
            <div class="success-actions">
                <button class="btn btn-primary" onclick="closeSuccessModal()">
                    Continue Procurement
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Search and filter functions
function searchProducts(searchTerm) {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('p').textContent.toLowerCase();
        const category = card.querySelector('.product-category').textContent.toLowerCase();
        
        if (title.includes(searchTerm.toLowerCase()) || 
            description.includes(searchTerm.toLowerCase()) || 
            category.includes(searchTerm.toLowerCase())) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function filterProductsByCategory(category) {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        const productCategory = card.querySelector('.product-category').textContent;
        if (category === 'all' || productCategory === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Dashboard statistics
function updateDashboardStats() {
    // This would typically fetch real-time data from the server
    // For now, we'll update based on DOM elements
    
    const productCards = document.querySelectorAll('#products .product-card');
    const lowStockItems = document.querySelectorAll('.product-stock.low-stock');
    
    // Update product count
    const productCountElement = document.querySelector('.stat-card .stat-number');
    if (productCountElement) {
        productCountElement.textContent = productCards.length;
    }
    
    // Update low stock count
    const lowStockElements = document.querySelectorAll('.stat-card .stat-number');
    if (lowStockElements[1]) {
        lowStockElements[1].textContent = lowStockItems.length;
    }
}

// Initialize dashboard when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateDashboardStats);
} else {
    updateDashboardStats();
}