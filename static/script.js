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
    btnAnalyze: "Analyze & Get Legal Guidance",
    btnAnalyzing: "Analyzing Verified Laws & Portals...",
    draftHeading: "Generate Official Complaint Draft",
    btnCopy: "Copy Complaint Draft",
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
    btnAnalyze: "कानूनी जानकारी व मार्गदर्शन प्राप्त करें",
    btnAnalyzing: "सत्यापित कानूनों की जांच हो रही है...",
    draftHeading: "औपचारिक शिकायत प्रारूप तैयार करें",
    btnCopy: "प्रारूप कॉपी करें",
    btnCopied: "कॉपी कर लिया गया!",
    btnDownload: "डाउनलोड करें (.txt)",
    btnPrint: "प्रिंट करें / PDF",
    checklistProgress: "तैयार साक्ष्य दस्तावेज:"
  }
};

let currentLang = "en";

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
  }
  problemInput.focus();
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
    // Fallback
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

// Print draft
function printDraft() {
  const draftArea = document.getElementById("complaintDraftText");
  if (!draftArea) return;
  const text = draftArea.value || draftArea.innerText;
  const printWindow = window.open("", "_blank");
  printWindow.document.write(`
    <html>
      <head>
        <title>NyayaMitra Legal Complaint Draft</title>
        <style>
          body { font-family: monospace; white-space: pre-wrap; padding: 2rem; line-height: 1.6; font-size: 13pt; }
        </style>
      </head>
      <body>${text}</body>
    </html>
  `);
  printWindow.document.close();
  printWindow.focus();
  setTimeout(() => printWindow.print(), 300);
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
