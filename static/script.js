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
  }
};

let currentLang = "en";
let speechRecognition = null;
let isListening = false;

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
    langSelect.value = lang === "en" ? "English" : "Hindi";
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
}

function toggleLanguage() {
  const nextLang = currentLang === "en" ? "hi" : "en";
  setLanguage(nextLang);
}

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
  speechRecognition.lang = currentLang === "hi" ? "hi-IN" : "en-IN";

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
// Text-to-Speech (TTS) Voice Readout Controller
// ==========================================================================
let currentSpeechUtterance = null;
let isSpeaking = false;
let isPaused = false;
let speechRate = 1.0;

function getOptimalVoice(langCode) {
  if (!('speechSynthesis' in window)) return null;
  const voices = window.speechSynthesis.getVoices();
  if (langCode === "hi") {
    return voices.find(v => v.lang.startsWith("hi")) || voices.find(v => v.lang.includes("IN")) || null;
  }
  return voices.find(v => v.lang === "en-IN") || voices.find(v => v.lang.startsWith("en")) || null;
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

  let textToRead = "";
  if (explanationEl) {
    textToRead += "Legal Guidance Summary: " + explanationEl.innerText.trim() + ". ";
  }

  if (actionItems.length > 0) {
    textToRead += " Immediate Action Steps: ";
    actionItems.forEach((act, idx) => {
      textToRead += `Step ${idx + 1}: ${act.innerText.trim()}. `;
    });
  }

  if (!textToRead.trim()) {
    showToast("No legal guidance text found to read.");
    return;
  }

  const isHindi = currentLang === "hi" || /[\u0900-\u097F]/.test(textToRead);
  const utterance = new SpeechSynthesisUtterance(textToRead);
  utterance.rate = speechRate;
  utterance.pitch = 1.0;
  utterance.lang = isHindi ? "hi-IN" : "en-IN";

  const voice = getOptimalVoice(isHindi ? "hi" : "en");
  if (voice) utterance.voice = voice;

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


