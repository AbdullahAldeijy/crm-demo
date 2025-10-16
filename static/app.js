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

// buyProductCRM function moved to CRM page inline JavaScript

// B2B payment function removed - using enhanced Torbiona modal from CRM page

// B2B payment processing function removed

// B2B success modal function removed

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

// B2B Features Functions
function generatePO() {
    const poNumber = 'PO-' + new Date().getFullYear() + '-' + String(Math.floor(Math.random() * 1000)).padStart(3, '0');
    alert(`Purchase Order ${poNumber} generated successfully!\nPDF will be available for download.`);
}

function downloadPDF(poNumber) {
    alert(`Downloading PDF for ${poNumber}...\nIn production, this would generate and download a PDF file.`);
}

function createContract() {
    const contractId = 'CONTRACT-' + Date.now();
    alert(`New contract ${contractId} created!\nRedirecting to contract editor...`);
}

function viewContract(contractId) {
    alert(`Opening contract ${contractId}...\nIn production, this would open the contract viewer.`);
}

// Chat functionality
let currentChatId = null;

function contactSellerCRM(companyId, productTitle) {
    const message = prompt(`Send a message about "${productTitle}":`);
    if (message) {
        fetch('/api/contact_company', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                company: companyId,
                product: productTitle,
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                openChatWindow(data.chat_id, productTitle);
                showSection('chat');
            } else {
                alert(data.error || 'Failed to start chat');
            }
        });
    }
}

function openChatWindow(chatId, title) {
    currentChatId = chatId;
    document.getElementById('chat-title').textContent = `Chat: ${title}`;
    document.getElementById('chat-window').style.display = 'block';
    loadChatMessages();
}

function closeChatWindow() {
    document.getElementById('chat-window').style.display = 'none';
    currentChatId = null;
}

function loadChatMessages() {
    if (!currentChatId) return;
    
    fetch(`/api/chat/${currentChatId}`)
        .then(response => response.json())
        .then(messages => {
            const container = document.getElementById('chat-messages');
            container.innerHTML = '';
            messages.forEach(msg => {
                const div = document.createElement('div');
                div.className = 'chat-message';
                div.innerHTML = `
                    <div class="message-header">
                        <strong>${msg.sender}</strong>
                        <span class="timestamp">${msg.timestamp}</span>
                    </div>
                    <div class="message-content">${msg.message}</div>
                `;
                container.appendChild(div);
            });
            container.scrollTop = container.scrollHeight;
        });
}

function sendMessage() {
    if (!currentChatId) return;
    
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (message) {
        fetch(`/api/chat/${currentChatId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                input.value = '';
                loadChatMessages();
            } else {
                alert(data.error || 'Failed to send message');
            }
        });
    }
}

function handleEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Initialize dashboard when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateDashboardStats);
} else {
    updateDashboardStats();
}