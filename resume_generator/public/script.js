// File: script.js

const sectionsData = [
  { type: 'personal', title: "Personal Details", icon: 'fa-user', side: 'left' },
  { type: 'textarea', title: "Profile", icon: 'fa-id-badge', placeholder: "Write your profile summary", side: 'left' },
  { type: 'list', title: "Skills", icon: 'fa-tools', placeholder: "List your skills (one per line)", side: 'left' },
  { type: 'textarea', title: "Education", icon: 'fa-graduation-cap', placeholder: "List your education", side: 'left' },
  { type: 'textarea', title: "Experience", icon: 'fa-briefcase', placeholder: "Professional Experience details", side: 'right' },
  { type: 'list', title: "Availability", icon: 'fa-clock', placeholder: "Availability details (one per line)", side: 'right' }
];

const sections = document.getElementById('sections');

sectionsData.forEach((data, idx) => {
  const card = document.createElement('div');
  card.className = 'card';
  card.draggable = true;
  card.id = `card-${idx}`;

  const header = document.createElement('div');
  header.className = 'card-header';
  header.innerHTML = `<span><i class="fas ${data.icon}"></i> ${data.title}</span><i class="fas fa-chevron-down"></i>`;

  const content = document.createElement('div');
  content.className = 'card-content';
  content.id = `content-${idx}`;

  if (data.type === 'personal') {
    content.innerHTML = `
      <input type="text" id="input-name" placeholder="Full Name" oninput="generateResume()">
      <input type="text" id="input-email" placeholder="Email" oninput="generateResume()">
      <input type="text" id="input-phone" placeholder="Phone" oninput="generateResume()">
      <input type="text" id="input-address" placeholder="Address" oninput="generateResume()">
    `;
  } else {
    content.innerHTML = `<textarea id="input-${idx}" placeholder="${data.placeholder}" oninput="generateResume()"></textarea>`;
  }

  header.onclick = () => {
    card.classList.toggle('active');
  };

  card.appendChild(header);
  card.appendChild(content);
  sections.appendChild(card);
});

Sortable.create(sections, {
  animation: 200,
  onEnd: generateResume
});

function generateResume() {
  const cards = document.querySelectorAll('#sections .card');
  const leftColumn = document.getElementById('left-column');
  const rightColumn = document.getElementById('right-column');
  leftColumn.innerHTML = '';
  rightColumn.innerHTML = '';

  cards.forEach((card, idx) => {
    const contentArea = card.querySelector('.card-content');
    const inputs = contentArea.querySelectorAll('input, textarea');
    let sectionHTML = '';

    const section = sectionsData[idx];

    inputs.forEach(input => {
      const placeholder = input.getAttribute('placeholder') || "";

      if (input.id.includes('name')) {
        sectionHTML += `<h1 id="resume-name" class="name">${input.value}</h1>`;
      } else if (input.id.includes('email')) {
        sectionHTML += `<div class="contact-info" id="resume-email"><p><i class='fas fa-envelope'></i> ${input.value}</p></div>`;
      } else if (input.id.includes('phone')) {
        sectionHTML += `<div class="contact-info" id="resume-phone"><p><i class='fas fa-phone'></i> ${input.value}</p></div>`;
      } else if (input.id.includes('address')) {
        sectionHTML += `<div class="contact-info" id="resume-address"><p><i class='fas fa-map-marker-alt'></i> ${input.value}</p></div>`;
      } else if (input.tagName === 'TEXTAREA' && input.value.trim()) {
        const lines = input.value.split('\n').filter(line => line.trim() !== '');
        if (placeholder.toLowerCase().includes('skills') || placeholder.toLowerCase().includes('availability')) {
          sectionHTML += `<div class='section-title'>${section.title.toUpperCase()}</div><ul>${lines.map(line => `<li>${applyFormatting(line.trim())}</li>`).join('')}</ul>`;
        } else {
          sectionHTML += `<div class='section-title'>${section.title.toUpperCase()}</div>${lines.map(line => `<p>${applyFormatting(line.trim())}</p>`).join('')}`;
        }
      }
    });

    if (section.side === 'left') {
      leftColumn.innerHTML += sectionHTML;
    } else {
      rightColumn.innerHTML += sectionHTML;
    }
  });
}

function applyFormatting(text) {
  return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

function showTab(tab) {
  document.getElementById('content').style.display = (tab === 'content') ? 'block' : 'none';
  document.getElementById('customize').style.display = (tab === 'customize') ? 'block' : 'none';
  document.getElementById('contentTab').classList.toggle('active', tab === 'content');
  document.getElementById('customizeTab').classList.toggle('active', tab === 'customize');
}

function adjustFontSize() {
  let v = parseInt(document.getElementById('fontSizeSlider').value);
  document.getElementById('fontSizeValue').innerText = v;
  const resume = document.getElementById('resume');
  resume.style.fontSize = v + 'px';
  resume.setAttribute('data-fontsize', v);
}

function adjustFontFamily() {
  let font = document.getElementById('fontFamilySelector').value;
  document.getElementById('resume').style.fontFamily = font;
}

function adjustColumns() {
  let leftVal = parseInt(document.getElementById('columnSplitSlider').value);
  document.getElementById('leftColumnValue').innerText = leftVal;
  document.querySelector('.left-column').style.flex = leftVal + '%';
  document.querySelector('.right-column').style.flex = (100 - leftVal) + '%';
}

function adjustMargin() {
  let marginVal = parseInt(document.getElementById('marginSlider').value);
  document.getElementById('marginValue').innerText = marginVal;
  const resume = document.getElementById('resume');
  resume.style.padding = marginVal + 'mm';
}

function getDownloadFilename() {
  const filenameInput = document.getElementById('filenameInput');
  let filename = filenameInput?.value?.trim();
  if (!filename) {
    filename = "resume"; // Default
  }
  return filename + ".pdf";
}

async function downloadPDF() {
  const resumeElement = document.getElementById('resume');
  const divider = document.querySelector('.divider-line');

  if (divider) divider.style.display = 'none';

  const fontSize = resumeElement.getAttribute('data-fontsize') || 14;

  const resumeHTML = `
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="UTF-8">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
      body { margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; font-size: ${fontSize}px; }
      .resume { width: 210mm; min-height: 297mm; padding: 20mm; box-sizing: border-box; display: flex; gap: 10mm; border: none; }
      .left-column, .right-column { box-sizing: border-box; }
      h1.name { font-size: ${parseInt(fontSize) + 6}px; }
      .section-title { text-transform: uppercase; margin-top: 20px; border-bottom: 2px solid #000; margin-bottom: 8px; font-weight: bold; display: inline-block; }
      p, li { font-size: ${fontSize}px; line-height: 1.4; margin: 2px 0; }
      .contact-info p { font-size: ${fontSize}px; line-height: 1.2; margin: 2px 0; }
      ul { padding-left: 20px; }
    </style>
  </head>
  <body>${resumeElement.outerHTML}</body>
  </html>`;

  try {
    const response = await fetch('/download-pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ html: resumeHTML })
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = getDownloadFilename();
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

  } catch (error) {
    console.error('Error downloading PDF:', error);
  }

  if (divider) divider.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', generateResume);
