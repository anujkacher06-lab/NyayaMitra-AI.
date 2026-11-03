// NyayaMitra AI - Frontend Controller & Bilingual State Engine

const i18n = {
  en: {
    heroBadge: "Govt-Verified Legal Information Assistant",
    heroTitlePrefix: "Accessible Legal Guidance for ",
    heroTitleGradient: "Every Indian Citizen",
    heroSubtitle: "Get instant, simple procedural explanations, official emergency helplines, evidence checklists, and ready-to-use complaint drafts.",
    emergencyBanner: "Immediate Financial Cyber Fraud Helpline:",
    categoryHeading: "Choose Your Legal Issue Category",
    catCyberTitle: "Cyber & Financial Fraud",
    catCyberDesc: "Fake UPI links, OTP scams, unauthorized bank debits, phishing, and impersonation.",
    catConsumerTitle: "Consumer Complaints",
    catConsumerDesc: "Defective goods, denied refunds, fake products, and e-commerce service deficiencies.",
    catWorkplaceTitle: "Workplace & Salary Issues",
    catWorkplaceDesc: "Unpaid wages, delayed salaries, withheld PF/gratuity, and wrongful termination.",
    catTenancyTitle: "Tenancy & Rent Disputes",
    catTenancyDesc: "Withheld security deposits, illegal eviction notice, arbitrary rent hike & basic utility cuts.",
    catRtiTitle: "RTI (Right to Information)",
    catRtiDesc: "Seeking government records, pending pension/scholarship status, and public project audit.",
    formHeading: "Describe Your Legal Problem",
    labelCategory: "Legal Category",
    labelName: "Your Full Name",
    labelState: "Your State / UT",
    labelProblem: "Describe What Happened",
    optionalTag: "(Optional)",
    placeholderProblem: "e.g., I received an SMS with a link claiming electricity bill overdue. After clicking it and entering UPI PIN, ₹15,000 was debited from my account.",
    samplePromptsLabel: "Try Quick Demos:",
    sampleCyber: "₹5,000 deducted after clicking fake UPI link",
    sampleConsumer: "Flipkart refused refund for damaged phone delivery",
    sampleSalary: "Employer has not paid last 2 months salary & F&F",
    sampleTenancy: "Landlord refusing ₹40,000 deposit refund after vacating",
    sampleRti: "File RTI for pending scholarship status & delay reason",
    btnAnalyze: "Analyze & Get Legal Guidance",
    btnAnalyzing: "Analyzing Verified Laws & Portals...",
    btnVoiceInput: "Voice Input (बोलकर लिखें)",
    btnListening: "Listening... (सुन रहे हैं)",
    btnScanReceipt: "Scan Receipt / Screenshot",
    btnScanningReceipt: "Scanning Receipt OCR...",
    ocrSuccessToast: "Receipt parsed successfully! Details auto-filled.",
    ocrErrorToast: "Could not scan receipt. Please enter details below.",
    draftHeading: "Generate Official Complaint Draft",
    btnCopy: "Copy Draft",
    btnCopied: "Copied to Clipboard!",
    btnDownload: "Download Draft (.txt)",
    btnPrint: "Print / Save PDF",
    checklistProgress: "Documents Prepared:"
  },
  hi: {
    heroBadge: "सत्यापित भारतीय कानूनी सूचना सहायक",
    heroTitlePrefix: "हर भारतीय नागरिक के लिए ",
    heroTitleGradient: "सरल व सुलभ कानूनी समाधान",
    heroSubtitle: "जटिल कानूनी प्रक्रियाओं की आसान व्याख्या, आधिकारिक हेल्पलाइन (1930/1915), साक्ष्य चेकलिस्ट और संपादन योग्य शिकायत प्रारूप प्राप्त करें।",
    emergencyBanner: "साइबर वित्तीय धोखाधड़ी आपातकालीन हेल्पलाइन:",
    categoryHeading: "अपनी कानूनी समस्या की श्रेणी चुनें",
    catCyberTitle: "साइबर और वित्तीय धोखाधड़ी",
    catCyberDesc: "फर्जी यूपीआई लिंक, ओटीपी फ्रॉड, खाते से अनाधिकृत पैसे कटना, ऑनलाइन ब्लैकमेल।",
    catConsumerTitle: "उपभोक्ता शिकायत व विवाद",
    catConsumerDesc: "खराब सामान, रिफंड न मिलना, ई-कॉमर्स धोखाधड़ी, वारंटी से इनकार।",
    catWorkplaceTitle: "कार्यस्थल व वेतन संबंधी समस्याएं",
    catWorkplaceDesc: "रुकी हुई सैलरी, वेतन में अनुचित कटौती, पीएफ/ग्रेच्युटी रोकना, अवैध सेवा समाप्ति।",
    catTenancyTitle: "किरायेदारी व मकान मालिक विवाद",
    catTenancyDesc: "सिक्योरिटी डिपॉजिट रोकना, अवैध बेदखली नोटिस, मनमाना किराया व सुविधाएं काटना।",
    catRtiTitle: "सूचना का अधिकार (RTI)",
    catRtiDesc: "सरकारी फाइलों की प्रति, छात्रवृत्ति/पेंशन देरी, और योजनाओं के ऑडिट की सूचना।",
    formHeading: "अपनी समस्या का विवरण दर्ज करें",
    labelCategory: "समस्या की श्रेणी",
    labelName: "आपका पूरा नाम",
    labelState: "आपका राज्य / केंद्र शासित प्रदेश",
    labelProblem: "घटना का पूरा विवरण लिखें",
    optionalTag: "(वैकल्पिक)",
    placeholderProblem: "उदाहरण: मुझे बिजली बिल बकाया होने का फर्जी एसएमएस मिला। लिंक खोलकर यूपीआई पिन डालते ही बैंक खाते से ₹15,000 कट गए।",
    samplePromptsLabel: "त्वरित डेमो टेस्ट करें:",
    sampleCyber: "फर्जी यूपीआई लिंक पर क्लिक करने से ₹5,000 कट गए",
    sampleConsumer: "फ्लिपकार्ट से टूटा हुआ फोन मिला, रिफंड देने से मना कर रहे हैं",
    sampleSalary: "कंपनी ने पिछले 2 महीने की सैलरी और रिलीविंग लेटर रोक रखा है",
    sampleTenancy: "मकान खाली करने के बाद मकान मालिक ₹40,000 का डिपॉजिट वापस नहीं कर रहा",
    sampleRti: "छात्रवृत्ति न मिलने का कारण जानने हेतु आरटीआई आवेदन",
    btnAnalyze: "कानूनी जानकारी व मार्गदर्शन प्राप्त करें",
    btnAnalyzing: "सत्यापित कानूनों की जांच हो रही है...",
    btnVoiceInput: "बोलकर लिखें (Voice Input)",
    btnListening: "सुन रहे हैं... (Listening)",
    btnScanReceipt: "रसीद स्कैन करें (OCR)",
    btnScanningReceipt: "रसीद स्कैन हो रही है...",
    ocrSuccessToast: "रसीद सफलता से स्कैन की गई! विवरण अपने-आप भर गया है।",
    ocrErrorToast: "रसीद स्कैन नहीं हो सकी। कृपया विवरण नीचे लिखें।",
    draftHeading: "औपचारिक शिकायत प्रारूप तैयार करें",
    btnCopy: "प्रारूप कॉपी करें",
    btnCopied: "कॉपी कर लिया गया!",
    btnDownload: "डाउनलोड करें (.txt)",
    btnPrint: "प्रिंट करें / PDF",
    checklistProgress: "तैयार साक्ष्य दस्तावेज:"
  },
  ta: {
    heroBadge: "அரசு சரிபார்க்கப்பட்ட சட்ட தகவல் உதவியாளர்",
    heroTitlePrefix: "ஒவ்வொரு இந்திய குடிமகனுக்கும் ",
    heroTitleGradient: "சட்ட வழிகாட்டுதல்",
    heroSubtitle: "உடனடி, எளிய நடைமுறை விளக்கங்கள், அதிகாரப்பூர்வ ஹெல்ப்லைன்கள், சான்று பட்டியல்கள் மற்றும் புகார் வரைவுகளைப் பெறுங்கள்.",
    emergencyBanner: "உடனடி நிதி சைபர் மோசடி உதவி எண்:",
    categoryHeading: "உங்கள் சட்ட பிரச்சனை வகையைத் தேர்ந்தெடுக்கவும்",
    catCyberTitle: "சைபர் & நிதி மோசடி",
    catCyberDesc: "போலி UPI இணைப்புகள், OTP மோசடிகள், அங்கீகரிக்கப்படாத வங்கி பற்று, ஃபிஷிங் மற்றும் ஆள்மாறாட்டம்.",
    catConsumerTitle: "நுகர்வோர் புகார்கள்",
    catConsumerDesc: "குறைபாடுள்ள பொருட்கள், மறுக்கப்பட்ட பணத்திரும்பல், போலி தயாரிப்புகள் மற்றும் ஈ-காமர்ஸ் சேவை குறைபாடுகள்.",
    catWorkplaceTitle: "பணியிட & சம்பள பிரச்சினைகள்",
    catWorkplaceDesc: "செலுத்தப்படாத ஊதியங்கள், தாமதமான சம்பளங்கள், நிறுத்திவைக்கப்பட்ட PF/கிராஜுவிட்டி மற்றும் தவறான பணிநீக்கம்.",
    catTenancyTitle: "வாடகை & குத்தகை சர்ச்சைகள்",
    catTenancyDesc: "தடுத்துவைக்கப்பட்ட பாதுகாப்பு வைப்பு, சட்டவிரோத வெளியேற்றம், தன்னிச்சையான வாடகை உயர்வு.",
    catRtiTitle: "RTI (தகவல் அறியும் உரிமை)",
    catRtiDesc: "அரசு ஆவணங்கள் பெறுதல், நிலுவையில் உள்ள ஓய்வூதியம்/உதவித்தொகை நிலை மற்றும் பொது திட்ட தணிக்கை.",
    formHeading: "உங்கள் சட்ட பிரச்சனையை விவரிக்கவும்",
    labelCategory: "சட்ட வகை",
    labelName: "உங்கள் முழு பெயர்",
    labelState: "உங்கள் மாநிலம் / யூ.டி.",
    labelProblem: "என்ன நடந்தது என்று விவரிக்கவும்",
    optionalTag: "(விரும்பினால்)",
    placeholderProblem: "எ.கா., மின்சார பில் அதிகமாக உள்ளது என்று SMS வந்தது. UPI PIN உள்ளிட்டதும் ₹15,000 பற்று வைக்கப்பட்டது.",
    samplePromptsLabel: "விரைவு டெமோக்களை முயற்சிக்கவும்:",
    sampleCyber: "போலி UPI இணைப்பை கிளிக் செய்த பிறகு ₹15,000 பற்று",
    sampleConsumer: "சேதமடைந்த போன் டெலிவரிக்கு Flipkart பணத்திரும்பல் மறுத்தது",
    sampleSalary: "கடந்த 2 மாத சம்பளம் & F&F செலுத்தப்படவில்லை",
    sampleTenancy: "வீடு காலி செய்த பிறகு ₹1,40,000 வைப்பு திரும்பப் பெற மறுப்பு",
    sampleRti: "நிலுவையில் உள்ள உதவித்தொகை நிலைக்கு RTI தாக்கல் செய்யவும்",
    btnAnalyze: "பகுப்பாய்வு செய்து சட்ட வழிகாட்டுதல் பெறவும்",
    btnAnalyzing: "சரிபார்க்கப்பட்ட சட்டங்களை ஆய்வு செய்கிறோம்...",
    btnVoiceInput: "குரல் உள்ளீடு",
    btnListening: "கேட்கிறோம்...",
    btnScanReceipt: "ரசீதை / ஸ்கிரீன்ஷாட்டை ஸ்கேன் செய்யவும்",
    btnScanningReceipt: "OCR ஸ்கேன் செய்கிறோம்...",
    ocrSuccessToast: "ரசீது வெற்றிகரமாக பகுப்பாய்வு செய்யப்பட்டது!",
    ocrErrorToast: "ரசீதை ஸ்கேன் செய்ய முடியவில்லை. கீழே விவரங்களை உள்ளிடவும்.",
    draftHeading: "அதிகாரப்பூர்வ புகார் வரைவை உருவாக்கவும்",
    btnCopy: "வரைவை நகலெடுக்கவும்",
    btnCopied: "கிளிப்போர்டில் நகலெடுக்கப்பட்டது!",
    btnDownload: "வரைவை பதிவிறக்கவும் (.txt)",
    btnPrint: "அச்சிடு / PDF சேமி",
    checklistProgress: "தயாரிக்கப்பட்ட ஆவணங்கள்:"
  },
  te: {
    heroBadge: "ప్రభుత్వం ధృవీకరించిన న్యాయ సమాచార సహాయకుడు",
    heroTitlePrefix: "ప్రతి భారతీయ పౌరుడికీ ",
    heroTitleGradient: "న్యాయ మార్గదర్శకత్వం",
    heroSubtitle: "తక్షణ, సరళమైన విధాన వివరణలు, అధికారిక హెల్ప్‌లైన్‌లు, సాక్ష్యం చెక్‌లిస్ట్‌లు మరియు రెడీమేడ్ ఫిర్యాదు ముసాయిదాలు పొందండి.",
    emergencyBanner: "తక్షణ ఆర్థిక సైబర్ మోసం హెల్ప్‌లైన్:",
    categoryHeading: "మీ చట్టపరమైన సమస్య వర్గాన్ని ఎంచుకోండి",
    catCyberTitle: "సైబర్ & ఆర్థిక మోసం",
    catCyberDesc: "నకిలీ UPI లింకులు, OTP స్కామ్‌లు, అనధికార బ్యాంక్ డెబిట్లు, ఫిషింగ్ మరియు వేషం.",
    catConsumerTitle: "వినియోగదారు ఫిర్యాదులు",
    catConsumerDesc: "లోపభూయిష్ట వస్తువులు, తిరస్కరించిన రీఫండ్లు, నకిలీ ఉత్పత్తులు మరియు ఈ-కామర్స్ సేవా లోపాలు.",
    catWorkplaceTitle: "కార్యాలయ & వేతన సమస్యలు",
    catWorkplaceDesc: "చెల్లించని వేతనాలు, ఆలస్యమైన జీతాలు, నిలిపివేసిన PF/గ్రాచ్యుటీ మరియు తప్పుడు తొలగింపు.",
    catTenancyTitle: "అద్దె & కౌలు వివాదాలు",
    catTenancyDesc: "నిలిపివేసిన భద్రతా డిపాజిట్, చట్టవిరుద్ధమైన తొలగింపు నోటీసు, అనియంత్రిత అద్దె పెంపు.",
    catRtiTitle: "RTI (సమాచార హక్కు)",
    catRtiDesc: "ప్రభుత్వ రికార్డులు పొందడం, పెండింగ్ పెన్షన్/స్కాలర్‌షిప్ స్థితి మరియు ప్రజా ప్రాజెక్ట్ ఆడిట్.",
    formHeading: "మీ చట్టపరమైన సమస్యను వివరించండి",
    labelCategory: "చట్ట వర్గం",
    labelName: "మీ పూర్తి పేరు",
    labelState: "మీ రాష్ట్రం / యూ.టి.",
    labelProblem: "ఏం జరిగిందో వివరించండి",
    optionalTag: "(ఐచ్ఛికం)",
    placeholderProblem: "ఉదా., విద్యుత్ బిల్లు బకాయి ఉందని SMS వచ్చింది. UPI PIN నమోదు చేసిన తర్వాత ₹15,000 డెబిట్ అయింది.",
    samplePromptsLabel: "త్వరిత డెమోలు ప్రయత్నించండి:",
    sampleCyber: "నకిలీ UPI లింక్ క్లిక్ చేసిన తర్వాత ₹15,000 డెబిట్",
    sampleConsumer: "దెబ్బతిన్న ఫోన్ డెలివరీకి Flipkart రీఫండ్ నిరాకరించింది",
    sampleSalary: "చివరి 2 నెలల జీతం & F&F చెల్లించలేదు",
    sampleTenancy: "ఖాళీ చేసిన తర్వాత ₹1,40,000 డిపాజిట్ వాపసు నిరాకరణ",
    sampleRti: "పెండింగ్ స్కాలర్‌షిప్ స్థితికి RTI దాఖలు",
    btnAnalyze: "విశ్లేషించి న్యాయ మార్గదర్శకత్వం పొందండి",
    btnAnalyzing: "ధృవీకరించిన చట్టాలను విశ్లేషిస్తున్నాం...",
    btnVoiceInput: "వాయిస్ ఇన్‌పుట్",
    btnListening: "వింటున్నాం...",
    btnScanReceipt: "రసీదు / స్క్రీన్‌షాట్ స్కాన్ చేయండి",
    btnScanningReceipt: "OCR స్కాన్ చేస్తున్నాం...",
    ocrSuccessToast: "రసీదు విజయవంతంగా విశ్లేషించబడింది!",
    ocrErrorToast: "రసీదు స్కాన్ చేయడం సాధ్యపడలేదు. దయచేసి దిగువ వివరాలు నమోదు చేయండి.",
    draftHeading: "అధికారిక ఫిర్యాదు ముసాయిదా రూపొందించండి",
    btnCopy: "ముసాయిదా కాపీ చేయండి",
    btnCopied: "క్లిప్‌బోర్డ్‌కి కాపీ అయింది!",
    btnDownload: "ముసాయిదా డౌన్‌లోడ్ చేయండి (.txt)",
    btnPrint: "ముద్రించు / PDF సేవ్",
    checklistProgress: "సిద్ధమైన పత్రాలు:"
  },
  bn: {
    heroBadge: "সরকার যাচাইকৃত আইনি তথ্য সহকারী",
    heroTitlePrefix: "প্রতিটি ভারতীয় নাগরিকের জন্য ",
    heroTitleGradient: "আইনি দিকনির্দেশনা",
    heroSubtitle: "তাৎক্ষণিক, সহজ পদ্ধতিগত ব্যাখ্যা, অফিসিয়াল হেল্পলাইন, প্রমাণ চেকলিস্ট এবং রেডিমেড অভিযোগ খসড়া পান।",
    emergencyBanner: "তাৎক্ষণিক আর্থিক সাইবার প্রতারণা হেল্পলাইন:",
    categoryHeading: "আপনার আইনি সমস্যার বিভাগ বেছে নিন",
    catCyberTitle: "সাইবার ও আর্থিক প্রতারণা",
    catCyberDesc: "জাল UPI লিঙ্ক, OTP স্ক্যাম, অননুমোদিত ব্যাঙ্ক ডেবিট, ফিশিং এবং ছদ্মবেশ।",
    catConsumerTitle: "ভোক্তা অভিযোগ",
    catConsumerDesc: "ত্রুটিপূর্ণ পণ্য, প্রত্যাখ্যাত রিফান্ড, নকল পণ্য এবং ই-কমার্স সেবার অপূর্ণতা।",
    catWorkplaceTitle: "কর্মক্ষেত্র ও বেতন সমস্যা",
    catWorkplaceDesc: "অপরিশোধিত মজুরি, বিলম্বিত বেতন, আটকানো PF/গ্র্যাচুইটি এবং অন্যায় বরখাস্ত।",
    catTenancyTitle: "ভাড়া ও লিজ বিরোধ",
    catTenancyDesc: "আটকানো নিরাপত্তা আমানত, বেআইনি উচ্ছেদ নোটিশ, স্বেচ্ছাচারী ভাড়া বৃদ্ধি।",
    catRtiTitle: "RTI (তথ্যের অধিকার)",
    catRtiDesc: "সরকারি নথি প্রাপ্তি, মুলতুবি পেনশন/বৃত্তির অবস্থা এবং সরকারি প্রকল্পের নিরীক্ষা।",
    formHeading: "আপনার আইনি সমস্যা বর্ণনা করুন",
    labelCategory: "আইনি বিভাগ",
    labelName: "আপনার পূর্ণ নাম",
    labelState: "আপনার রাজ্য / ইউ.টি.",
    labelProblem: "কী ঘটেছে তা বর্ণনা করুন",
    optionalTag: "(ঐচ্ছিক)",
    placeholderProblem: "যেমন, বিদ্যুৎ বিল বকেয়া বলে SMS এসেছিল। UPI PIN দেওয়ার পর ₹15,000 কেটে নেওয়া হয়েছে।",
    samplePromptsLabel: "দ্রুত ডেমো চেষ্টা করুন:",
    sampleCyber: "জাল UPI লিঙ্কে ক্লিক করার পর ₹15,000 ডেবিট",
    sampleConsumer: "ক্ষতিগ্রস্ত ফোন ডেলিভারিতে Flipkart রিফান্ড প্রত্যাখ্যান করেছে",
    sampleSalary: "শেষ ২ মাসের বেতন ও F&F দেওয়া হয়নি",
    sampleTenancy: "বাসা ছাড়ার পর ₹1,40,000 ডিপোজিট ফেরত দিতে অস্বীকার",
    sampleRti: "মুলতুবি বৃত্তির অবস্থার জন্য RTI দাখিল করুন",
    btnAnalyze: "বিশ্লেষণ করুন ও আইনি দিকনির্দেশনা পান",
    btnAnalyzing: "যাচাইকৃত আইন বিশ্লেষণ করা হচ্ছে...",
    btnVoiceInput: "ভয়েস ইনপুট",
    btnListening: "শুনছি...",
    btnScanReceipt: "রসিদ / স্ক্রিনশট স্ক্যান করুন",
    btnScanningReceipt: "OCR স্ক্যান করা হচ্ছে...",
    ocrSuccessToast: "রসিদ সফলভাবে বিশ্লেষণ করা হয়েছে!",
    ocrErrorToast: "রসিদ স্ক্যান করা সম্ভব হয়নি। নিচে বিবরণ দিন।",
    draftHeading: "অফিসিয়াল অভিযোগ খসড়া তৈরি করুন",
    btnCopy: "খসড়া কপি করুন",
    btnCopied: "ক্লিপবোর্ডে কপি হয়েছে!",
    btnDownload: "খসড়া ডাউনলোড করুন (.txt)",
    btnPrint: "মুদ্রণ করুন / PDF সংরক্ষণ",
    checklistProgress: "প্রস্তুত নথিপত্র:"
  },
  mr: {
    heroBadge: "सरकार प्रमाणित कायदेशीर माहिती सहाय्यक",
    heroTitlePrefix: "प्रत्येक भारतीय नागरिकासाठी ",
    heroTitleGradient: "कायदेशीर मार्गदर्शन",
    heroSubtitle: "त्वरित, सोप्या प्रक्रियात्मक स्पष्टीकरणे, अधिकृत हेल्पलाइन, पुरावा चेकलिस्ट आणि तयार तक्रार मसुदे मिळवा.",
    emergencyBanner: "तत्काळ आर्थिक सायबर फसवणूक हेल्पलाइन:",
    categoryHeading: "तुमच्या कायदेशीर समस्येची श्रेणी निवडा",
    catCyberTitle: "सायबर व आर्थिक फसवणूक",
    catCyberDesc: "बनावट UPI लिंक, OTP घोटाळे, अनधिकृत बँक डेबिट, फिशिंग आणि तोतयागिरी.",
    catConsumerTitle: "ग्राहक तक्रारी",
    catConsumerDesc: "सदोष वस्तू, नाकारलेला परतावा, बनावट उत्पादने आणि ई-कॉमर्स सेवेतील त्रुटी.",
    catWorkplaceTitle: "कामाच्या ठिकाणी व पगाराच्या समस्या",
    catWorkplaceDesc: "न दिलेले वेतन, विलंबित पगार, रोखलेले PF/ग्रॅच्युइटी आणि अन्यायकारक बडतर्फी.",
    catTenancyTitle: "भाडेकरू व भाडे विवाद",
    catTenancyDesc: "अडवलेली सुरक्षा ठेव, बेकायदेशीर बेदखल नोटीस, मनमानी भाडेवाढ.",
    catRtiTitle: "RTI (माहितीचा अधिकार)",
    catRtiDesc: "सरकारी नोंदी मिळवणे, प्रलंबित पेन्शन/शिष्यवृत्ती स्थिती आणि सार्वजनिक प्रकल्प लेखापरीक्षण.",
    formHeading: "तुमची कायदेशीर समस्या सांगा",
    labelCategory: "कायदेशीर श्रेणी",
    labelName: "तुमचे पूर्ण नाव",
    labelState: "तुमचे राज्य / केंद्रशासित प्रदेश",
    labelProblem: "काय झाले ते सांगा",
    optionalTag: "(पर्यायी)",
    placeholderProblem: "उदा., वीज बिल थकीत असल्याचा SMS आला. UPI PIN टाकल्यावर ₹15,000 कापले गेले.",
    samplePromptsLabel: "जलद डेमो वापरा:",
    sampleCyber: "बनावट UPI लिंक क्लिक केल्यानंतर ₹15,000 डेबिट",
    sampleConsumer: "खराब फोन डिलिव्हरीसाठी Flipkart ने परतावा नाकारला",
    sampleSalary: "मागील 2 महिन्यांचा पगार व F&F दिला नाही",
    sampleTenancy: "घर सोडल्यानंतर ₹1,40,000 ठेव परत करण्यास नकार",
    sampleRti: "प्रलंबित शिष्यवृत्ती स्थितीसाठी RTI दाखल करा",
    btnAnalyze: "विश्लेषण करा व कायदेशीर मार्गदर्शन मिळवा",
    btnAnalyzing: "सत्यापित कायदे विश्लेषण केले जात आहेत...",
    btnVoiceInput: "व्हॉइस इनपुट",
    btnListening: "ऐकत आहोत...",
    btnScanReceipt: "पावती / स्क्रीनशॉट स्कॅन करा",
    btnScanningReceipt: "OCR स्कॅन होत आहे...",
    ocrSuccessToast: "पावती यशस्वीरित्या विश्लेषित!",
    ocrErrorToast: "पावती स्कॅन करणे शक्य झाले नाही. खाली तपशील भरा.",
    draftHeading: "अधिकृत तक्रार मसुदा तयार करा",
    btnCopy: "मसुदा कॉपी करा",
    btnCopied: "क्लिपबोर्डवर कॉपी झाले!",
    btnDownload: "मसुदा डाउनलोड करा (.txt)",
    btnPrint: "मुद्रित करा / PDF जतन करा",
    checklistProgress: "तयार कागदपत्रे:"
  }
};

let currentLang = "en";
let speechRecognition = null;
let isListening = false;

// Map from dropdown value → i18n code
const LANG_VALUE_MAP = {
  "English": "en",
  "Hindi": "hi",
  "Tamil": "ta",
  "Telugu": "te",
  "Bengali": "bn",
  "Marathi": "mr"
};

// Map from i18n code → dropdown value
const LANG_CODE_TO_VALUE = {
  "en": "English", "hi": "Hindi", "ta": "Tamil",
  "te": "Telugu", "bn": "Bengali", "mr": "Marathi"
};

// Web Speech API language codes
const VOICE_LANG_MAP = {
  "en": "en-IN", "hi": "hi-IN", "ta": "ta-IN",
  "te": "te-IN", "bn": "bn-IN", "mr": "mr-IN"
};

function onLanguageSelectChange(value) {
  const code = LANG_VALUE_MAP[value] || "en";
  setLanguage(code);
}

function setLanguage(lang) {
  currentLang = lang;
  const t = i18n[lang] || i18n.en;

  // Update navbar button
  const langToggleBtn = document.getElementById("langToggleBtn");
  if (langToggleBtn) {
    langToggleBtn.innerHTML = lang === "en" ? "🇮🇳 हिंदी में देखें" : "🌐 View in English";
  }

  // Update language select in form
  const langSelect = document.getElementById("languageSelect");
  if (langSelect) {
    langSelect.value = LANG_CODE_TO_VALUE[lang] || "English";
  }

  // Update text nodes by data-i18n
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (t[key]) {
      el.textContent = t[key];
    }
  });

  // Update placeholders
  const problemInput = document.getElementById("problemInput");
  if (problemInput && t.placeholderProblem) {
    problemInput.placeholder = t.placeholderProblem;
  }

  // Update theme button text
  const themeText = document.getElementById("themeText");
  const currentTheme = document.documentElement.getAttribute("data-theme") || "dark";
  if (themeText) {
    if (currentTheme === "light") {
      themeText.textContent = lang === "hi" ? "मिडनाइट" : "Midnight";
    } else {
      themeText.textContent = lang === "hi" ? "कोर्ट रूम" : "Courtroom";
    }
  }

  // Update voice recognition language if active
  if (speechRecognition) {
    speechRecognition.lang = VOICE_LANG_MAP[lang] || "en-IN";
  }
}

function toggleLanguage() {
  const nextLang = currentLang === "en" ? "hi" : "en";
  setLanguage(nextLang);
}

// Courtroom Theme Controller (Midnight Onyx <-> Courtroom Parchment)
function initTheme() {
  const savedTheme = localStorage.getItem("nyayamitra-theme") || "dark";
  applyTheme(savedTheme, false);
}

function applyTheme(theme, notify = true) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("nyayamitra-theme", theme);

  const themeIcon = document.getElementById("themeIcon");
  const themeText = document.getElementById("themeText");
  if (themeIcon && themeText) {
    if (theme === "light") {
      themeIcon.textContent = "🌙";
      themeText.textContent = currentLang === "hi" ? "मिडनाइट" : "Midnight";
    } else {
      themeIcon.textContent = "🏛️";
      themeText.textContent = currentLang === "hi" ? "कोर्ट रूम" : "Courtroom";
    }
  }
  if (notify && typeof showToast === "function") {
    showToast(theme === "light"
      ? (currentLang === "hi" ? "कोर्ट रूम थीम सक्रिय" : "Courtroom Parchment Theme")
      : (currentLang === "hi" ? "मिडनाइट थीम सक्रिय" : "Judicial Midnight Theme")
    );
  }
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "dark";
  const next = current === "light" ? "dark" : "light";
  applyTheme(next, true);
}

// Immediately initialize theme on script evaluation
initTheme();

// Category selection
function selectCategory(cat) {
  const catInput = document.getElementById("categoryInput");
  if (catInput) catInput.value = cat;

  document.querySelectorAll(".cat-card").forEach(c => {
    if (c.getAttribute("data-cat") === cat) {
      c.classList.add("active");
    } else {
      c.classList.remove("active");
    }
  });
}

// Quick fill sample prompt
function fillSamplePrompt(type) {
  const problemInput = document.getElementById("problemInput");
  if (!problemInput) return;

  if (type === "cyber") {
    selectCategory("cyber_fraud");
    if (currentLang === "hi") {
      problemInput.value = "मेरे पास बैंक अधिकारी बनकर एक कॉल आया और उन्होंने केवाईसी अपडेट के नाम पर एक लिंक भेजा। मैंने जैसे ही लिंक पर क्लिक किया, मेरे खाते से ₹5,000 की राशि कट गई।";
    } else {
      problemInput.value = "I received a phone call claiming to be from my bank asking for KYC verification. I was made to click a link, and immediately ₹5,000 was debited from my bank account without my authorization.";
    }
  } else if (type === "consumer") {
    selectCategory("consumer_complaint");
    if (currentLang === "hi") {
      problemInput.value = "मैंने एक ई-कॉमर्स वेबसाइट से ₹22,000 का स्मार्टफोन ऑर्डर किया था। डिलीवरी पर डिब्बा टूटा हुआ निकला और स्क्रीन फूटी थी। मैंने 24 घंटे में रिफंड मांगा लेकिन सेलर ने अनुरोध रिजेक्ट कर दिया।";
    } else {
      problemInput.value = "I ordered a smartphone worth ₹22,000 from an online shopping platform. Upon delivery, the package was damaged and the screen was completely broken. Customer care is refusing a refund or replacement.";
    }
  } else if (type === "salary") {
    selectCategory("workplace_salary_issue");
    if (currentLang === "hi") {
      problemInput.value = "मेरी कंपनी ने पिछले दो महीनों का वेतन नहीं दिया है। जब मैंने इस्तीफा दिया, तो उन्होंने मेरा फुल एंड फाइनल सेटलमेंट और रिलीविंग लेटर भी रोक लिया है।";
    } else {
      problemInput.value = "My employer has failed to disburse my salary for the last 2 consecutive months amounting to ₹90,000. When I tendered my resignation, they also withheld my relieving letter and full and final settlement.";
    }
  } else if (type === "tenancy") {
    selectCategory("tenancy_dispute");
    if (currentLang === "hi") {
      problemInput.value = "मैंने 1 महीने पहले विधिवत नोटिस देकर फ्लैट खाली कर दिया था। रेंट एग्रीमेंट के अनुसार मकान मालिक को 15 दिनों में ₹40,000 का सिक्योरिटी डिपॉजिट वापस करना था, लेकिन वह फोन नहीं उठा रहे हैं।";
    } else {
      problemInput.value = "I vacated my rented apartment after serving proper 30-day written notice. As per the tenancy agreement, the landlord was obligated to refund my refundable security deposit of ₹40,000 within 15 days, but is now withholding it without cause.";
    }
  } else if (type === "rti") {
    selectCategory("rti_assistance");
    if (currentLang === "hi") {
      problemInput.value = "मैंने 8 महीने पहले राज्य सरकार की उच्च शिक्षा छात्रवृत्ति योजना के लिए आवेदन किया था। सभी दस्तावेज सत्यापित होने के बाद भी कोई राशि नहीं मिली। मुझे आवेदन की दैनिक प्रगति और देरी के कारणों की आधिकारिक जानकारी चाहिए।";
    } else {
      problemInput.value = "I applied for the State Government Higher Education Scholarship 8 months ago. Despite all document approvals, no funds have been disbursed. I require certified daily progress reports and reasons for delay under Section 6(1) of RTI Act.";
    }
  }
  problemInput.focus();
}

// Receipt & Document OCR Scanning
async function handleReceiptUpload(event) {
  const fileInput = event.target;
  if (!fileInput.files || fileInput.files.length === 0) return;
  const file = fileInput.files[0];

  const scanBtn = document.getElementById("scanReceiptBtn");
  const scanText = document.getElementById("scanReceiptText");
  const origText = scanText ? scanText.textContent : "Scan Receipt";

  if (scanBtn) scanBtn.classList.add("scanning");
  if (scanText) scanText.textContent = i18n[currentLang]?.btnScanningReceipt || "Scanning Receipt OCR...";
  showToast(currentLang === "hi" ? "रसीद स्कैन की जा रही है..." : "Scanning receipt & extracting transaction entities...");

  const formData = new FormData();
  formData.append("file", file);
  formData.append("language", currentLang === "hi" ? "Hindi" : "English");

  try {
    const res = await fetch("/scan-document", {
      method: "POST",
      body: formData
    });
    const data = await res.json();

    if (data.status === "success") {
      const entities = data.entities || {};
      const problemInput = document.getElementById("problemInput");

      // Auto-fill prompt if returned or synthesize from entities
      if (data.auto_fill_prompt && problemInput) {
        problemInput.value = data.auto_fill_prompt;
      } else if (data.extracted_text && problemInput) {
        problemInput.value = data.extracted_text;
      }

      // Automatically select detected category
      if (entities.detected_category) {
        selectCategory(entities.detected_category);
        const displayCat = document.getElementById("displayCategory");
        if (displayCat) {
          const catMap = {
            "cyber_fraud": "Cyber & Financial Fraud",
            "consumer_complaint": "Consumer Complaints",
            "workplace_salary_issue": "Workplace & Salary Issues",
            "tenancy_dispute": "Tenancy & Rent Disputes",
            "rti_assistance": "RTI (Right to Information)"
          };
          displayCat.value = catMap[entities.detected_category] || entities.detected_category;
        }
      }

      // Render OCR preview card
      renderOcrPreview(data);
      showToast(i18n[currentLang]?.ocrSuccessToast || "Receipt parsed successfully!");
    } else {
      showToast(data.message || (i18n[currentLang]?.ocrErrorToast || "Could not parse receipt."));
    }
  } catch (err) {
    console.error("OCR Scan error:", err);
    showToast(i18n[currentLang]?.ocrErrorToast || "Could not connect to OCR scanner.");
  } finally {
    if (scanBtn) scanBtn.classList.remove("scanning");
    if (scanText) scanText.textContent = origText;
    fileInput.value = "";
  }
}

function renderOcrPreview(data) {
  const card = document.getElementById("ocrPreviewCard");
  const chipsContainer = document.getElementById("ocrEntitiesChips");
  const engineTag = document.getElementById("ocrEngineTag");
  const noteText = document.getElementById("ocrNoteText");
  if (!card || !chipsContainer) return;

  chipsContainer.innerHTML = "";
  if (engineTag) engineTag.textContent = data.ocr_engine || "Vision OCR";

  const entities = data.entities || {};
  const chips = [];

  if (entities.amount) chips.push(`💰 ₹${entities.amount}`);
  if (entities.utr) chips.push(`🔢 UTR: ${entities.utr}`);
  if (entities.payment_app) chips.push(`📱 ${entities.payment_app}`);
  if (entities.incident_date) chips.push(`📅 ${entities.incident_date}`);
  if (entities.detected_category) {
    const catLabel = entities.detected_category.replace(/_/g, " ").toUpperCase();
    chips.push(`🏷️ ${catLabel}`);
  }

  chips.forEach(chipText => {
    const chip = document.createElement("span");
    chip.className = "ocr-chip";
    chip.textContent = chipText;
    chipsContainer.appendChild(chip);
  });

  if (data.note && noteText) {
    noteText.textContent = data.note;
    noteText.style.display = "block";
  } else if (noteText) {
    noteText.style.display = "none";
  }

  card.style.display = "block";
}

function clearOcrPreview() {
  const card = document.getElementById("ocrPreviewCard");
  if (card) card.style.display = "none";
}

// Voice Input via Web Speech API
function toggleVoiceRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const voiceBtn = document.getElementById("voiceBtn");
  const voiceText = document.getElementById("voiceText");
  const problemInput = document.getElementById("problemInput");

  if (!SpeechRecognition) {
    alert(currentLang === "hi"
      ? "आपका ब्राउज़र वॉइस इनपुट का समर्थन नहीं करता है। कृपया गूगल क्रोम (Google Chrome) या एज (Microsoft Edge) का उपयोग करें।"
      : "Speech recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge.");
    return;
  }

  if (isListening && speechRecognition) {
    speechRecognition.stop();
    return;
  }

  speechRecognition = new SpeechRecognition();
  speechRecognition.continuous = false;
  speechRecognition.interimResults = false;
  speechRecognition.lang = VOICE_LANG_MAP[currentLang] || "en-IN";

  speechRecognition.onstart = () => {
    isListening = true;
    if (voiceBtn) voiceBtn.classList.add("listening");
    if (voiceText) voiceText.textContent = i18n[currentLang]?.btnListening || "Listening...";
    showToast(currentLang === "hi" ? "सुन रहे हैं... कृपया अपनी समस्या बोलें" : "Listening... Please describe your issue");
  };

  speechRecognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    if (problemInput) {
      if (problemInput.value.trim().length > 0) {
        problemInput.value += " " + transcript;
      } else {
        problemInput.value = transcript;
      }
    }
    showToast(currentLang === "hi" ? "आवाज रिकॉर्ड हो गई!" : "Voice transcribed successfully!");
  };

  speechRecognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    showToast(currentLang === "hi" ? "वॉइस इनपुट में त्रुटि हुई।" : "Microphone input error.");
  };

  speechRecognition.onend = () => {
    isListening = false;
    if (voiceBtn) voiceBtn.classList.remove("listening");
    if (voiceText) voiceText.textContent = i18n[currentLang]?.btnVoiceInput || "Voice Input (बोलकर लिखें)";
  };

  speechRecognition.start();
}

// Toast notification
function showToast(message) {
  const existing = document.querySelector(".toast-msg");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.className = "toast-msg";
  toast.innerHTML = `
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M20 6L9 17l-5-5"/>
    </svg>
    <span>${message}</span>
  `;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

// Copy draft text
function copyDraft() {
  const draftArea = document.getElementById("complaintDraftText");
  if (!draftArea) return;
  const text = draftArea.value || draftArea.innerText;
  navigator.clipboard.writeText(text).then(() => {
    showToast(currentLang === "hi" ? "शिकायत प्रारूप कॉपी हो गया!" : "Draft copied to clipboard!");
  }).catch(() => {
    draftArea.select();
    document.execCommand("copy");
    showToast("Copied to clipboard!");
  });
}

// Download draft as .txt
function downloadDraft() {
  const draftArea = document.getElementById("complaintDraftText");
  if (!draftArea) return;
  const text = draftArea.value || draftArea.innerText;
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `NyayaMitra_Complaint_Draft_${Date.now()}.txt`;
  a.click();
}

// Print / Export Formal Petition (PDF)
function printFormalPetition() {
  const draftArea = document.getElementById("complaintDraftText");
  const draftText = draftArea ? (draftArea.value || draftArea.innerText) : "";
  const queryId = window.currentQueryId || "";

  // Open /print-draft with POST to pass exact text cleanly
  const form = document.createElement("form");
  form.method = "POST";
  form.action = "/print-draft";
  form.target = "_blank";

  const draftInput = document.createElement("input");
  draftInput.type = "hidden";
  draftInput.name = "draft_text";
  draftInput.value = draftText;
  form.appendChild(draftInput);

  const queryIdInput = document.createElement("input");
  queryIdInput.type = "hidden";
  queryIdInput.name = "query_id";
  queryIdInput.value = queryId;
  form.appendChild(queryIdInput);

  document.body.appendChild(form);
  form.submit();
  form.remove();
}

// Dynamic Draft Generation via AJAX
function generateDraftAjax(categoryId, language) {
  const nameInput = document.getElementById("modalUserName")?.value || "";
  const addressInput = document.getElementById("modalUserAddress")?.value || "";
  const phoneInput = document.getElementById("modalUserPhone")?.value || "";
  const amountInput = document.getElementById("modalAmount")?.value || "";
  const dateInput = document.getElementById("modalDate")?.value || "";
  const descInput = document.getElementById("modalDesc")?.value || "";

  fetch("/generate-draft", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      category: categoryId,
      language: language,
      name: nameInput,
      address: addressInput,
      phone: phoneInput,
      amount: amountInput,
      incident_date: dateInput,
      description: descInput
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "success") {
      const draftBox = document.getElementById("complaintDraftText");
      if (draftBox) {
        draftBox.value = data.draft;
        showToast("Complaint draft updated with your details!");
        closeDraftModal();
      }
    }
  })
  .catch(err => {
    console.error("Draft generation error:", err);
    showToast("Error updating draft.");
  });
}

function openDraftModal() {
  const modal = document.getElementById("draftModal");
  if (modal) modal.classList.add("open");
}

function closeDraftModal() {
  const modal = document.getElementById("draftModal");
  if (modal) modal.classList.remove("open");
}

// Checklist progress counter
function updateChecklistProgress() {
  const checkboxes = document.querySelectorAll(".evidence-chk");
  if (checkboxes.length === 0) return;
  let checked = 0;
  checkboxes.forEach(chk => { if (chk.checked) checked++; });
  const badge = document.getElementById("checklistCounter");
  if (badge) {
    badge.textContent = `${checked} / ${checkboxes.length} Ready`;
  }
}

// Feedback submission
function submitRating(rating, queryId) {
  const stars = document.querySelectorAll(".star");
  stars.forEach((s, idx) => {
    if (idx < rating) s.classList.add("active");
    else s.classList.remove("active");
  });

  const comment = prompt("Optional: Share any comments or feedback for this legal analysis:") || "";

  fetch("/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query_id: queryId,
      rating: rating,
      comments: comment
    })
  })
  .then(res => res.json())
  .then(data => {
    showToast(data.message || "Feedback submitted!");
    const feedbackBox = document.getElementById("feedbackArea");
    if (feedbackBox) {
      feedbackBox.innerHTML = `<p style="color: #34d399; font-weight: 600;">✓ Thank you for your feedback! It helps improve legal accessibility for citizens.</p>`;
    }
  })
  .catch(err => console.error("Feedback error:", err));
}

// Form submission loading state
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("legalQueryForm");
  if (form) {
    form.addEventListener("submit", () => {
      const btn = document.getElementById("submitQueryBtn");
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = `
          <svg style="animation: spin 1s linear infinite;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
            <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"></path>
          </svg>
          <span>${currentLang === "hi" ? "सत्यापित कानूनों की जांच हो रही है..." : "Analyzing Verified Laws & Portals..."}</span>
        `;
      }
    });
  }

  // Attach checklist listener
  document.querySelectorAll(".evidence-chk").forEach(chk => {
    chk.addEventListener("change", updateChecklistProgress);
  });
  updateChecklistProgress();
});

// Quick Share Handlers
function shareViaWhatsApp() {
  const title = document.querySelector(".result-header h2")?.innerText || "NyayaMitra Legal Analysis";
  const cat = document.querySelector(".category-tag-badge strong")?.innerText || "Legal Guidance";
  const url = window.location.href;
  const text = encodeURIComponent(`⚖️ *NyayaMitra AI Legal Guidance*\nCategory: ${cat}\nReview procedural steps, evidence checklist, and emergency helplines at:\n${url}`);
  window.open(`https://api.whatsapp.com/send?text=${text}`, "_blank");
}

function shareViaEmail() {
  const cat = document.querySelector(".category-tag-badge strong")?.innerText || "Legal Guidance";
  const url = window.location.href;
  const subject = encodeURIComponent(`NyayaMitra Legal Guidance: ${cat}`);
  const body = encodeURIComponent(`Citizen Legal Information Report\nCategory: ${cat}\n\nPlease review your action checklist and complaint draft at:\n${url}\n\nEmergency Helplines:\n- Cyber Fraud: 1930\n- Consumer Grievance: 1915\n- NALSA Legal Aid: 15100\n- Tele-Law: 14488`);
  window.location.href = `mailto:?subject=${subject}&body=${body}`;
}

// Follow-Up Chat Handlers
function askFollowUpChip(text) {
  const input = document.getElementById("followUpInput");
  if (input) {
    input.value = text;
    const form = document.getElementById("followUpForm");
    if (form) form.dispatchEvent(new Event("submit", { cancelable: true }));
  }
}

function submitFollowUp(e) {
  if (e) e.preventDefault();
  const input = document.getElementById("followUpInput");
  const thread = document.getElementById("chatThread");
  const sendBtn = document.getElementById("sendFollowUpBtn");
  if (!input || !input.value.trim()) return;

  const userQuestion = input.value.trim();
  input.value = "";

  // Append user bubble
  const userBubble = document.createElement("div");
  userBubble.className = "chat-bubble chat-bubble-user";
  userBubble.textContent = userQuestion;
  thread.appendChild(userBubble);
  thread.scrollTop = thread.scrollHeight;

  // Append thinking bubble
  const aiBubble = document.createElement("div");
  aiBubble.className = "chat-bubble chat-bubble-ai";
  aiBubble.innerHTML = `<em>${currentLang === "hi" ? "कानूनी संदर्भ की जांच की जा रही है..." : "Checking verified statutes..."}</em>`;
  thread.appendChild(aiBubble);
  thread.scrollTop = thread.scrollHeight;

  if (sendBtn) sendBtn.disabled = true;

  fetch("/follow-up", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query_id: window.currentQueryId || null,
      question: userQuestion
    })
  })
  .then(res => res.json())
  .then(data => {
    if (sendBtn) sendBtn.disabled = false;
    if (data.answer) {
      aiBubble.textContent = data.answer;
    } else {
      aiBubble.textContent = "Could not retrieve answer. Please try again or call NALSA 15100.";
    }
    thread.scrollTop = thread.scrollHeight;
  })
  .catch(err => {
    if (sendBtn) sendBtn.disabled = false;
    console.error("Follow-up error:", err);
    aiBubble.textContent = "Network error. Please try again.";
  });
}

// ==========================================================================
// Text-to-Speech (TTS) Voice Readout Controller (Enhanced Natural Indian & Hindi Pronunciation)
// ==========================================================================
let currentSpeechUtterance = null;
let isSpeaking = false;
let isPaused = false;
let speechRate = 1.0;
let cachedVoices = [];

function refreshVoices() {
  if ('speechSynthesis' in window) {
    cachedVoices = window.speechSynthesis.getVoices();
  }
}
if ('speechSynthesis' in window) {
  refreshVoices();
  window.speechSynthesis.onvoiceschanged = refreshVoices;
}

function cleanTextForSpeech(text, isHindi) {
  if (!text) return "";
  let clean = text;
  // Replace symbols and numbers with readable words so TTS doesn't mangle or stumble
  if (isHindi) {
    clean = clean
      .replace(/₹\s*([0-9,]+)/g, "$1 रुपये ")
      .replace(/Rs\.?\s*([0-9,]+)/gi, "$1 रुपये ")
      .replace(/INR\s*([0-9,]+)/gi, "$1 रुपये ")
      .replace(/1930/g, "उन्नीस सौ तीस")
      .replace(/1915/g, "उन्नीस सौ पंद्रह")
      .replace(/15100/g, "पंद्रह सौ सौ")
      .replace(/14488/g, "चौदह चार सौ अठासी")
      .replace(/FIR/gi, "एफ आई आर")
      .replace(/OTP/gi, "ओ टी पी")
      .replace(/UPI/gi, "यू पी आई")
      .replace(/PIN/gi, "पिन")
      .replace(/SMS/gi, "एस एम एस")
      .replace(/cybercrime\.gov\.in/gi, "साइबर क्राइम डॉट जी ओ वी डॉट इन")
      .replace(/NALSA/gi, "नालसा")
      .replace(/BNS/gi, "बी एन एस")
      .replace(/BNSS/gi, "बी एन एस एस")
      .replace(/RTI/gi, "आर टी आई");
  } else {
    clean = clean
      .replace(/₹\s*([0-9,]+)/g, "$1 Rupees ")
      .replace(/Rs\.?\s*([0-9,]+)/gi, "$1 Rupees ")
      .replace(/INR\s*([0-9,]+)/gi, "$1 Rupees ")
      .replace(/cybercrime\.gov\.in/gi, "cyber crime dot gov dot in");
  }

  // Remove URLs, harsh markdown characters, brackets, multiple dots
  clean = clean
    .replace(/https?:\/\/\S+/gi, "")
    .replace(/[\*\_#\[\]\(\)\{\}\<\>\\\/\|\~]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  return clean;
}

function getOptimalVoice(langCode, isHindiText) {
  if (!('speechSynthesis' in window)) return null;
  refreshVoices();
  const voices = cachedVoices.length ? cachedVoices : window.speechSynthesis.getVoices();
  if (!voices || voices.length === 0) return null;

  if (isHindiText || langCode === "hi") {
    // Priority order for high-clarity natural Hindi voices:
    // 1. Google हिन्दी (Chrome Android/Desktop - highest natural quality)
    // 2. Microsoft Swara / Madhur / Hemant (Edge Windows Natural Voices)
    // 3. Apple Lekha / Rishi (macOS/iOS Hindi)
    // 4. Any voice explicitly tagged hi-IN or hi_IN
    const googleHi = voices.find(v => v.lang.replace('_', '-').startsWith("hi") && /google/i.test(v.name));
    if (googleHi) return googleHi;

    const naturalHi = voices.find(v => v.lang.replace('_', '-').startsWith("hi") && /natural|online|neural/i.test(v.name));
    if (naturalHi) return naturalHi;

    const msHi = voices.find(v => v.lang.replace('_', '-').startsWith("hi") && /swara|madhur|hemant|microsoft/i.test(v.name));
    if (msHi) return msHi;

    const anyHi = voices.find(v => v.lang.replace('_', '-').startsWith("hi"));
    if (anyHi) return anyHi;
  }

  // English (Indian accent preferred: Google English India, Microsoft Neerja/Prabhat, Ravi)
  const googleEnIn = voices.find(v => (v.lang === "en-IN" || v.lang === "en_IN") && /google/i.test(v.name));
  if (googleEnIn) return googleEnIn;

  const naturalEnIn = voices.find(v => (v.lang === "en-IN" || v.lang === "en_IN") && /natural|online|neural/i.test(v.name));
  if (naturalEnIn) return naturalEnIn;

  const anyEnIn = voices.find(v => v.lang === "en-IN" || v.lang === "en_IN");
  if (anyEnIn) return anyEnIn;

  // Fallback to clear general English voice (Google US/UK, Microsoft, or default)
  return voices.find(v => v.lang.startsWith("en") && /google/i.test(v.name)) ||
         voices.find(v => v.lang.startsWith("en")) ||
         voices[0];
}

function toggleSpeechReadout() {
  if (!('speechSynthesis' in window)) {
    alert("Speech Synthesis (Voice Readout) is not supported in your browser.");
    return;
  }

  if (isSpeaking && !isPaused) {
    window.speechSynthesis.pause();
    isPaused = true;
    updateTTSUI("paused");
    return;
  } else if (isSpeaking && isPaused) {
    window.speechSynthesis.resume();
    isPaused = false;
    updateTTSUI("speaking");
    return;
  }

  startSpeechReadout();
}

function startSpeechReadout() {
  window.speechSynthesis.cancel();

  const explanationEl = document.querySelector(".card-block p");
  const actionItems = document.querySelectorAll(".step-item .step-content");

  const rawExplanation = explanationEl ? explanationEl.innerText.trim() : "";
  const effectiveLang = window.currentLanguage ? window.currentLanguage.toLowerCase() : currentLang;
  const isHindi = effectiveLang.startsWith("hi") || /[\u0900-\u097F]/.test(rawExplanation);

  let introPrefix = isHindi ? "न्यायमित्र कानूनी मार्गदर्शन। " : "NyayaMitra Legal Guidance. ";
  let actionPrefix = isHindi ? " तुरंत उठाने वाले कदम: " : " Immediate action steps: ";

  let speechSegments = [];
  if (rawExplanation) {
    speechSegments.push(introPrefix + cleanTextForSpeech(rawExplanation, isHindi));
  }

  if (actionItems.length > 0) {
    let actionsText = actionPrefix;
    actionItems.forEach((act, idx) => {
      const stepLabel = isHindi ? `कदम ${idx + 1}: ` : `Step ${idx + 1}: `;
      actionsText += `${stepLabel}${cleanTextForSpeech(act.innerText.trim(), isHindi)}. `;
    });
    speechSegments.push(actionsText);
  }

  const fullTextToRead = speechSegments.join(" ");

  if (!fullTextToRead.trim()) {
    showToast(isHindi ? "बोलने के लिए कोई पाठ नहीं मिला।" : "No legal guidance text found to read.");
    return;
  }

  const utterance = new SpeechSynthesisUtterance(fullTextToRead);
  // Optimal speech pace: slightly slower (0.92x) gives much clearer articulation in Hindi & Indian English
  utterance.rate = speechRate ? (speechRate * 0.94) : 0.94;
  utterance.pitch = isHindi ? 1.05 : 1.0;
  utterance.lang = isHindi ? "hi-IN" : (VOICE_LANG_MAP[currentLang] || "en-IN");

  const voice = getOptimalVoice(isHindi ? "hi" : "en", isHindi);
  if (voice) {
    utterance.voice = voice;
  }

  utterance.onstart = () => {
    isSpeaking = true;
    isPaused = false;
    updateTTSUI("speaking");
  };

  utterance.onend = () => {
    isSpeaking = false;
    isPaused = false;
    updateTTSUI("ready");
  };

  utterance.onerror = (e) => {
    console.error("Speech error:", e);
    isSpeaking = false;
    isPaused = false;
    updateTTSUI("ready");
  };

  currentSpeechUtterance = utterance;
  window.speechSynthesis.speak(utterance);
}

function stopSpeechReadout() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  isSpeaking = false;
  isPaused = false;
  updateTTSUI("ready");
}

function changeSpeechRate(rate) {
  speechRate = parseFloat(rate) || 1.0;
  if (isSpeaking && !isPaused) {
    startSpeechReadout();
  }
}

function updateTTSUI(status) {
  const bar = document.getElementById("ttsPlayerBar");
  const statusPill = document.getElementById("ttsStatusPill");
  const wave = document.getElementById("ttsSoundWave");
  const btnLabel = document.getElementById("ttsBtnLabel");
  const stopBtn = document.getElementById("ttsStopBtn");
  const playSvg = document.getElementById("ttsPlaySvg");

  if (!bar) return;

  if (status === "speaking") {
    bar.classList.add("playing");
    if (statusPill) {
      statusPill.textContent = "Speaking";
      statusPill.className = "tts-status-pill speaking";
    }
    if (wave) wave.style.display = "flex";
    if (btnLabel) btnLabel.textContent = "Pause";
    if (stopBtn) stopBtn.style.display = "inline-flex";
    if (playSvg) playSvg.innerHTML = '<rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect>';
  } else if (status === "paused") {
    bar.classList.remove("playing");
    if (statusPill) {
      statusPill.textContent = "Paused";
      statusPill.className = "tts-status-pill";
    }
    if (wave) wave.style.display = "none";
    if (btnLabel) btnLabel.textContent = "Resume";
    if (stopBtn) stopBtn.style.display = "inline-flex";
    if (playSvg) playSvg.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"></polygon>';
  } else {
    bar.classList.remove("playing");
    if (statusPill) {
      statusPill.textContent = "Ready";
      statusPill.className = "tts-status-pill";
    }
    if (wave) wave.style.display = "none";
    if (btnLabel) btnLabel.textContent = currentLang === "hi" ? "सलाह सुनें" : "Listen Guidance";
    if (stopBtn) stopBtn.style.display = "none";
    if (playSvg) playSvg.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"></polygon>';
  }
}

if ('speechSynthesis' in window) {
  window.speechSynthesis.onvoiceschanged = () => {};
}

// ==========================================================================
// Interactive State Legal Aid Live Switcher
// ==========================================================================
function loadStateAidDropdown(selectElementId, activeStateName = "") {
  const select = document.getElementById(selectElementId);
  if (!select) return;

  fetch("/api/all-states")
    .then(res => res.json())
    .then(data => {
      if (data.status === "success" && data.states) {
        select.innerHTML = '<option value="">-- Choose State / UT --</option>';
        data.states.forEach(st => {
          const opt = document.createElement("option");
          opt.value = st.name;
          opt.textContent = `${st.name} (${st.name_hi})`;
          if (activeStateName && (activeStateName.toLowerCase().includes(st.id) || st.name.toLowerCase().includes(activeStateName.toLowerCase()))) {
            opt.selected = true;
          }
          select.appendChild(opt);
        });
      }
    })
    .catch(err => console.error("Error loading states:", err));
}

function switchStateAid(selectedState) {
  if (!selectedState) return;
  fetch(`/api/state-aid?state=${encodeURIComponent(selectedState)}&language=${currentLang === "hi" ? "Hindi" : "English"}`)
    .then(res => res.json())
    .then(data => {
      if (data.status === "success" && data.state_aid) {
        const aid = data.state_aid;
        const slsaName = document.getElementById("aidSlsaName");
        const slsaHelpline = document.getElementById("aidSlsaHelpline");
        const slsaWebsite = document.getElementById("aidSlsaWebsite");
        const slsaAddress = document.getElementById("aidSlsaAddress");
        const cyberCell = document.getElementById("aidCyberCell");
        const cyberPortal = document.getElementById("aidCyberPortal");
        const consumerComm = document.getElementById("aidConsumerCommission");
        const freeThreshold = document.getElementById("aidFreeThreshold");

        if (slsaName) slsaName.textContent = aid.slsa_name || "State Legal Services Authority";
        if (slsaHelpline) slsaHelpline.innerHTML = `📞 Helpline: ${aid.slsa_helpline || "15100"}`;
        if (slsaWebsite && aid.slsa_website) {
          slsaWebsite.href = aid.slsa_website;
          slsaWebsite.style.display = "block";
        }
        if (slsaAddress) slsaAddress.textContent = aid.slsa_address || "";
        if (cyberCell) cyberCell.textContent = aid.cyber_cell || "State Cyber Crime Police Wing";
        if (cyberPortal && aid.cyber_portal) {
          cyberPortal.href = aid.cyber_portal;
          cyberPortal.style.display = "block";
        }
        if (consumerComm) consumerComm.textContent = aid.consumer_commission || "State Consumer Commission";
        if (freeThreshold) freeThreshold.textContent = aid.free_aid_threshold || "Free legal aid under Section 12, Legal Services Authorities Act, 1987.";

        showToast(`Updated to ${aid.state_name}`);
      }
    })
    .catch(err => console.error("Error fetching state aid:", err));
}

// -------------------------------------------------------------
// 1-Click WhatsApp Statutory Legal Demand Notice Dispatcher
// -------------------------------------------------------------
function openWhatsAppNoticeModal() {
  const modal = document.getElementById("whatsappNoticeModalOverlay");
  if (!modal) return;
  modal.classList.add("open");

  // Pre-fill amount if found in current draft
  const draftText = document.getElementById("complaintDraftText")?.value || "";
  const amountMatch = draftText.match(/(?:Rs\.?|₹|INR)\s*([0-9,]+)/i);
  const amountInput = document.getElementById("waClaimAmount");
  if (amountInput && !amountInput.value && amountMatch) {
    amountInput.value = `₹${amountMatch[1]}`;
  }

  updateWhatsAppPreview();
}

function closeWhatsAppNoticeModal() {
  const modal = document.getElementById("whatsappNoticeModalOverlay");
  if (modal) modal.classList.remove("open");
}

function updateWhatsAppPreview() {
  const recipient = document.getElementById("waRecipientName")?.value.trim() || "[Opposite Party / Landlord / Employer / Merchant]";
  const cureDays = document.getElementById("waCureDays")?.value || "7 Days";
  const claimAmount = document.getElementById("waClaimAmount")?.value.trim() || "[Disputed Amount]";
  const categoryElem = document.querySelector(".category-tag-badge strong");
  const categoryTitle = categoryElem ? categoryElem.innerText.trim() : "Civic Legal Dispute";

  const today = new Date().toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
  const draftText = document.getElementById("complaintDraftText")?.value || "";

  // Summary snippet from draft or fallback
  let summarySnippet = "";
  const lines = draftText.split("\n").filter(l => l.trim().length > 15);
  for (let l of lines) {
    if (!l.startsWith("To,") && !l.startsWith("From:") && !l.startsWith("Subject:") && !l.startsWith("Date:")) {
      summarySnippet = l.trim().substring(0, 160);
      break;
    }
  }
  if (!summarySnippet) {
    summarySnippet = `Regarding the pending grievance and outstanding claim of ${claimAmount} which remains unresolved despite prior requests.`;
  }

  const noticeMessage = 
`🚨 *FORMAL STATUTORY LEGAL DEMAND NOTICE* 🚨
*Date:* ${today}
*To:* ${recipient}
*Subject:* Formal Legal Demand Notice regarding *${categoryTitle}*

Sir / Madam,

Take formal notice that you have failed / refused to redress the following grievance:
"${summarySnippet}"

⚡ *MANDATORY STATUTORY DEMAND:*
You are hereby formally called upon to resolve this grievance and disburse / refund the rightful amount of *${claimAmount}* within *${cureDays}* of receipt of this notice.

⚠️ *NOTICE OF LEGAL CONSEQUENCES:*
Should you fail to comply within the stipulated *${cureDays}*, formal legal proceedings will be immediately initiated against you before:
• National Consumer Commission (e-Daakhil Portal) / Jurisdictional Police Wing
• District Legal Services Authority (DLSA) under Legal Services Authorities Act
• Applicable provisions of the *Bharatiya Nyaya Sanhita (BNS), 2023* and relevant civic statutes.
All litigation expenses, interest, and legal costs will be claimed at your sole liability.

📌 *ELECTRONIC EVIDENCE CERTIFICATION:*
This WhatsApp communication is recorded, timestamped, and preserved as admissible electronic evidence under *Section 63 of Bharatiya Sakshya Adhiniyam (BSA), 2023*.

_Dispatched via NyayaMitra AI Legal Redressal Assistant_`;

  const previewBox = document.getElementById("waMessagePreview");
  if (previewBox) {
    previewBox.value = noticeMessage;
  }
}

function copyWhatsAppNotice() {
  const previewBox = document.getElementById("waMessagePreview");
  if (!previewBox || !previewBox.value) return;
  navigator.clipboard.writeText(previewBox.value).then(() => {
    showToast("WhatsApp notice copied to clipboard!");
  }).catch(() => {
    previewBox.select();
    document.execCommand("copy");
    showToast("WhatsApp notice copied!");
  });
}

function dispatchWhatsAppNotice() {
  const previewBox = document.getElementById("waMessagePreview");
  if (!previewBox || !previewBox.value.trim()) {
    showToast("Notice message is empty.");
    return;
  }

  const rawPhone = document.getElementById("waRecipientPhone")?.value.replace(/[^0-9]/g, "") || "";
  const encodedText = encodeURIComponent(previewBox.value.trim());

  let waUrl = "";
  if (rawPhone.length >= 10) {
    // If 10 digits without country code, add 91 (India)
    const formattedPhone = rawPhone.length === 10 ? `91${rawPhone}` : rawPhone;
    waUrl = `https://wa.me/${formattedPhone}?text=${encodedText}`;
  } else {
    // Open WhatsApp app/web contact picker
    waUrl = `https://api.whatsapp.com/send?text=${encodedText}`;
  }

  window.open(waUrl, "_blank");
  showToast("Opening WhatsApp with pre-filled legal notice...");
}


