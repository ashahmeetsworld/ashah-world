// Sideways carousels (Instagram style): swipe through the slides, dots underneath show where you are; tap a dot to jump.
// Works for carousels in the page and ones added later (Field Notes load from Instagram after the page opens).
export function wireCarousel(car: HTMLElement) {
  if (car.dataset.wired) return;
  car.dataset.wired = '1';
  const track = car.querySelector<HTMLElement>('.car-track');
  const dots = car.querySelector<HTMLElement>('.car-dots');
  if (!track || !dots) return;
  const slides = () => Array.from(track.children) as HTMLElement[];
  const n = slides().length;
  dots.hidden = n < 2;
  dots.innerHTML = slides().map((_, i) => `<button type="button" tabindex="-1" aria-label="Slide ${i + 1}"><i></i></button>`).join('');
  const go = (i: number) => track.scrollTo({ left: slides()[i].offsetLeft - track.offsetLeft, behavior: 'smooth' });
  dots.querySelectorAll('button').forEach((b, i) => b.addEventListener('click', () => go(i)));
  const update = () => {
    const edge = track.getBoundingClientRect().left;
    let active = 0, best = Infinity;
    slides().forEach((s, i) => { const d = Math.abs(s.getBoundingClientRect().left - edge); if (d < best) { best = d; active = i; } });
    if (track.scrollLeft >= track.scrollWidth - track.clientWidth - 4) active = n - 1;
    dots.querySelectorAll('button').forEach((b, i) => b.classList.toggle('on', i === active));
  };
  track.addEventListener('scroll', update, { passive: true });
  update();
}

export const wireAll = (root: ParentNode = document) => root.querySelectorAll<HTMLElement>('.car').forEach(wireCarousel);

export const carouselHtml = (images: string[], alt: string, ratio = '4 / 5') =>
  `<div class="car" style="--ratio:${ratio}"><div class="car-track">${images
    .map((src, i) => `<div class="car-slide"><img src="${src}" alt="${i === 0 ? alt : ''}" loading="${i < 3 ? 'eager' : 'lazy'}" decoding="async" /></div>`)
    .join('')}</div><div class="car-dots" aria-hidden="true"></div></div>`;
