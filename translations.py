"""
Multi-language translation support for Bill Splitter
"""

TRANSLATIONS = {
    'en': {
        # Navigation
        'app_title': '💰 Bill Splitter',
        'dashboard': 'Dashboard',
        'logout': 'Logout',
        'help': 'Help',
        'language': 'Language',
        
        # Help Guide
        'help_title': 'How to Use Bill Splitter',
        'help_close': 'Close',
        
        # Help Sections
        'help_overview_title': '📚 Overview',
        'help_overview_content': 'Bill Splitter helps roommates track shared expenses and calculate who owes what. Create profiles for your household, add monthly periods, track bills, and manage usage adjustments.',
        
        'help_profile_title': '🏠 Creating a Profile',
        'help_profile_content': 'A profile represents your household. Start by creating a profile, then add all roommates who share expenses. Each profile can have multiple monthly billing periods.',
        
        'help_months_title': '📅 Monthly Billing Periods',
        'help_months_content': 'Each month is a separate billing period. Create a new month to track bills for that period. You can have multiple active months and view historical data.',
        
        'help_bills_title': '💰 Adding Bills',
        'help_bills_content': 'Add bills by clicking "+ Bill". Specify the bill type (Gas, Electricity, Water, or Extras), amount, date range, and who paid. Bills are automatically split equally among all roommates by default.',
        
        'help_adjustment_title': '⚙️ Usage Adjustments',
        'help_adjustment_content': 'If a roommate was away during part of the billing period, add an adjustment to exclude them from bills during that time. This ensures fair billing based on actual usage.',
        
        'help_exclude_title': '⊘ Excluding Members',
        'help_exclude_content': 'When adding a bill, you can exclude specific roommates who should not be charged for that expense. Useful for personal purchases or items not shared by everyone.',
        
        'help_calculation_title': '🧮 How Calculations Work',
        'help_calculation_content': 'Bills are split equally among active roommates for the billing period. Adjustments reduce someone\'s share proportionally based on days absent. The system calculates who paid what versus who owes what, showing final balances.',
        
        'help_summary_title': '📊 Payment Summary',
        'help_summary_content': 'The summary shows each person\'s total bills, what they paid, and their final balance. "Gets" means they overpaid and should receive money. "Owes" means they need to pay. The system verifies all bills match all splits.',
        
        # Common
        'back': '← Back',
        'add': 'Add',
        'edit': 'Edit',
        'delete': 'Delete',
        'save': 'Save',
        'cancel': 'Cancel',
        'close': 'Close',
    },
    
    'zh': {
        # Navigation
        'app_title': '💰 账单分摊器',
        'dashboard': '仪表板',
        'logout': '登出',
        'help': '帮助',
        'language': '语言',
        
        # Help Guide
        'help_title': '如何使用账单分摊器',
        'help_close': '关闭',
        
        # Help Sections
        'help_overview_title': '📚 概述',
        'help_overview_content': '账单分摊器帮助室友追踪共同支出并计算谁欠谁。为您的家庭创建配置文件，添加每月周期，跟踪账单，并管理使用调整。',
        
        'help_profile_title': '🏠 创建配置文件',
        'help_profile_content': '配置文件代表您的家庭。首先创建一个配置文件，然后添加所有分摊费用的室友。每个配置文件可以有多个月度计费周期。',
        
        'help_months_title': '📅 月度计费周期',
        'help_months_content': '每个月是一个单独的计费周期。创建新月份以跟踪该期间的账单。您可以有多个活动月份并查看历史数据。',
        
        'help_bills_title': '💰 添加账单',
        'help_bills_content': '点击"+ 账单"添加账单。指定账单类型（燃气、电力、水或其他）、金额、日期范围和付款人。默认情况下，账单会在所有室友之间平均分摊。',
        
        'help_adjustment_title': '⚙️ 使用调整',
        'help_adjustment_content': '如果室友在计费期间的部分时间不在，添加调整以在该期间排除他们的账单。这确保基于实际使用情况的公平计费。',
        
        'help_exclude_title': '⊘ 排除成员',
        'help_exclude_content': '添加账单时，您可以排除不应收取该费用的特定室友。适用于个人购买或不是每个人共享的物品。',
        
        'help_calculation_title': '🧮 计算方式',
        'help_calculation_content': '账单在计费期间的活跃室友之间平均分摊。调整根据缺席天数按比例减少某人的份额。系统计算谁付了什么与谁欠什么，显示最终余额。',
        
        'help_summary_title': '📊 付款摘要',
        'help_summary_content': '摘要显示每个人的总账单、他们支付的金额和最终余额。"获得"表示他们多付了应该收到钱。"欠款"表示他们需要付款。系统验证所有账单与所有分摊匹配。',
        
        # Common
        'back': '← 返回',
        'add': '添加',
        'edit': '编辑',
        'delete': '删除',
        'save': '保存',
        'cancel': '取消',
        'close': '关闭',
    },
    
    'ja': {
        # Navigation
        'app_title': '💰 請求書分割ツール',
        'dashboard': 'ダッシュボード',
        'logout': 'ログアウト',
        'help': 'ヘルプ',
        'language': '言語',
        
        # Help Guide
        'help_title': '請求書分割ツールの使い方',
        'help_close': '閉じる',
        
        # Help Sections
        'help_overview_title': '📚 概要',
        'help_overview_content': '請求書分割ツールは、ルームメイトが共有費用を追跡し、誰が何を負っているかを計算するのに役立ちます。世帯のプロファイルを作成し、月次期間を追加し、請求書を追跡し、使用調整を管理します。',
        
        'help_profile_title': '🏠 プロファイルの作成',
        'help_profile_content': 'プロファイルは世帯を表します。まずプロファイルを作成し、費用を共有するすべてのルームメイトを追加します。各プロファイルには複数の月次請求期間を設定できます。',
        
        'help_months_title': '📅 月次請求期間',
        'help_months_content': '各月は個別の請求期間です。その期間の請求書を追跡するために新しい月を作成します。複数のアクティブな月を持ち、履歴データを表示できます。',
        
        'help_bills_title': '💰 請求書の追加',
        'help_bills_content': '「+ 請求書」をクリックして請求書を追加します。請求書の種類（ガス、電気、水道、その他）、金額、日付範囲、支払者を指定します。デフォルトでは、請求書はすべてのルームメイト間で均等に分割されます。',
        
        'help_adjustment_title': '⚙️ 使用調整',
        'help_adjustment_content': 'ルームメイトが請求期間の一部不在だった場合、その期間の請求書から除外する調整を追加します。これにより、実際の使用状況に基づいた公平な請求が保証されます。',
        
        'help_exclude_title': '⊘ メンバーの除外',
        'help_exclude_content': '請求書を追加する際、その費用を請求すべきでない特定のルームメイトを除外できます。個人的な購入や全員が共有しないアイテムに便利です。',
        
        'help_calculation_title': '🧮 計算方法',
        'help_calculation_content': '請求書は請求期間中のアクティブなルームメイト間で均等に分割されます。調整により、不在日数に基づいて誰かの負担が比例的に減少します。システムは誰が何を支払ったかと誰が何を負っているかを計算し、最終残高を表示します。',
        
        'help_summary_title': '📊 支払いサマリー',
        'help_summary_content': 'サマリーには、各人の総請求額、支払った金額、最終残高が表示されます。「受取」は過払いで受け取るべき金額を意味します。「支払」は支払う必要がある金額を意味します。システムはすべての請求書がすべての分割と一致することを確認します。',
        
        # Common
        'back': '← 戻る',
        'add': '追加',
        'edit': '編集',
        'delete': '削除',
        'save': '保存',
        'cancel': 'キャンセル',
        'close': '閉じる',
    },
    
    'bn': {
        # Navigation
        'app_title': '💰 বিল বিভাজক',
        'dashboard': 'ড্যাশবোর্ড',
        'logout': 'লগআউট',
        'help': 'সাহায্য',
        'language': 'ভাষা',
        
        # Help Guide
        'help_title': 'বিল বিভাজক কীভাবে ব্যবহার করবেন',
        'help_close': 'বন্ধ করুন',
        
        # Help Sections
        'help_overview_title': '📚 সংক্ষিপ্ত বিবরণ',
        'help_overview_content': 'বিল বিভাজক রুমমেটদের ভাগ করা খরচ ট্র্যাক করতে এবং কে কী পাওনা তা গণনা করতে সাহায্য করে। আপনার পরিবারের জন্য প্রোফাইল তৈরি করুন, মাসিক সময়কাল যোগ করুন, বিল ট্র্যাক করুন এবং ব্যবহার সমন্বয় পরিচালনা করুন।',
        
        'help_profile_title': '🏠 প্রোফাইল তৈরি',
        'help_profile_content': 'একটি প্রোফাইল আপনার পরিবারকে প্রতিনিধিত্ব করে। প্রথমে একটি প্রোফাইল তৈরি করুন, তারপরে খরচ ভাগ করে এমন সমস্ত রুমমেট যোগ করুন। প্রতিটি প্রোফাইলে একাধিক মাসিক বিলিং সময়কাল থাকতে পারে।',
        
        'help_months_title': '📅 মাসিক বিলিং সময়কাল',
        'help_months_content': 'প্রতিটি মাস একটি পৃথক বিলিং সময়কাল। সেই সময়ের জন্য বিল ট্র্যাক করতে একটি নতুন মাস তৈরি করুন। আপনি একাধিক সক্রিয় মাস রাখতে এবং ঐতিহাসিক ডেটা দেখতে পারেন।',
        
        'help_bills_title': '💰 বিল যোগ করা',
        'help_bills_content': '"+ বিল" ক্লিক করে বিল যোগ করুন। বিলের ধরন (গ্যাস, বিদ্যুৎ, পানি বা অতিরিক্ত), পরিমাণ, তারিখ পরিসীমা এবং কে পরিশোধ করেছে তা নির্দিষ্ট করুন। ডিফল্টরূপে, বিল সমস্ত রুমমেটদের মধ্যে সমানভাবে বিভক্ত হয়।',
        
        'help_adjustment_title': '⚙️ ব্যবহার সমন্বয়',
        'help_adjustment_content': 'যদি কোনও রুমমেট বিলিং সময়ের অংশে অনুপস্থিত ছিল, তাদের সেই সময়ে বিল থেকে বাদ দিতে একটি সমন্বয় যোগ করুন। এটি প্রকৃত ব্যবহারের উপর ভিত্তি করে ন্যায্য বিলিং নিশ্চিত করে।',
        
        'help_exclude_title': '⊘ সদস্য বাদ দেওয়া',
        'help_exclude_content': 'বিল যোগ করার সময়, আপনি নির্দিষ্ট রুমমেটদের বাদ দিতে পারেন যাদের সেই খরচের জন্য চার্জ করা উচিত নয়। ব্যক্তিগত কেনাকাটা বা সবার দ্বারা ভাগ করা হয় না এমন আইটেমগুলির জন্য উপযোগী।',
        
        'help_calculation_title': '🧮 গণনা কীভাবে কাজ করে',
        'help_calculation_content': 'বিলিং সময়ের জন্য সক্রিয় রুমমেটদের মধ্যে বিল সমানভাবে বিভক্ত হয়। সমন্বয় অনুপস্থিত দিনের উপর ভিত্তি করে কারও অংশ আনুপাতিকভাবে হ্রাস করে। সিস্টেম কে কী পরিশোধ করেছে বনাম কে কী পাওনা তা গণনা করে, চূড়ান্ত ব্যালেন্স দেখায়।',
        
        'help_summary_title': '📊 পেমেন্ট সারাংশ',
        'help_summary_content': 'সারাংশ প্রতিটি ব্যক্তির মোট বিল, তারা কী পরিশোধ করেছে এবং তাদের চূড়ান্ত ব্যালেন্স দেখায়। "পায়" মানে তারা অতিরিক্ত পরিশোধ করেছে এবং অর্থ পাওয়া উচিত। "পাওনা" মানে তাদের পরিশোধ করতে হবে। সিস্টেম যাচাই করে যে সমস্ত বিল সমস্ত বিভাজনের সাথে মিলে যায়।',
        
        # Common
        'back': '← পিছনে',
        'add': 'যোগ করুন',
        'edit': 'সম্পাদনা',
        'delete': 'মুছুন',
        'save': 'সংরক্ষণ',
        'cancel': 'বাতিল',
        'close': 'বন্ধ করুন',
    },
    
    'es': {
        # Navigation
        'app_title': '💰 Divisor de Facturas',
        'dashboard': 'Panel',
        'logout': 'Cerrar sesión',
        'help': 'Ayuda',
        'language': 'Idioma',
        
        # Help Guide
        'help_title': 'Cómo usar el Divisor de Facturas',
        'help_close': 'Cerrar',
        
        # Help Sections
        'help_overview_title': '📚 Descripción general',
        'help_overview_content': 'El Divisor de Facturas ayuda a los comp