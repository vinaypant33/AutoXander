const sectionsData = [
  { type: 'personal', title: "Personal Details" },
  { type: 'textarea', title: "Profile", placeholder: "Write your profile summary" },
  { type: 'list', title: "Skills", placeholder: "List your skills (one per line)" },
  { type: 'textarea', title: "Education", placeholder: "List your education" },
  { type: 'textarea', title: "Experience", placeholder: "Professional Experience details" },
  { type: 'list', title: "Availability", placeholder: "Availability details (one per line)" }
];

const sections = document.getElementById('sections');

sectionsData.forEach((data, idx) => {
  const card = document.createElement('div');
  card.className = 'card';
  card.draggable = true;

  const header = document.createElement('div');
  header.className = 'card-header';
  header.innerHTML = `<span>${data.title}</span><i class="fas fa-chevron-down"></i>`;

  const content = document.createElement('div');
  content.className = 'card-content';

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
  const resumeContent = document.getElementById('resume-content');
  resumeContent.innerHTML = '';

  cards.forEach((card, idx) => {
    const contentArea = card.querySelector('.card-content');
    const inputs = contentArea.querySelectorAll('input, textarea');
    let sectionHTML = '';

    inputs.forEach(input => {
      const placeholder = input.getAttribute('placeholder') || "";

      if (input.id.includes('name')) {
        sectionHTML += `<h1 class="name">${input.value}</h1>`;
      } else if (input.id.includes('email')) {
        sectionHTML += `<p><strong>Email:</strong> ${input.value}</p>`;
      } else if (input.id.includes('phone')) {
        sectionHTML += `<p><strong>Phone:</strong> ${input.value}</p>`;
      } else if (input.id.includes('address')) {
        sectionHTML += `<p><strong>Address:</strong> ${input.value}</p>`;
      } else if (input.tagName === 'TEXTAREA' && input.value.trim()) {
        const title = card.querySelector('span').innerText;

        if (placeholder.toLowerCase().includes('skills') || placeholder.toLowerCase().includes('availability')) {
          const lines = input.value.split('\n').filter(line => line.trim() !== "");
          if (lines.length > 0) {
            sectionHTML += `<div class='section-title'>${title}</div><ul>${lines.map(line => `<li>${formatText(line.trim())}</li>`).join('')}</ul>`;
          }
        } else {
          const lines = input.value.split('\n').filter(line => line.trim() !== "");
          if (lines.length > 0) {
            sectionHTML += `<div class='section-title'>${title}</div>${lines.map(line => `<p>${formatText(line.trim())}</p>`).join('')}`;
          }
        }
      }
    });

    resumeContent.innerHTML += sectionHTML;
  });
}

function formatText(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold **text**
    .replace(/\*(.*?)\*/g, '<em>$1</em>');              // Italic *text*
}

function showTab(tab) {
  document.getElementById('content').style.display = (tab === 'content') ? 'block' : 'none';
  document.getElementById('customize').style.display = (tab === 'customize') ? 'block' : 'none';
  document.querySelectorAll('.tab-buttons button').forEach(btn => btn.classList.remove('active'));
  document.querySelector(`.tab-buttons button[onclick*="${tab}"]`).classList.add('active');
}

function adjustFontSize() {
  let v = parseInt(document.getElementById('fontSizeSlider').value);
  document.getElementById('fontSizeValue').innerText = v;
  document.getElementById('resume').style.fontSize = v + 'px';
}

function adjustFontFamily() {
  let font = document.getElementById('fontFamilySelector').value;
  document.getElementById('resume').style.fontFamily = font;
}

function adjustMargin() {
  let v = parseInt(document.getElementById('marginSlider').value);
  document.getElementById('resume').style.padding = v + 'px';
  document.getElementById('marginValue').innerText = v;
}

// function downloadPDF() {
//   const resumeElement = document.getElementById("resume");
//   const resumeNameInput = document.getElementById("resumeName");
//   const filename = resumeNameInput?.value.trim() || 'resume';

//   fetch('/download-pdf', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({
//       html: '<!DOCTYPE html><html><head><meta charset=\"utf-8\"><style>' + getPrintStyles() + '</style></head><body>' + resumeElement.outerHTML + '</body></html>',
//       filename: filename
//     })
//   })
//     .then(res => res.blob())
//     .then(blob => {
//       const a = document.createElement('a');
//       a.href = window.URL.createObjectURL(blob);
//       a.download = filename + '.pdf';
//       document.body.appendChild(a);
//       a.click();
//       a.remove();
//     })
//     .catch(err => console.error('PDF download failed:', err));
// }

function downloadPDF() {
  const resumeElement = document.getElementById("resume");
  const resumeNameInput = document.getElementById("resumeName");
  const filename = resumeNameInput?.value.trim() || 'resume';

  fetch('/download-pdf', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      html: '<!DOCTYPE html><html><head><meta charset="utf-8"><style>' + getPrintStyles() + '</style></head><body>' + resumeElement.outerHTML + '</body></html>',
      filename: filename
    })
  })
  .then(res => res.blob())
  .then(blob => {
    const a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = filename + '.pdf';
    document.body.appendChild(a);
    a.click();
    a.remove();
  })
  .catch(err => console.error('PDF download failed:', err));
}


function getPrintStyles() {
  return `
    body { margin: 0; font-family: 'Segoe UI', sans-serif; }
    .resume { width: 794px; min-height: 1123px; padding: 40px; box-sizing: border-box; }
    .section-title { font-weight: bold; margin-bottom: 8px; margin-top: 20px; font-size: 1.1rem; text-transform: uppercase; color: #111827; border-bottom: 2px solid #111827; padding-bottom: 2px; width: fit-content; }
    p, li { font-size: 0.95rem; color: #374151; line-height: 1.4; margin: 4px 0; }
    ul { padding-left: 20px; margin: 5px 0; }
    h1.name { font-size: 28px; font-weight: bold; margin: 0 0 10px 0; color: #111827; }
  `;
}

document.addEventListener('DOMContentLoaded', generateResume);
