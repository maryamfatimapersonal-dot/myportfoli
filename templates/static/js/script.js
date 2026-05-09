// Smooth scroll navigation - All pages/links working
document.querySelector('.nav-work').addEventListener('click', (e) => {
  e.preventDefault();
  document.getElementById('work-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
});
document.querySelector('.nav-experience').addEventListener('click', (e) => {
  e.preventDefault();
  document.getElementById('experience-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
});
document.querySelector('.nav-skills').addEventListener('click', (e) => {
  e.preventDefault();
  document.getElementById('skills-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
});

// Modal logic
const modal = document.getElementById('contactModal');
const openBtns = [document.getElementById('contactNavBtn'), document.getElementById('contactGlowBtn')];
const closeBtn = document.getElementById('closeModalBtn');

function openModal() {
  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
}
function closeModalFunc() {
  modal.classList.remove('active');
  document.body.style.overflow = '';
}

openBtns.forEach(btn => {
  if(btn) btn.addEventListener('click', (e) => {
    e.preventDefault();
    openModal();
  });
});

if(closeBtn) closeBtn.addEventListener('click', closeModalFunc);
modal.addEventListener('click', (e) => {
  if(e.target === modal) closeModalFunc();
});

// Animated stats counter
const animateNumbers = () => {
  const statNumbers = document.querySelectorAll('.stat-number');
  statNumbers.forEach(el => {
    let final = el.innerText;
    let numeric = parseInt(final);
    if(isNaN(numeric)) return;
    let current = 0;
    let step = Math.ceil(numeric / 40);
    const update = () => {
      current += step;
      if(current >= numeric) {
        el.innerText = final;
        return;
      }
      el.innerText = current;
      requestAnimationFrame(update);
    };
    setTimeout(() => update(), 200);
  });
};

window.addEventListener('load', () => {
  animateNumbers();
});