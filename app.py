from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'crm-platform-secret-key-2024'
app.jinja_env.autoescape = True

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
        'buy_now': 'Buy',
        'crm_dashboard': 'CRM Dashboard',
        'main_platform': 'Main Platform',
        'company_login': 'Company Login',
        'employee_login': 'Employee Login',
        'register_company': 'Register Company',
        'company_id': 'Company ID',
        'password': 'Password',
        'company_name': 'Company Name',
        'industry': 'Industry',
        'commercial_registration': 'Commercial Registration',
        'employee_id': 'Employee ID',
        'demo_accounts': 'Demo Accounts',
        'chat': 'Chat',
        'messages': 'Messages',
        'send_message': 'Send Message',
        'type_message': 'Type your message...',
        'quantity': 'Quantity',
        'in_stock': 'in stock',
        'by': 'by',
        # CRM translations
        'dashboard': 'Dashboard',
        'my_products': 'My Products',
        'marketplace': 'Marketplace',
        'purchase_orders': 'Purchase Orders',
        'contracts': 'Contracts',
        'supplier_performance': 'Supplier Performance',
        'analytics': 'Analytics',
        'employees': 'Manage Departments',
        'logout': 'Logout',
        'dashboard_overview': 'Dashboard Overview',
        'total_products': 'Total Products',
        'low_stock_items': 'Low Stock Items',
        'total_employees': 'Total Employees',
        'your_role': 'Your Role',
        'quick_actions': 'Quick Actions',
        'add_new_product': 'Add New Product',
        'add_employee': 'Add Employee',
        'browse_marketplace': 'Browse Marketplace',
        'add_product': 'Add Product',
        'available': 'available',
        'company_admin': 'Company Admin',
        'admin': 'Admin',
        'marketing': 'Marketing',
        'market_analytics': 'Market Analytics',
        'supply_demand': 'Supply & Demand Balance',
        'download_reports': 'Download Reports/Ads',
        'campaign_analysis': 'Campaign Analysis',
        'packages': 'Advertising Packages',
        'package_1': 'Package 1 - Daily Priority',
        'package_2': 'Package 2 - Weekly Priority',
        'package_3': 'Package 3 - Monthly Priority',
        'package_1_desc': 'First appearance among companies for 1 day in store interface with advertising image',
        'package_2_desc': 'First appearance for 1 week among companies + 2 products + image in interface',
        'package_3_desc': 'First appearance for 1 month among companies + 2 products + image in interface',
        'purchase_package': 'Purchase Package',
        'sar': 'SAR'
    },
    'ar': {
        'site_name': 'ميزانين',
        'welcome': 'مرحباً بكم في ميزانين',
        'subtitle': 'منصتكم الرائدة لسوق البناء والمقاولات',
        'partners': 'الشركات',
        'featured': 'منتجات البناء المميزة',
        'login': 'تسجيل دخول الشركة',
        'contact_seller': 'تواصل مع البائع',
        'buy_now': 'شراء',
        'quantity': 'الكمية',
        'in_stock': 'متوفر',
        'by': 'من',
        'crm_dashboard': 'لوحة إدارة الشركة',
        'main_platform': 'المنصة الرئيسية',
        'company_login': 'تسجيل دخول الشركة',
        'employee_login': 'تسجيل دخول الموظف',
        'register_company': 'تسجيل شركة',
        'company_id': 'معرف الشركة',
        'password': 'كلمة المرور',
        'company_name': 'اسم الشركة',
        'industry': 'القطاع',
        'commercial_registration': 'السجل التجاري',
        'employee_id': 'معرف الموظف',
        'demo_accounts': 'حسابات تجريبية',
        'chat': 'المحادثة',
        'messages': 'الرسائل',
        'send_message': 'إرسال رسالة',
        'type_message': 'اكتب رسالتك...',
        # CRM translations
        'dashboard': 'لوحة التحكم',
        'my_products': 'منتجاتي',
        'marketplace': 'السوق',
        'purchase_orders': 'أوامر الشراء',
        'contracts': 'العقود',
        'supplier_performance': 'أداء الموردين',
        'analytics': 'التحليلات',
        'employees': 'إدارة الأقسام',
        'logout': 'تسجيل الخروج',
        'dashboard_overview': 'نظرة عامة على لوحة التحكم',
        'total_products': 'إجمالي المنتجات',
        'low_stock_items': 'المنتجات منخفضة المخزون',
        'total_employees': 'إجمالي الموظفين',
        'your_role': 'دورك',
        'quick_actions': 'إجراءات سريعة',
        'add_new_product': 'إضافة منتج جديد',
        'add_employee': 'إضافة موظف',
        'browse_marketplace': 'تصفح السوق',
        'add_product': 'إضافة منتج',
        'available': 'متاح',
        'company_admin': 'مدير الشركة',
        'admin': 'مدير',
        'marketing': 'التسويق',
        'market_analytics': 'تحليلات السوق',
        'supply_demand': 'موازنة العرض والطلب',
        'download_reports': 'تنزيل التقارير/الإعلانات',
        'campaign_analysis': 'تحليل الحملات التسويقية',
        'packages': 'باقات الإعلان',
        'package_1': 'الباقة الأولى - الأولوية اليومية',
        'package_2': 'الباقة الثانية - الأولوية الأسبوعية',
        'package_3': 'الباقة الثالثة - الأولوية الشهرية',
        'package_1_desc': 'الظهور الأول بين الشركات لمدة يوم في واجهة المتجر مع إضافة صورة إعلانية',
        'package_2_desc': 'الظهور الأول لمدة أسبوع بين الشركات + منتجين + صورة بالواجهة',
        'package_3_desc': 'الظهور الأول لمدة شهر بين الشركات + منتجين + صورة بالواجهة',
        'purchase_package': 'شراء الباقة',
        'sar': 'ريال'
    }
}

# Chat messages storage
chat_messages = {}

# Purchase orders storage with ratings
purchase_orders = [
    {
        'id': 'PO-2024-001',
        'supplier': 'Global Materials Supply',
        'amount': 22500.00,
        'status': 'completed',
        'date': '2024-11-15',
        'due_date': '2024-12-15',
        'product': 'Steel Reinforcement Bars',
        'quantity': 50,
        'rating': 4.5,
        'feedback': 'Excellent quality materials, delivered on time'
    },
    {
        'id': 'PO-2024-002',
        'supplier': 'BuildTech Construction',
        'amount': 45000.00,
        'status': 'completed',
        'date': '2024-11-20',
        'due_date': '2024-12-20',
        'product': 'Concrete Mixers',
        'quantity': 2,
        'rating': 4.2,
        'feedback': 'Good equipment, minor delivery delay'
    },
    {
        'id': 'PO-2024-003',
        'supplier': 'ProBuild Materials',
        'amount': 18750.00,
        'status': 'pending',
        'date': '2024-12-01',
        'due_date': '2024-12-30',
        'product': 'Safety Equipment',
        'quantity': 100,
        'rating': None,
        'feedback': None
    },
    {
        'id': 'PO-2024-004',
        'supplier': 'SteelWorks Industries',
        'amount': 67500.00,
        'status': 'completed',
        'date': '2024-10-15',
        'due_date': '2024-11-15',
        'product': 'Structural Steel Beams',
        'quantity': 25,
        'rating': 4.8,
        'feedback': 'Outstanding quality and service, highly recommended'
    },
    {
        'id': 'PO-2024-005',
        'supplier': 'ConcretePro Solutions',
        'amount': 32000.00,
        'status': 'in_progress',
        'date': '2024-11-25',
        'due_date': '2024-12-25',
        'product': 'Ready-Mix Concrete',
        'quantity': 200,
        'rating': None,
        'feedback': None
    },
    {
        'id': 'PO-2024-006',
        'supplier': 'Heavy Machinery Co',
        'amount': 125000.00,
        'status': 'completed',
        'date': '2024-09-10',
        'due_date': '2024-10-10',
        'product': 'Excavator Rental',
        'quantity': 1,
        'rating': 4.0,
        'feedback': 'Reliable machinery, good maintenance support'
    },
    {
        'id': 'PO-2024-007',
        'supplier': 'ElectroTech Systems',
        'amount': 28500.00,
        'status': 'pending',
        'date': '2024-12-05',
        'due_date': '2025-01-05',
        'product': 'Electrical Components',
        'quantity': 150,
        'rating': None,
        'feedback': None
    },
    {
        'id': 'PO-2024-008',
        'supplier': 'Quality Paints Ltd',
        'amount': 15600.00,
        'status': 'completed',
        'date': '2024-11-01',
        'due_date': '2024-11-30',
        'product': 'Industrial Paint',
        'quantity': 80,
        'rating': 3.8,
        'feedback': 'Good coverage but color consistency could be better'
    }
]

# Contracts storage - 4 contracts per company
contracts = [
    # Bin Laden Group contracts
    {'id': 'PUR-20241201-001', 'title': 'اتفاقية شراء - حديد التسليح', 'buyer': 'مجموعة بن لادن السعودية', 'seller': 'نسما وشركاهم', 'amount': 280000.00, 'payment_method': 'pay-now', 'status': 'نشط', 'date': '2024-12-01', 'type': 'buyer-seller', 'product': 'حديد التسليح عالي الجودة', 'quantity': 100},
    {'id': 'PUR-20241130-002', 'title': 'اتفاقية شراء - كرينات برجية', 'buyer': 'مجموعة بن لادن السعودية', 'seller': 'السيف للمقاولات', 'amount': 850000.00, 'payment_method': 'torbiona', 'status': 'نشط', 'date': '2024-11-30', 'type': 'buyer-seller', 'product': 'كرينات برجية للمشاريع العالية', 'quantity': 1},
    {'id': 'PUR-20241129-003', 'title': 'اتفاقية بيع - حفارات ثقيلة', 'buyer': 'نسما وشركاهم', 'seller': 'مجموعة بن لادن السعودية', 'amount': 900000.00, 'payment_method': 'pay-now', 'status': 'نشط', 'date': '2024-11-29', 'type': 'buyer-seller', 'product': 'حفارات ثقيلة للمشاريع الكبرى', 'quantity': 2},
    {'id': 'PUR-20241128-004', 'title': 'اتفاقية بيع - خلاطات خرسانة', 'buyer': 'البواني', 'seller': 'مجموعة بن لادن السعودية', 'amount': 280000.00, 'payment_method': 'torbiona', 'status': 'نشط', 'date': '2024-11-28', 'type': 'buyer-seller', 'product': 'خلاطات الخرسانة المتنقلة', 'quantity': 1},
    
    # Nesma contracts
    {'id': 'PUR-20241127-005', 'title': 'اتفاقية شراء - كتل خرسانية', 'buyer': 'نسما وشركاهم', 'seller': 'البواني', 'amount': 6250.00, 'payment_method': 'pay-now', 'status': 'نشط', 'date': '2024-11-27', 'type': 'buyer-seller', 'product': 'كتل خرسانية معزولة', 'quantity': 500},
    {'id': 'PUR-20241126-006', 'title': 'اتفاقية شراء - خرسانة جاهزة', 'buyer': 'نسما وشركاهم', 'seller': 'المباني', 'amount': 3800.00, 'payment_method': 'torbiona', 'status': 'نشط', 'date': '2024-11-26', 'type': 'buyer-seller', 'product': 'خرسانة جاهزة عالية المقاومة', 'quantity': 10},
    {'id': 'PUR-20241125-007', 'title': 'اتفاقية بيع - حديد التسليح', 'buyer': 'السيف للمقاولات', 'seller': 'نسما وشركاهم', 'amount': 280000.00, 'payment_method': 'pay-now', 'status': 'نشط', 'date': '2024-11-25', 'type': 'buyer-seller', 'product': 'حديد التسليح عالي الجودة', 'quantity': 100},
    {'id': 'PUR-20241124-008', 'title': 'اتفاقية بيع - سقالات معدنية', 'buyer': 'المباني', 'seller': 'نسما وشركاهم', 'amount': 92500.00, 'payment_method': 'torbiona', 'status': 'نشط', 'date': '2024-11-24', 'type': 'buyer-seller', 'product': 'أنظمة السقالات المعدنية', 'quantity': 5},
    
    # Al-Saif contracts
    {'id': 'PUR-20241123-009', 'title': 'اتفاقية شراء - ألواح عزل', 'buyer': 'السيف للمقاولات', 'seller': 'البواني', 'amount': 2250.00, 'payment_method': 'pay-now', 'status': 'نشط', 'date': '2024-11-23', 'type': 'buyer-seller', 'product': 'ألواح العزل الحراري', 'quantity': 50},
    {'id': 'PUR-20241122-010', 'title': 'اتفاقية شراء - واجهات زجاجية', 'buyer': 'السيف للمقاولات', 'seller': 'المباني', 'amount': 6250.00, 'payment_method': 'torbiona', 'status': 'نشط', 'date': '2024-11-22', 'type': 'buyer-seller', 'product': 'أنظمة الواجهات الزجاجية', 'quantity': 5},
    {'id': 'PUR-20241121-011', 'title': 'اتفاقية بيع - كرينات برجية', 'buyer': 'البواني', 'seller': 'السيف للمقاولات', 'amount': 850000.00, 'payment_method': 'pay-now', 'status': 'نشط', 'date': '2024-11-21', 'type': 'buyer-seller', 'product': 'كرينات برجية للمشاريع العالية', 'quantity': 1},
    {'id': 'PUR-20241120-012', 'title': 'اتفاقية بيع - مضخات خرسانة', 'buyer': 'مجموعة بن لادن السعودية', 'seller': 'السيف للمقاولات', 'amount': 320000.00, 'payment_method': 'torbiona', 'status': 'نشط', 'date': '2024-11-20', 'type': 'buyer-seller', 'product': 'مضخات الخرسانة الثابتة', 'quantity': 1},
    
    # Al-Bawani contracts
    {'id': 'PUR-20241119-013', 'title': 'اتفاقية شراء - حفارات ثقيلة', 'buyer': 'البواني', 'seller': 'مجموعة بن لادن السعودية', 'amount': 450000.00, 'payment_method': 'pay-now', 'status': 'نشط', 'date': '2024-11-19', 'type': 'buyer-seller', 'product': 'حفارات ثقيلة للمشاريع الكبرى', 'quantity': 1},
    {'id': 'PUR-20241118-014', 'title': 'اتفاقية شراء - سقالات معدنية', 'buyer': 'البواني', 'seller': 'نسما وشركاهم', 'amount': 92500.00, 'payment_method': 'torbiona', 'status': 'نشط', 'date': '2024-11-18', 'type': 'buyer-seller', 'product': 'أنظمة السقالات المعدنية', 'quantity': 5},
    {'id': 'PUR-20241117-015', 'title': 'اتفاقية بيع - كتل خرسانية', 'buyer': 'المباني', 'seller': 'البواني', 'amount': 6250.00, 'payment_method': 'pay-now', 'status': 'نشط', 'date': '2024-11-17', 'type': 'buyer-seller', 'product': 'كتل خرسانية معزولة', 'quantity': 500},
    {'id': 'PUR-20241116-016', 'title': 'اتفاقية بيع - ألواح عزل', 'buyer': 'نسما وشركاهم', 'seller': 'البواني', 'amount': 2250.00, 'payment_method': 'torbiona', 'status': 'نشط', 'date': '2024-11-16', 'type': 'buyer-seller', 'product': 'ألواح العزل الحراري', 'quantity': 50},
    
    # Al-Mabani contracts
    {'id': 'PUR-20241115-017', 'title': 'اتفاقية شراء - مضخات خرسانة', 'buyer': 'المباني', 'seller': 'السيف للمقاولات', 'amount': 320000.00, 'payment_method': 'pay-now', 'status': 'نشط', 'date': '2024-11-15', 'type': 'buyer-seller', 'product': 'مضخات الخرسانة الثابتة', 'quantity': 1},
    {'id': 'PUR-20241114-018', 'title': 'اتفاقية شراء - خلاطات خرسانة', 'buyer': 'المباني', 'seller': 'مجموعة بن لادن السعودية', 'amount': 280000.00, 'payment_method': 'torbiona', 'status': 'نشط', 'date': '2024-11-14', 'type': 'buyer-seller', 'product': 'خلاطات الخرسانة المتنقلة', 'quantity': 1},
    {'id': 'PUR-20241113-019', 'title': 'اتفاقية بيع - خرسانة جاهزة', 'buyer': 'السيف للمقاولات', 'seller': 'المباني', 'amount': 3800.00, 'payment_method': 'pay-now', 'status': 'نشط', 'date': '2024-11-13', 'type': 'buyer-seller', 'product': 'خرسانة جاهزة عالية المقاومة', 'quantity': 10},
    {'id': 'PUR-20241112-020', 'title': 'اتفاقية بيع - واجهات زجاجية', 'buyer': 'البواني', 'seller': 'المباني', 'amount': 6250.00, 'payment_method': 'torbiona', 'status': 'نشط', 'date': '2024-11-12', 'type': 'buyer-seller', 'product': 'أنظمة الواجهات الزجاجية', 'quantity': 5}
]

# Delivery services for logistics companies
delivery_services = {
    'fastlogistics': {
        'services': [
            {
                'id': 'fast_delivery',
                'name': 'خدمة توصيل سريعة',
                'description': 'توصيل في نفس اليوم',
                'base_price': 50.00,
                'time': 'Same Day'
            },
            {
                'id': 'standard_delivery',
                'name': 'خدمة توصيل عادية',
                'description': 'توصيل خلال 2-3 أيام',
                'base_price': 25.00,
                'time': '2-3 Days'
            },
            {
                'id': 'heavy_equipment',
                'name': 'نقل المعدات الثقيلة',
                'description': 'نقل وتوصيل المعدات الثقيلة',
                'base_price': 200.00,
                'time': '1-2 Days'
            }
        ],
        'assigned_products': []  # Products this logistics company can deliver
    }
}

# Supplier performance data with ratings
supplier_performance = {
    'buildtech': {'delivery_time': 3.2, 'quality_rating': 4.2, 'orders_completed': 45, 'reviews': 23},
    'globalmaterials': {'delivery_time': 2.8, 'quality_rating': 4.5, 'orders_completed': 67, 'reviews': 34},
    'probuild': {'delivery_time': 4.1, 'quality_rating': 4.2, 'orders_completed': 32, 'reviews': 18},
    'steelworks': {'delivery_time': 2.5, 'quality_rating': 4.8, 'orders_completed': 89, 'reviews': 45},
    'concretepro': {'delivery_time': 3.0, 'quality_rating': 4.6, 'orders_completed': 56, 'reviews': 28},
    'heavymachinery': {'delivery_time': 3.5, 'quality_rating': 4.0, 'orders_completed': 38, 'reviews': 19},
    'electrotech': {'delivery_time': 2.9, 'quality_rating': 4.3, 'orders_completed': 42, 'reviews': 21},
    'qualitypaints': {'delivery_time': 3.8, 'quality_rating': 3.8, 'orders_completed': 29, 'reviews': 15}
}

# Company accounts with employees
companies = {
    'binladin': {
        'password': 'binladin123',
        'name': 'مجموعة بن لادن السعودية',
        'industry': 'Construction & Development',
        'employees': {
            'mohammed_manager': {'name': 'محمد العمري', 'role': 'manager', 'password': 'mohammed123'},
            'fatima_sales': {'name': 'فاطمة الأحمد', 'role': 'sales', 'password': 'fatima123'},
            'abdullah_purchase': {'name': 'عبدالله السعد', 'role': 'purchase', 'password': 'abdullah123'},
            'layla_marketing': {'name': 'ليلى الشمري', 'role': 'marketing', 'password': 'layla123'}
        }
    },
    'nesma': {
        'password': 'nesma123',
        'name': 'نسما وشركاهم',
        'industry': 'Contracting & Development',
        'employees': {
            'ahmed_manager': {'name': 'أحمد الخالد', 'role': 'manager', 'password': 'ahmed123'},
            'sara_sales': {'name': 'سارة المحمد', 'role': 'sales', 'password': 'sara123'},
            'omar_purchase': {'name': 'عمر الزهراني', 'role': 'purchase', 'password': 'omar123'},
            'huda_marketing': {'name': 'هدى القرني', 'role': 'marketing', 'password': 'huda123'}
        }
    },
    'alsaif': {
        'password': 'alsaif123',
        'name': 'السيف للمقاولات',
        'industry': 'Major Contracting',
        'employees': {
            'khalid_manager': {'name': 'خالد الراشد', 'role': 'manager', 'password': 'khalid123'},
            'noura_sales': {'name': 'نورا العتيبي', 'role': 'sales', 'password': 'noura123'},
            'hassan_purchase': {'name': 'حسن القحطاني', 'role': 'purchase', 'password': 'hassan123'},
            'reem_marketing': {'name': 'ريم الفيصل', 'role': 'marketing', 'password': 'reem123'}
        }
    },
    'albawani': {
        'password': 'albawani123',
        'name': 'البواني',
        'industry': 'Construction & Contracting',
        'employees': {
            'salman_manager': {'name': 'سلمان الدوسري', 'role': 'manager', 'password': 'salman123'},
            'maryam_sales': {'name': 'مريم الشهري', 'role': 'sales', 'password': 'maryam123'},
            'faisal_purchase': {'name': 'فيصل الغامدي', 'role': 'purchase', 'password': 'faisal123'},
            'amira_marketing': {'name': 'أميرة الجهني', 'role': 'marketing', 'password': 'amira123'}
        }
    },
    'almabani': {
        'password': 'almabani123',
        'name': 'المباني',
        'industry': 'Integrated Construction',
        'employees': {
            'nasser_manager': {'name': 'ناصر الحربي', 'role': 'manager', 'password': 'nasser123'},
            'aisha_sales': {'name': 'عائشة البقمي', 'role': 'sales', 'password': 'aisha123'},
            'yazeed_purchase': {'name': 'يزيد العنزي', 'role': 'purchase', 'password': 'yazeed123'},
            'dana_marketing': {'name': 'دانا المطيري', 'role': 'marketing', 'password': 'dana123'}
        }
    },
    'fastlogistics': {
        'password': 'fast123',
        'name': 'فاست لوجيستك',
        'industry': 'Logistics',
        'employees': {
            'khalil_manager': {'name': 'خليل الشهري', 'role': 'manager', 'password': 'khalil123'},
            'laila_sales': {'name': 'ليلى الدوسري', 'role': 'sales', 'password': 'laila123'},
            'tariq_purchase': {'name': 'طارق العتيبي', 'role': 'purchase', 'password': 'tariq123'},
            'rania_marketing': {'name': 'رانيا القحطاني', 'role': 'marketing', 'password': 'rania123'}
        }
    },
    'sabic': {
        'password': 'sabic123',
        'name': 'سابك',
        'industry': 'Petrochemicals & Manufacturing',
        'employees': {
            'ceo_sabic': {'name': 'يوسف البنيان', 'role': 'manager', 'password': 'ceo123'}
        }
    }
}

# Products by company - Contracting sector focus
products = {
    'binladin': [
        {
            'id': 1,
            'title': 'حفارات ثقيلة للمشاريع الكبرى',
            'description': 'حفارات كاتربيلر 320 - مثالية للمشاريع الإنشائية الضخمة',
            'image': 'https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=300',
            'quantity': 15,
            'min_quantity': 2,
            'price': 450000.00,
            'category': 'المعدات الثقيلة'
        },
        {
            'id': 2,
            'title': 'خلاطات الخرسانة المتنقلة',
            'description': 'خلاطات خرسانة بسعة 12 متر مكعب - للمشاريع الكبيرة',
            'image': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=300',
            'quantity': 8,
            'min_quantity': 1,
            'price': 280000.00,
            'category': 'معدات الخرسانة'
        }
    ],
    'nesma': [
        {
            'id': 3,
            'title': 'حديد التسليح عالي الجودة',
            'description': 'حديد تسليح درجة 60 - أطوال 12 متر، أقطار متنوعة',
            'image': 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=300',
            'quantity': 2000,
            'min_quantity': 100,
            'price': 2800.00,
            'category': 'مواد البناء'
        },
        {
            'id': 4,
            'title': 'أنظمة السقالات المعدنية',
            'description': 'سقالات ألمنيوم معيارية - نظام كامل 50 متر',
            'image': 'https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=300',
            'quantity': 25,
            'min_quantity': 5,
            'price': 18500.00,
            'category': 'معدات البناء'
        }
    ],
    'alsaif': [
        {
            'id': 5,
            'title': 'كرينات برجية للمشاريع العالية',
            'description': 'كرينات برجية بقدرة رفع 8 طن - ارتفاع 60 متر',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300',
            'quantity': 6,
            'min_quantity': 1,
            'price': 850000.00,
            'category': 'معدات الرفع'
        },
        {
            'id': 6,
            'title': 'مضخات الخرسانة الثابتة',
            'description': 'مضخات خرسانة ثابتة بقدرة 90 متر مكعب/ساعة',
            'image': 'https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=300',
            'quantity': 4,
            'min_quantity': 1,
            'price': 320000.00,
            'category': 'معدات الضخ'
        }
    ],
    'albawani': [
        {
            'id': 7,
            'title': 'كتل خرسانية معزولة',
            'description': 'كتل خرسانية معزولة حرارياً - مقاس 20x20x40 سم',
            'image': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=300',
            'quantity': 5000,
            'min_quantity': 500,
            'price': 12.50,
            'category': 'مواد البناء'
        },
        {
            'id': 8,
            'title': 'ألواح العزل الحراري',
            'description': 'ألواح عزل حراري من البوليسترين - سماكة 5 سم',
            'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300',
            'quantity': 1000,
            'min_quantity': 50,
            'price': 45.00,
            'category': 'مواد العزل'
        }
    ],
    'almabani': [
        {
            'id': 9,
            'title': 'خرسانة جاهزة عالية المقاومة',
            'description': 'خرسانة جاهزة مقاومة 350 كجم/سم² - توصيل مجاني',
            'image': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=300',
            'quantity': 200,
            'min_quantity': 10,
            'price': 380.00,
            'category': 'الخرسانة الجاهزة'
        },
        {
            'id': 10,
            'title': 'أنظمة الواجهات الزجاجية',
            'description': 'أنظمة واجهات زجاجية مزدوجة - مقاومة للعوامل الجوية',
            'image': 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=300',
            'quantity': 50,
            'min_quantity': 5,
            'price': 1250.00,
            'category': 'أنظمة الواجهات'
        }
    ],
    'sabic': [
        {
            'id': 11,
            'title': 'بولي إيثيلين عالي الكثافة',
            'description': 'بولي إيثيلين عالي الجودة للصناعات البتروكيميائية',
            'image': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=300',
            'quantity': 500,
            'min_quantity': 50,
            'price': 1200.00,
            'category': 'البتروكيماويات'
        },
        {
            'id': 12,
            'title': 'مواد كيميائية متخصصة',
            'description': 'مواد كيميائية متقدمة للصناعات المتخصصة',
            'image': 'https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=300',
            'quantity': 200,
            'min_quantity': 20,
            'price': 2500.00,
            'category': 'المواد الكيميائية'
        }
    ]

}

@app.route('/')
@app.route('/<lang>')
def index(lang='en'):
    # Public view - show only construction companies and their products (exclude logistics)
    all_products = []
    construction_companies = {k: v for k, v in companies.items() if v['industry'] != 'Logistics'}
    
    for company_id, company_products in products.items():
        if company_id in construction_companies:  # Only show construction company products
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
    
    return render_template('index.html', companies=construction_companies, products=all_products, 
                         lang=lang, t=translations[lang])

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/<lang>', methods=['GET', 'POST'])
def login(lang=None):
    # Set language
    if lang and lang in translations:
        session['language'] = lang
    current_lang = session.get('language', 'en')
    
    if request.method == 'POST':
        company_id = request.form['company_id']
        password = request.form['password']
        
        if company_id in companies and companies[company_id]['password'] == password:
            session['company_id'] = company_id
            session['user_type'] = 'company'
            return redirect(url_for('crm_dashboard'))
        else:
            return render_template('login.html', error='Invalid company credentials', companies=companies, lang=current_lang, t=translations[current_lang])
    
    return render_template('login.html', companies=companies, lang=current_lang, t=translations[current_lang])

@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    current_lang = session.get('language', 'en')
    
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
            return render_template('login.html', error='Invalid employee credentials', companies=companies, lang=current_lang, t=translations[current_lang])
    
    return render_template('login.html', companies=companies, lang=current_lang, t=translations[current_lang])

@app.route('/crm')
@app.route('/crm/<lang>')
def crm_dashboard(lang=None):
    if 'company_id' not in session:
        return redirect(url_for('login'))
    
    # Set language
    if lang and lang in translations:
        session['language'] = lang
    current_lang = session.get('language', 'en')
    
    company_id = session['company_id']
    company = companies[company_id]
    user_role = session.get('role', 'company')
    
    # Check if this is a logistics company
    is_logistics = company['industry'] == 'Logistics'
    
    if is_logistics:
        # For logistics companies, show delivery services and marketplace assignment
        company_services = delivery_services.get(company_id, {'services': [], 'assigned_products': []})
        
        # Get all construction products for assignment
        all_products = []
        for other_company_id, other_company_products in products.items():
            if companies[other_company_id]['industry'] != 'Logistics':
                other_company_name = companies[other_company_id]['name']
                for product in other_company_products:
                    product_copy = product.copy()
                    product_copy['company'] = other_company_name
                    product_copy['company_id'] = other_company_id
                    all_products.append(product_copy)
        
        return render_template('crm.html', 
                             company=company, 
                             company_id=company_id,
                             is_logistics=True,
                             delivery_services=company_services,
                             all_products=all_products,
                             companies=companies,
                             user_role=user_role,
                             session=session,
                             lang=current_lang,
                             t=translations[current_lang])
    else:
        # For construction companies, show products as before
        company_products = products.get(company_id, [])
        
        # Get all other construction companies' products for purchase view
        other_products = []
        all_products = []
        for other_company_id, other_company_products in products.items():
            if companies[other_company_id]['industry'] != 'Logistics':
                other_company_name = companies[other_company_id]['name']
                for product in other_company_products:
                    product_copy = product.copy()
                    product_copy['company'] = other_company_name
                    product_copy['company_id'] = other_company_id
                    all_products.append(product_copy)
                    if other_company_id != company_id:
                        other_products.append(product_copy)
        
        return render_template('crm.html', 
                             company=company, 
                             company_id=company_id,
                             is_logistics=False,
                             products=company_products,
                             other_products=other_products,
                             all_products=all_products,
                             companies=companies,
                             user_role=user_role,
                             session=session,
                             lang=current_lang,
                             t=translations[current_lang])

@app.route('/crm/chat/<company_id>/<int:product_id>')
def crm_chat_page(company_id, product_id):
    if 'company_id' not in session:
        return redirect(url_for('login'))
    
    if company_id not in companies:
        return redirect(url_for('crm_dashboard'))
    
    # Find the product
    product_title = "Unknown Product"
    for comp_id, comp_products in products.items():
        if comp_id == company_id and companies[comp_id]['industry'] != 'Logistics':
            for product in comp_products:
                if product['id'] == product_id:
                    product_title = product['title']
                    break
            break
    
    company = companies[company_id]
    lang = session.get('language', 'en')
    
    return render_template('chat.html', 
                         company=company, 
                         product_title=product_title,
                         company_id=company_id,
                         product_id=product_id,
                         lang=lang, 
                         t=translations[lang],
                         from_crm=True)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



@app.route('/api/contracts')
def get_contracts():
    return jsonify([])

@app.route('/chat/<company_id>/<int:product_id>')
def chat_page(company_id, product_id):
    if company_id not in companies:
        return redirect(url_for('index'))
    
    # Find the product
    product_title = "Unknown Product"
    for comp_id, comp_products in products.items():
        if comp_id == company_id:
            for product in comp_products:
                if product['id'] == product_id:
                    product_title = product['title']
                    break
            break
    
    company = companies[company_id]
    lang = session.get('language', 'en')
    
    return render_template('chat.html', 
                         company=company, 
                         product_title=product_title,
                         company_id=company_id,
                         product_id=product_id,
                         lang=lang, 
                         t=translations[lang])



@app.route('/api/products', methods=['GET', 'POST'])
def api_products():
    if 'company_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    company_id = session['company_id']
    user_role = session.get('role', 'company')
    
    # Logistics companies cannot add products
    if companies[company_id]['industry'] == 'Logistics':
        return jsonify({'error': 'Logistics companies cannot add products'}), 403
    
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

@app.route('/api/set_redirect', methods=['POST'])
def set_redirect():
    data = request.json
    if data.get('action') == 'buy':
        session['redirect_to_marketplace'] = True
    return jsonify({'success': True})

@app.route('/api/contact_company', methods=['POST'])
def contact_company():
    if 'company_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_role = session.get('role', 'company')
    user_type = session.get('user_type')
    
    # Check permissions: only company, manager, and purchase can initiate contact
    if user_type == 'employee' and user_role not in ['manager', 'purchase']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    data = request.json
    sender_company = session['company_id']
    target_company = data['company']
    product_name = data['product'].replace(' ', '_').replace('/', '_')
    
    # Create unique chat ID
    chat_id = f"{sender_company}_{target_company}_{product_name}"
    
    # Initialize chat if it doesn't exist
    if chat_id not in chat_messages:
        chat_messages[chat_id] = {
            'messages': [],
            'participants': [sender_company, target_company],
            'product': data['product'],
            'initiated_by': sender_company,
            'initiated_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    
    # Add initial message
    sender_name = companies[sender_company]['name']
    if user_type == 'employee':
        employee_name = companies[sender_company]['employees'][session['employee_id']]['name']
        sender_name = f"{employee_name} ({companies[sender_company]['name']})"
    
    message = {
        'sender': sender_name,
        'sender_company': sender_company,
        'message': data['message'],
        'timestamp': datetime.now().strftime('%H:%M'),
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    
    chat_messages[chat_id]['messages'].append(message)
    
    return jsonify({
        'success': True,
        'chat_id': chat_id,
        'message': 'Chat initiated successfully'
    })

@app.route('/api/company_chats')
def get_company_chats():
    if 'company_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    company_id = session['company_id']
    company_chats = []
    
    # Find all chats involving this company
    for chat_id, chat_data in chat_messages.items():
        if company_id in chat_data.get('participants', []):
            # Get the other company name
            other_company = None
            for participant in chat_data['participants']:
                if participant != company_id:
                    other_company = companies.get(participant, {}).get('name', participant)
                    break
            
            # Get last message
            last_message = None
            if chat_data['messages']:
                last_message = chat_data['messages'][-1]
            
            company_chats.append({
                'chat_id': chat_id,
                'other_company': other_company,
                'product': chat_data.get('product', 'Unknown Product'),
                'last_message': last_message,
                'message_count': len(chat_data['messages']),
                'initiated_at': chat_data.get('initiated_at')
            })
    
    return jsonify(company_chats)



@app.route('/api/purchase', methods=['POST'])
def purchase_product():
    data = request.json
    seller_company_id = data.get('company_id')
    product_id = int(data.get('product_id'))
    quantity = int(data.get('quantity', 1))
    payment_method = data.get('payment_method', 'pay-now')
    
    # Find the product in seller's inventory
    product_found = None
    for company_id, company_products in products.items():
        if company_id == seller_company_id:
            for product in company_products:
                if product['id'] == product_id:
                    product_found = product
                    break
            break
    
    if not product_found:
        return jsonify({'success': False, 'message': "Product not found."})
    
    if product_found['quantity'] < quantity:
        return jsonify({
            'success': False,
            'message': f"Insufficient stock. Only {product_found['quantity']} available."
        })
    
    # Update inventory
    product_found['quantity'] -= quantity
    total_price = product_found['price'] * quantity
    
    # Generate contract
    buyer_company = session.get('company_id')
    contract_id = f"PUR-{datetime.now().strftime('%Y%m%d')}-{len(contracts) + 1:03d}"
    
    purchase_contract = {
        'id': contract_id,
        'title': f'اتفاقية شراء - {product_found["title"]}',
        'buyer': companies[buyer_company]['name'],
        'seller': companies[seller_company_id]['name'],
        'amount': total_price,
        'payment_method': payment_method,
        'status': 'نشط',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': 'buyer-seller',
        'product': product_found['title'],
        'quantity': quantity
    }
    
    contracts.append(purchase_contract)
    
    return jsonify({
        'success': True,
        'message': f"Purchase successful! {quantity} x {product_found['title']} for ${total_price:.2f}",
        'order_id': f"ORD-{product_id}-{quantity}",
        'total': total_price
    })



@app.route('/api/chat/<chat_id>', methods=['GET', 'POST'])
def api_chat(chat_id):
    if 'company_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Check if user's company is part of this chat
    if chat_id in chat_messages:
        if session['company_id'] not in chat_messages[chat_id].get('participants', []):
            return jsonify({'error': 'Access denied'}), 403
    
    if request.method == 'POST':
        user_role = session.get('role', 'company')
        user_type = session.get('user_type')
        
        # Check permissions: only company, manager, and sales can reply
        if user_type == 'employee' and user_role not in ['manager', 'sales']:
            return jsonify({'error': 'Insufficient permissions to reply'}), 403
        
        data = request.json
        
        # Determine sender name
        sender_name = companies[session['company_id']]['name']
        if user_type == 'employee':
            employee_name = companies[session['company_id']]['employees'][session['employee_id']]['name']
            sender_name = f"{employee_name} ({companies[session['company_id']]['name']})"
        
        message = {
            'sender': sender_name,
            'sender_company': session['company_id'],
            'message': data['message'],
            'timestamp': datetime.now().strftime('%H:%M'),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        if chat_id not in chat_messages:
            return jsonify({'error': 'Chat not found'}), 404
            
        chat_messages[chat_id]['messages'].append(message)
        
        return jsonify({'success': True})
    
    # Return messages for GET request
    if chat_id in chat_messages:
        return jsonify(chat_messages[chat_id]['messages'])
    else:
        return jsonify([])

@app.route('/api/generate_contracts', methods=['POST'])
def generate_contracts():
    if 'company_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    buyer_company = session['company_id']
    seller_company = data['seller_company']
    product_title = data['product_title']
    quantity = data['quantity']
    total_amount = float(data['total_amount'])
    
    contract_id_1 = f"TRB-{datetime.now().strftime('%Y%m%d')}-{len(contracts) + 1:03d}"
    contract_id_2 = f"PUR-{datetime.now().strftime('%Y%m%d')}-{len(contracts) + 2:03d}"
    
    torbiona_contract = {
        'id': contract_id_1,
        'title': f'اتفاقية تمويل تربيونا - {product_title}',
        'buyer': companies[buyer_company]['name'],
        'seller': 'تربيونا للخدمات المالية',
        'amount': total_amount,
        'payment_method': 'torbiona',
        'status': 'نشط',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': 'buyer-torbiona',
        'product': product_title,
        'quantity': quantity
    }
    
    purchase_contract = {
        'id': contract_id_2,
        'title': f'اتفاقية شراء - {product_title}',
        'buyer': companies[buyer_company]['name'],
        'seller': companies[seller_company]['name'],
        'amount': total_amount,
        'payment_method': 'torbiona',
        'status': 'نشط',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': 'buyer-seller',
        'product': product_title,
        'quantity': quantity
    }
    
    contracts.extend([torbiona_contract, purchase_contract])
    
    return jsonify({
        'success': True,
        'contracts': [contract_id_1, contract_id_2],
        'message': 'تم إنشاء العقود بنجاح'
    })

@app.route('/api/generate_sample_contract', methods=['POST'])
def generate_sample_contract():
    if 'company_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    company_id = session['company_id']
    contract_id = f"SAMPLE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    sample_contract = {
        'id': contract_id,
        'title': f'Sample Contract - {companies[company_id]["name"]}',
        'buyer': companies[company_id]['name'],
        'seller': 'Sample Supplier Co.',
        'amount': 25000.00,
        'payment_method': 'pay-now',
        'status': 'Active',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': 'buyer-seller',
        'product': 'Sample Construction Materials',
        'quantity': 10
    }
    
    contracts.append(sample_contract)
    
    return jsonify({
        'success': True,
        'contract_id': contract_id,
        'message': 'Sample contract generated successfully'
    })

@app.route('/contract/<contract_id>')
def view_contract(contract_id):
    if 'company_id' not in session:
        return redirect(url_for('login'))
    
    contract = None
    for c in contracts:
        if c['id'] == contract_id:
            contract = c
            break
    
    if not contract:
        return redirect(url_for('crm_dashboard'))
    
    lang = session.get('language', 'en')
    return render_template('contract.html', contract=contract, lang=lang, t=translations[lang])

@app.route('/torbiona-calculator')
def torbiona_calculator():
    import random
    order_data = request.args.get('order')
    lang = session.get('language', 'en')
    
    # Generate random scores for each category (each worth 20%)
    behavioral = random.randint(30, 100)
    financial = random.randint(30, 100)
    market = random.randint(30, 100)
    technical = random.randint(30, 100)
    governmental = random.randint(30, 100)
    
    # Calculate total score (average of all categories)
    total_score = (behavioral + financial + market + technical + governmental) / 5
    
    # Approval if score >= 50%
    approved = total_score >= 50
    
    return render_template('torbiona_calculator.html', 
                         approved=approved, 
                         score=int(total_score),
                         behavioral=behavioral,
                         financial=financial,
                         market=market,
                         technical=technical,
                         governmental=governmental,
                         order_data=order_data,
                         lang=lang, 
                         t=translations[lang])

@app.route('/register', methods=['POST'])
def register_company():
    current_lang = session.get('language', 'en')
    
    company_id = request.form['company_id']
    company_name = request.form['company_name']
    industry = request.form['industry']
    commercial_registration = request.form['commercial_registration']
    password = request.form['password']
    
    if company_id in companies:
        return render_template('login.html', error='Company ID already exists', companies=companies, lang=current_lang, t=translations[current_lang])
    
    # Add new company
    companies[company_id] = {
        'password': password,
        'name': company_name,
        'industry': industry,
        'commercial_registration': commercial_registration,
        'employees': {}
    }
    
    # Initialize empty products for new company
    products[company_id] = []
    
    return render_template('login.html', success='Company registered successfully! You can now login.', companies=companies, lang=current_lang, t=translations[current_lang])

@app.route('/register_sabic')
def register_sabic():
    # Auto-login as SABIC and go to registration steps
    session['company_id'] = 'sabic'
    session['user_type'] = 'company'
    return redirect(url_for('registration_steps'))

@app.route('/registration_steps')
def registration_steps():
    if 'company_id' not in session:
        return redirect(url_for('login'))
    
    company_id = session['company_id']
    company = companies[company_id]
    lang = session.get('language', 'en')
    
    return render_template('registration_steps.html', 
                         company=company,
                         company_id=company_id,
                         lang=lang,
                         t=translations[lang])

@app.route('/market-analytics')
def market_analytics():
    if 'company_id' not in session:
        return redirect(url_for('login'))
    
    # Only allow managers and marketing employees
    user_role = session.get('role', 'company')
    user_type = session.get('user_type')
    
    if user_type == 'employee' and user_role not in ['manager', 'marketing']:
        return redirect(url_for('crm_dashboard'))
    
    current_lang = session.get('language', 'en')
    company_id = session['company_id']
    company = companies[company_id]
    
    return render_template('market_analytics.html', 
                         company=company,
                         company_id=company_id,
                         user_role=user_role,
                         session=session,
                         lang=current_lang,
                         t=translations[current_lang])

@app.route('/packages')
def packages():
    if 'company_id' not in session:
        return redirect(url_for('login'))
    
    # Only allow managers and marketing employees
    user_role = session.get('role', 'company')
    user_type = session.get('user_type')
    
    if user_type == 'employee' and user_role not in ['manager', 'marketing']:
        return redirect(url_for('crm_dashboard'))
    
    current_lang = session.get('language', 'en')
    company_id = session['company_id']
    company = companies[company_id]
    
    return render_template('packages.html', 
                         company=company,
                         company_id=company_id,
                         user_role=user_role,
                         session=session,
                         lang=current_lang,
                         t=translations[current_lang])

@app.route('/api/assign_delivery', methods=['POST'])
def assign_delivery():
    if 'company_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    company_id = session['company_id']
    
    # Only logistics companies can assign delivery services
    if companies[company_id]['industry'] != 'Logistics':
        return jsonify({'error': 'Only logistics companies can assign delivery services'}), 403
    
    # Only managers can assign delivery services
    user_role = session.get('role', 'company')
    if user_role not in ['manager'] and session.get('user_type') != 'company':
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    data = request.json
    product_id = data.get('product_id')
    service_id = data.get('service_id')
    price_per_quantity = data.get('price_per_quantity', {})
    
    if company_id not in delivery_services:
        delivery_services[company_id] = {'services': [], 'assigned_products': []}
    
    # Check if product is already assigned
    assigned_products = delivery_services[company_id]['assigned_products']
    existing_assignment = next((p for p in assigned_products if p['product_id'] == product_id), None)
    
    if existing_assignment:
        # Update existing assignment
        existing_assignment['service_id'] = service_id
        existing_assignment['price_per_quantity'] = price_per_quantity
    else:
        # Add new assignment
        assigned_products.append({
            'product_id': product_id,
            'service_id': service_id,
            'price_per_quantity': price_per_quantity
        })
    
    return jsonify({'success': True, 'message': 'Delivery service assigned successfully'})

@app.route('/company/<company_id>')
def company_page(company_id):
    if company_id not in companies:
        return redirect(url_for('index'))
    
    company = companies[company_id]
    company_products = products.get(company_id, [])
    lang = session.get('language', 'en')
    
    # Mock company info (in real app, this would be from database)
    company_info = {
        'about_us': None  # Will use default text in template
    }
    
    return render_template('company.html',
                         company=company,
                         company_id=company_id,
                         company_products=company_products,
                         company_info=company_info,
                         lang=lang,
                         t=translations[lang])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)