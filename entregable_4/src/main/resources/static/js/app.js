const preview = document.querySelector('#cover-preview');
const updateCover = () => {
  const selected = document.querySelector('input[name="cover"]:checked');
  if (preview && selected) preview.src = selected.closest('label').querySelector('img').src;
};
document.querySelectorAll('input[name="cover"]').forEach(input => input.addEventListener('change', updateCover));
updateCover();
