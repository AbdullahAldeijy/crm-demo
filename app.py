from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'crm-platform-secret-key-2024'

# Language translations
translations = {
    'en': {
        'site_name': 'Mizzanine',
        'welcome': 'Welcome to Mizzanine',
        'subtitle': 'Your Premier Construction & Contracting Marketplace',
        'partners': 'Our Construction Partners',
        'featured': 'Featured Construction Products',
        'login': 'Company Login',
        'contact_seller': 'Contact Seller',
        'buy_now': 'Buy with Torbiona',
        'quantity': 'Quantity',
        'in_stock': 'in stock',
        'by': 'by'
    },
    'ar': {
        'site_name': 'ميزانين',
        'welcome': 'مرحباً بكم في ميزانين',
        'subtitle': 'منصتكم الرائدة لسوق البناء والمقاولات',
        'partners': 'الشركات',
        'featured': 'منتجات البناء المميزة',
        'login': 'تسجيل دخول الشركة',
        'contact_seller': 'تواصل مع البائع',
        'buy_now': 'توربيونا',
        'quantity': 'الكمية',
        'in_stock': 'متوفر',
        'by': 'من'
    }
}

# Chat messages storage
chat_messages = {}

# Company accounts with employees
companies = {
    'techcorp': {
        'password': 'tech123',
        'name': 'BuildTech Construction',
        'industry': 'Construction',
        'employees': {
            'john_manager': {'name': 'John Smith', 'role': 'manager', 'password': 'john123'},
            'sarah_sales': {'name': 'Sarah Johnson', 'role': 'sales', 'password': 'sarah123'},
            'mike_purchase': {'name': 'Mike Davis', 'role': 'purchase', 'password': 'mike123'}
        }
    },
    'globaltech': {
        'password': 'global123',
        'name': 'Global Materials Supply',
        'industry': 'Construction Materials',
        'employees': {
            'lisa_manager': {'name': 'Lisa Chen', 'role': 'manager', 'password': 'lisa123'},
            'david_sales': {'name': 'David Wilson', 'role': 'sales', 'password': 'david123'},
            'emma_purchase': {'name': 'Emma Brown', 'role': 'purchase', 'password': 'emma123'}
        }
    },
    'innovate': {
        'password': 'innovate123',
        'name': 'ProBuild Equipment',
        'industry': 'Construction Equipment',
        'employees': {
            'alex_manager': {'name': 'Alex Rodriguez', 'role': 'manager', 'password': 'alex123'},
            'nina_sales': {'name': 'Nina Patel', 'role': 'sales', 'password': 'nina123'},
            'tom_purchase': {'name': 'Tom Anderson', 'role': 'purchase', 'password': 'tom123'}
        }
    }
}

# Products by company - Contracting sector focus
products = {
    'techcorp': [
        {
            'id': 1,
            'title': 'Heavy Duty Excavator',
            'description': 'CAT 320 Excavator - Perfect for large construction projects',
            'image': 'https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=300',
            'quantity': 5,
            'min_quantity': 1,
            'price': 125000.00,
            'category': 'Heavy Machinery'
        },
        {
            'id': 2,
            'title': 'Construction Safety Helmets',
            'description': 'OSHA compliant safety helmets - Pack of 50',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300',
            'quantity': 200,
            'min_quantity': 25,
            'price': 15.99,
            'category': 'Safety Equipment'
        }
    ],
    'globaltech': [
        {
            'id': 3,
            'title': 'Steel Reinforcement Bars',
            'description': 'Grade 60 rebar - 20ft lengths, various diameters',
            'image': 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=300',
            'quantity': 500,
            'min_quantity': 50,
            'price': 45.00,
            'category': 'Building Materials'
        },
        {
            'id': 4,
            'title': 'Concrete Mixer Truck',
            'description': '10 cubic yard capacity concrete mixer truck',
            'image': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=300',
            'quantity': 3,
            'min_quantity': 1,
            'price': 85000.00,
            'category': 'Heavy Machinery'
        }
    ],
    'innovate': [
        {
            'id': 5,
            'title': 'Scaffolding System',
            'description': 'Modular aluminum scaffolding - Complete 100ft system',
            'image': 'https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=300',
            'quantity': 15,
            'min_quantity': 3,
            'price': 2500.00,
            'category': 'Construction Equipment'
        },
        {
            'id': 6,
            'title': 'Power Tools Set',
            'description': 'Professional contractor power tools kit - 25 pieces',
            'image': 'https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=300',
            'quantity': 25,
            'min_quantity': 5,
            'price': 899.99,
            'category': 'Tools'
        }
    ]
}

@app.route('/')
@app.route('/<lang>')
def index(lang='en'):
    # Public view - show all companies and their products
    all_products = []
    for company_id, company_products in products.items():
        company_name = companies[company_id]['name']
        for product in company_products:
            product_copy = product.copy()
            product_copy['company'] = company_name
            product_copy['company_id'] = company_id
            all_products.append(product_copy)
    
    # Set language in session
    if lang in translations:
        session['language'] = lang
    else:
        lang = session.get('language', 'en')
    
    return render_template('index.html', companies=companies, products=all_products, 
                         lang=lang, t=translations[lang])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        company_id = request.form['company_id']
        password = request.form['password']
        
        if company_id in companies and companies[company_id]['password'] == password:
            session['company_id'] = company_id
            session['user_type'] = 'company'
            return redirect(url_for('crm_dashboard'))
        else:
            return render_template('login.html', error='Invalid company credentials', companies=companies)
    
    return render_template('login.html', companies=companies)

@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        company_id = request.form['company_id']
        employee_id = request.form['employee_id']
        password = request.form['password']
        
        if (company_id in companies and 
            employee_id in companies[company_id]['employees'] and 
            companies[company_id]['employees'][employee_id]['password'] == password):
            
            session['company_id'] = company_id
            session['employee_id'] = employee_id
            session['user_type'] = 'employee'
            session['role'] = companies[company_id]['employees'][employee_id]['role']
            return redirect(url_for('crm_dashboard'))
        else:
            return render_template('login.html', error='Invalid employee credentials', companies=companies)
    
    return render_template('login.html', companies=companies)

@app.route('/crm')
def crm_dashboard():
    if 'company_id' not in session:
        return redirect(url_for('login'))
    
    company_id = session['company_id']
    company = companies[company_id]
    user_role = session.get('role', 'company')
    
    # Get company's products
    company_products = products.get(company_id, [])
    
    # Get all other companies' products for purchase view
    other_products = []
    for other_company_id, other_company_products in products.items():
        if other_company_id != company_id:
            other_company_name = companies[other_company_id]['name']
            for product in other_company_products:
                product_copy = product.copy()
                product_copy['company'] = other_company_name
                product_copy['company_id'] = other_company_id
                other_products.append(product_copy)
    
    return render_template('crm.html', 
                         company=company, 
                         company_id=company_id,
                         products=company_products,
                         other_products=other_products,
                         user_role=user_role,
                         session=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/products', methods=['GET', 'POST'])
def api_products():
    if 'company_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    company_id = session['company_id']
    user_role = session.get('role', 'company')
    
    if request.method == 'POST':
        # Only managers and sales can add products
        if user_role not in ['manager', 'sales'] and session.get('user_type') != 'company':
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.json
        new_product = {
            'id': max([p['id'] for all_products in products.values() for p in all_products], default=0) + 1,
            'title': data['title'],
            'description': data['description'],
            'image': data['image'],
            'quantity': int(data['quantity']),
            'min_quantity': int(data['min_quantity']),
            'price': float(data['price']),
            'category': data['category']
        }
        
        if company_id not in products:
            products[company_id] = []
        products[company_id].append(new_product)
        
        return jsonify(new_product)
    
    return jsonify(products.get(company_id, []))

@app.route('/api/employees', methods=['GET', 'POST'])
def api_employees():
    if 'company_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    company_id = session['company_id']
    user_role = session.get('role', 'company')
    
    # Only company owners and managers can manage employees
    if user_role not in ['manager'] and session.get('user_type') != 'company':
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    if request.method == 'POST':
        data = request.json
        employee_id = data['employee_id']
        
        companies[company_id]['employees'][employee_id] = {
            'name': data['name'],
            'role': data['role'],
            'password': data['password']
        }
        
        return jsonify({'success': True})
    
    return jsonify(companies[company_id]['employees'])

@app.route('/api/contact_company', methods=['POST'])
def contact_company():
    data = request.json
    # In a real app, this would send an email or notification
    return jsonify({
        'success': True, 
        'message': f"Contact request sent to {data['company']} regarding {data['product']}"
    })

@app.route('/api/purchase', methods=['POST'])
def purchase_product():
    data = request.json
    company_id = data.get('company_id')
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    # Find the product
    if company_id in products:
        for product in products[company_id]:
            if product['id'] == product_id:
                if product['quantity'] >= quantity:
                    # Update inventory
                    product['quantity'] -= quantity
                    total_price = product['price'] * quantity
                    
                    return jsonify({
                        'success': True,
                        'message': f"Purchase successful! {quantity} x {product['title']} for ${total_price:.2f}",
                        'order_id': f"ORD-{product_id}-{quantity}",
                        'total': total_price
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': f"Insufficient stock. Only {product['quantity']} available."
                    })
    
    return jsonify({
        'success': False,
        'message': "Product not found."
    })

@app.route('/chat/<company_id>/<product_title>')
def chat_page(company_id, product_title):
    if company_id not in companies:
        return redirect(url_for('index'))
    
    chat_id = f"{company_id}_{product_title.replace(' ', '_')}"
    company = companies[company_id]
    lang = session.get('language', 'en')
    
    return render_template('chat.html', 
                         company=company, 
                         product_title=product_title,
                         chat_id=chat_id,
                         lang=lang, 
                         t=translations[lang])

@app.route('/api/chat/<chat_id>', methods=['GET', 'POST'])
def api_chat(chat_id):
    if request.method == 'POST':
        data = request.json
        message = {
            'sender': data.get('sender', 'Anonymous'),
            'message': data['message'],
            'timestamp': datetime.now().strftime('%H:%M')
        }
        
        if chat_id not in chat_messages:
            chat_messages[chat_id] = []
        chat_messages[chat_id].append(message)
        
        return jsonify({'success': True})
    
    return jsonify(chat_messages.get(chat_id, []))

@app.route('/torbiona-calculator')
def torbiona_calculator():
    import random
    order_data = request.args.get('order')
    lang = session.get('language', 'en')
    
    # Random approval (60% chance)
    approved = random.random() < 0.6
    score = random.randint(45, 95)
    
    return render_template('torbiona_calculator.html', 
                         approved=approved, 
                         score=score,
                         order_data=order_data,
                         lang=lang, 
                         t=translations[lang])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)